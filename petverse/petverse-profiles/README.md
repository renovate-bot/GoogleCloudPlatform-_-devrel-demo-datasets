#   Welcome to the PetVerse!

This is a quick demo application to make use of all the magical SQL statements generated [in this codelab](https://codelabs.developers.google.com/devsite/codelabs/petverse_multimodal).


This setup assumes:
1. Your Cloud Build and Cloud Run setup are running with the default (Compute) service account. This is not a recommended practice for production environments, however, we assume this demo is being run by beginners exploring in a throwaway, non-critical process in the context of the codelab.
2. You have almighty IAM admin permissions to correct permission errors
3. You have (at least) Storage Object User and so does the Compute service account or the account executing the build and Cloud Run services. Your pictures will not be displayed otherwise. If this was a real application, you would use [Signed URLs](https://cloud.google.com/storage/docs/access-control/signing-urls-with-helpers).
4. This application is using IAP authentication, which is a secure and simple method to authenticate in this context.
5. This application is running everything in the same container. In a real, production scenario, you would separate the services to make them reusable and scalable.
6. You are following these instructions in the [Cloud Shell](https://shell.cloud.google.com/)


## Instructions

1. Clone the repository and navigate to the application directory:

```bash
git clone https://github.com/GoogleCloudPlatform/devrel-demo-datasets
cd devrel-data-samples/petverse/petverse-profiles/
```

2. Test the application locally. Replace the project ID where the dataset `petverse` is. This assumes you have completed all the steps in the codelab.

```bash
gcloud config set project <<your project id>>
pip install --no-cache-dir -r requirements.txt
gunicorn --bind 0.0.0.0:8080 app:app
```

Unless you get errors, you should be able to click on the URL from which the application will be serving (e.g., https://127.0.0.1:8080 ).

Click around the interface and pay attention to the logs in the console. This will give you the chance to correct potential permission errors.

**Note**: If you can't see the pictures, make sure your user has Storage User for the bucket where the media is.

3. Deploy to Cloud Run

Execute `deploy.sh`. This script will attempt to create an image from this local repository.

If you run into permission errors, check the documentation for [Cloud Run](https://cloud.google.com/run/docs/deploying-source-code#required_roles)

## Licensing

* See [LICENSE](LICENSE) for code
* For dataset, media files (audio, video, images), [CC-0](https://creativecommons.org/public-domain/cc0/) applies