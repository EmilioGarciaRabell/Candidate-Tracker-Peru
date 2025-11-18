import datetime
from flask import Blueprint, jsonify
from src.services.data_management import candidates

storage = Blueprint('storage', __name__)

@app.get("/image/<filename>")
def get_image_url(filename):
    client = storage.Client()
    bucket = client.bucket("YOUR_BUCKET_NAME")
    blob = bucket.blob(filename)

    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=30),
        method="GET"
    )
    return jsonify({"filename":filename,"url": url})