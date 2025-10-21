from flask import Blueprint, jsonify
from src.services.data_management import candidates

candidate_bp = Blueprint('candidate_bp', __name__)


@candidate_bp.get("/candidates")
def get_candidates():
    candidates_list = candidates.get_candidates()
    return jsonify({'candidates':candidates_list}) , 200

@candidate_bp.get("/candidate/<int:id>")
def get_candidate(id):
    candidate = candidates.get_candidate(id)

    if not candidate:
        return jsonify({"error": "Candidate not found"}), 404
    
    return jsonify ({"candidate": candidate}), 200
    