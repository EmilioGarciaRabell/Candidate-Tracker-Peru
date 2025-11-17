import os
from google.cloud import storage
from dotenv import load_dotenv
load_dotenv()

GOOGLE_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

def upload_image(bucket_name,source_file_name,blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(source_file_name)


upload_image('images_candidate_tracker_candidates','/Users/carlalopez/Candidate-Tracker-Peru/etl/Perú.jpg','image_peru')



