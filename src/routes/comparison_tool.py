from flask import Blueprint, jsonify
from src.services.data_management import candidates

comparison_bp = Blueprint('compare', __name__)

@comparison_bp.get("/<int:candidate_id1>,<int:candidate_id2>")
def get_candidates_info(candidate_id1, candidate_id2):
    candidate1 = candidates.get_candidate(candidate_id1)
    candidate2 = candidates.get_candidate(candidate_id2)
    
    if not candidate_id1 or not candidate_id1:
        return jsonify({"error": "Candidate not found"}), 404
    
    return jsonify ({"candidate1": candidate1, "candidate2":candidate2}), 200