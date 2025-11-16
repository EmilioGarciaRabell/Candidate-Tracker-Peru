from flask import Blueprint, jsonify
from src.services.data_management import candidates, sentiment, social_media

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
    
@candidate_bp.get("/candidate/sentiment/<int:id>")
def get_candidate_sentiment(id):
    sentiment_anal = sentiment.get_candidate_sentiment(id)

    if not sentiment_anal:
        return jsonify({"error": "Sentiment not found"}), 404
    return jsonify ({"sentiment": sentiment_anal}), 200

@candidate_bp.get("/candidate/social/<int:id>")
def get_social_media(id):
    social_links = social_media.get_social_media(id)
    if not social_links:
        return jsonify({"error": "Sentiment not found"}), 404
    return jsonify ({"socials": social_links}), 200