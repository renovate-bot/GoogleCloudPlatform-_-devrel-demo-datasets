#!/bin/bash
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


# Script to create an artifact repository, a container image and deploy to Cloud Run

# Replace with your details
export SERVICE_NAME="petverse-profiles"
export REPOSITORY_NAME="cloud-run-source-deploy"
export REGION="us-central1"
export PROJECT_ID=$(gcloud config get-value project)
export IMAGE_URL="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/${SERVICE_NAME}:latest"

# Check if the repository exists, and create it if it doesn't
if ! gcloud artifacts repositories describe ${REPOSITORY_NAME} --location=${REGION} --project=${PROJECT_ID} &> /dev/null; then
  echo "Repository ${REPOSITORY_NAME} does not exist. Creating it..."
  gcloud artifacts repositories create ${REPOSITORY_NAME} --repository-format=docker --location=${REGION} --project=${PROJECT_ID}
fi

# Build the container image
gcloud builds submit --tag ${IMAGE_URL}

# Deploy the service to Cloud Run
gcloud beta run deploy ${SERVICE_NAME} \
  --region=${REGION} \
  --image=${IMAGE_URL} \
  --no-allow-unauthenticated \
  --iap
  --labels dev-tutorial=codelab-433288268

# Grant the current user IAP access
export USER_EMAIL=$(gcloud config get-value account)
echo "Adding ${USER_EMAIL} to IAP policy for ${SERVICE_NAME}..."
gcloud beta iap web add-iam-policy-binding \
  --member=user:${USER_EMAIL} \
  --role=roles/iap.httpsResourceAccessor \
  --region=${REGION} \
  --resource-type=cloud-run \
  --service=${SERVICE_NAME}
