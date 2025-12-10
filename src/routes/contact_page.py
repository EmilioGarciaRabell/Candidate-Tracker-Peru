from flask import Blueprint, jsonify, request
from src.services.data_management import contact


contact_bp = Blueprint('contact', __name__)

@contact_bp.post("/contact")
def send_contact():
    data = request.get_json()

    contact.submit_request(data)

    return jsonify({
        "status": "success",
        "received": data
    }), 200
    