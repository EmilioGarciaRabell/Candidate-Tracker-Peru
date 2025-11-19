from flask import Blueprint, jsonify
from google.cloud import storage
import datetime
google_storage_bp = Blueprint('storage', __name__)


@google_storage_bp.get("/image/<int:filename>")
def get_image_url(filename):
    client = storage.Client()
    bucket = client.bucket("images_candidate_tracker_candidates")
    blob = bucket.blob(str(filename))
    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=30),
        method="GET"
    )

    return jsonify({"url": url})

@google_storage_bp.get("/pImage/<int:filename>")
def get_parties_url(filename):
    client = storage.Client()
    bucket = client.bucket("images_candidate_tracker_parties")
    blob = bucket.blob(str(filename))
    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=30),
        method="GET"
    )
    return jsonify({"url": url})