from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def hello_world():
    return jsonify({"message": "Hello, World!"})
