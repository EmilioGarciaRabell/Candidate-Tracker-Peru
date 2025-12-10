from flask import Blueprint, jsonify
from src.services.data_management import parties

PARTY = Blueprint('parties', __name__)

@PARTY.get("/parties")
def get_all_parties():
    party = parties.get_all_parties()
    return jsonify({"parties": party}), 200

@PARTY.get("/party/<int:id>")
def get_party_id(id):
    party = parties.get_party_by_id(id)

    if not party:
        return jsonify({"error": "party not found"}), 404
    
    return jsonify ({"party": party}), 200

