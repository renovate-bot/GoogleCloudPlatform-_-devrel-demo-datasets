#   Welcome to the PetVerse!

This repository contains sample data and loading commands for the PetVerse AI codelab.

Follow the instructions [in the codelab](https://codelabs.developers.google.com/devsite/codelabs/petverse_multimodal) to make the best use of these assets.

If you are looking to quickly deploy the petverse-profiles demo application, check the README file in petverse-profiles.

## Contents

- Table data: Raw tables with cats, dogs, hamsters and our beloved pets
- Multimedia: Videos, sounds, pictures portraying our furry friends

## Usage

To use this on your own, without the codelab, follow these instructions:

1. Clone this repository:

```bash
git clone https://github.com/GoogleCloudPlatform/devrel-demo-datasets
cd devrel-data-samples
```


2. **Create a Storage bucket and load the multimedia**

Replace the variables with your project ID and a name for your bucket:

```bash
gsutil mb -p <<project_id>> -l us-central1 gs://<<your_bucket_name>>
gsutil cp ./petverse/pets.csv gs://<<your_bucket_name>>/
gsutil -m cp -r ./petverse/bucket/* gs://<<your_bucket_name>>/
 ```

3. **Prosper!**

Create a dataset or use an existing one. Load the CSV file as a table in BigQuery by pasting the following command in [BigQuery Studio](https://console.cloud.google.com/bigquery)

```sql
LOAD DATA INTO your_dataset.pets
OPTIONS(
    description="Table for furry friend data"
  )
FROM FILES (
  skip_leading_rows=1,
  uris = ['gs://<<your_bucket_name>>/pets.csv'],
  format = 'CSV'
);
```


You can create the table with the media associated to each pet in BigQuery as follows:

```sql
CREATE TABLE your_dataset.pet_media_assets_split (
    Id INTEGER OPTIONS(description="ID of the pet"),
    profile_picture STRING OPTIONS(description="URI of the pet's profile picture"),
    additional_media ARRAY<STRING> OPTIONS(description="Array of URIs for additional media associated with the pet")
);

INSERT INTO your_dataset.pet_media_assets_split (Id, profile_picture, additional_media)
VALUES
    (1, 'gs://sample-data-and-media/petverse/yoda_profile_picture.png', ['gs://sample-data-and-media/petverse/additional_media/Yoda_asks_for_cuddles.mp4']),
    (2, 'gs://sample-data-and-media/petverse/Madonna_profile_picture.jpg', ['gs://sample-data-and-media/petverse/additional_media/Madonna_description.wav']),
    (3, 'gs://sample-data-and-media/petverse/pixel_profile_picture.png', ['gs://sample-data-and-media/petverse/additional_media/pixel thug life.mp4', 'gs://sample-data-and-media/petverse/additional_media/pixel_description.wav']),
    (4, 'gs://sample-data-and-media/petverse/sql_profile_picture.png', ['gs://sample-data-and-media/petverse/additional_media/SQL_description.wav', 'gs://sample-data-and-media/petverse/additional_media/SQL_favorite_toy.mp4']),
    (5, 'gs://sample-data-and-media/petverse/buddy_golden_retriever.png', []),
    (6, 'gs://sample-data-and-media/petverse/daisy_french_bulldog.png', []),
    (7, 'gs://sample-data-and-media/petverse/max_german_shepherd.png', ['gs://sample-data-and-media/petverse/additional_media/max_description_tells_jokes.mp4']),
    (8, NULL, []), -- Penny has no media
    (9, NULL, []), -- Rocky has no media
    (10, 'gs://sample-data-and-media/petverse/pip_hamster.png', ['gs://sample-data-and-media/petverse/additional_media/pip_Hamster_Wheel_Video_Generated.mp4']),
    (11, NULL, []), -- Squeaky has no media
    (12, 'gs://sample-data-and-media/petverse/scales_snake.png', []),
    (13, NULL, []); -- Capy has no media
```

## Licensing

* See [LICENSE](LICENSE) for code
* For dataset, media files (audio, video, images), [CC-0](https://creativecommons.org/public-domain/cc0/) applies