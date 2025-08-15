# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, render_template, request
from google.cloud import bigquery
import google.cloud.aiplatform as aiplatform

app = Flask(__name__)

# Initialize BigQuery client
PROJECT_ID = os.environ.get('GCP_PROJECT')
bq_client = bigquery.Client(project=PROJECT_ID)

# Initialize Vertex AI
aiplatform.init(project=PROJECT_ID, location='us-central1')


def get_all_pets():
    """Fetches all pets from the BigQuery 'pets' table."""
    sql = """
        SELECT
            Id,
            Name,
            Species,
            profile_picture
        FROM
            `petverse.pets`
        ORDER BY
            Name
    """
    print(f"Executing SQL: \n{sql}")
    query_job = bq_client.query(sql)
    pets = query_job.result()
    return pets

def get_pet_details(pet_id):
    """Fetches detailed information for a single pet."""
    sql = """
        SELECT
            *
        FROM
            `petverse.pets`
        WHERE
            Id = @pet_id
    """
    print(f"Executing SQL: \n{sql}")
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("pet_id", "INT64", pet_id),
        ]
    )
    query_job = bq_client.query(sql, job_config=job_config)
    # Returns an iterator of rows
    rows = query_job.result()
    return list(rows)[0] if rows.total_rows > 0 else None

def get_similar_pets(pet_id):
    """Finds similar pets based on embedding cosine distance."""
    sql = """
        SELECT
            t2.Id as id,
            p.Name as name,
            p.profile_picture as profile_picture
        FROM
            `petverse.profile_embeddings` AS t1
        JOIN
            `petverse.profile_embeddings` AS t2 ON COSINE_DISTANCE(t1.ml_generate_embedding_result, t2.ml_generate_embedding_result) < 0.5
        JOIN
            `petverse.pets` p ON t2.Id = p.Id
        WHERE
            t1.Id = @pet_id AND t1.Id != t2.Id
            AND t1.content.uri IS NOT NULL
            AND t2.content.uri IS NOT NULL
        ORDER BY
            COSINE_DISTANCE(t1.ml_generate_embedding_result, t2.ml_generate_embedding_result)
        LIMIT 5;
    """
    print(f"Executing SQL: \n{sql}")
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("pet_id", "INT64", pet_id),
        ]
    )
    query_job = bq_client.query(sql, job_config=job_config)
    similar_pets = query_job.result()
    return similar_pets

def search_pets_semantic(query):
    """Performs a semantic search for pets based on a query."""
    sql = """
        SELECT
            base.content,
            p.Name,
            p.Id,
            p.profile_picture
        FROM
            VECTOR_SEARCH(
                TABLE `petverse.text_embeddings`,
                'ml_generate_embedding_result',
                (
                    SELECT ml_generate_embedding_result, content AS query
                    FROM ML.GENERATE_EMBEDDING(
                        MODEL `petverse.textembedding`,
                        (SELECT @query AS content)
                    )
                ),
                top_k => 3,
                options => '{"fraction_lists_to_search": 0.50}'
            )
        JOIN
            `petverse.pets` p ON base.Id = p.Id
        ORDER BY
            distance DESC
    """
    print(f"Executing SQL: {sql}")
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("query", "STRING", query),
        ]
    )
    query_job = bq_client.query(sql, job_config=job_config)
    results = query_job.result()
    return results



@app.route('/')
def index():
    """Main gallery page."""
    pets = get_all_pets()
    return render_template('index.html', pets=pets)

@app.route('/pet/<int:pet_id>')
def pet_profile(pet_id):
    """Pet profile page."""
    pet = get_pet_details(pet_id)
    if pet is None:
        return "Pet not found", 404

    similar_pets = get_similar_pets(pet_id)
    return render_template('pet.html', pet=pet, similar_pets=similar_pets)

@app.route('/search')
def search():
    """Search results page."""
    query = request.args.get('query')
    if not query:
        return "Please provide a search query", 400

    search_results = search_pets_semantic(query)
    return render_template('search.html', pets=search_results, query=query)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
