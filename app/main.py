from flask import Flask, request, jsonify
from functools import wraps
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


# ── Auth decorator ─────────────────────────────────────────────────────────────
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        secret = os.getenv("API_KEY")
        if not secret:
            return jsonify({"error": "Server misconfiguration: API_KEY not set."}), 500
        provided = request.headers.get("X-API-KEY")
        if not provided or provided != secret:
            logger.warning("Unauthorized access attempt.")
            return jsonify({"error": "Unauthorized. Provide a valid X-API-KEY header."}), 401
        return f(*args, **kwargs)
    return decorated


# ── Health check ───────────────────────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# ── Core endpoint ──────────────────────────────────────────────────────────────
@app.route("/sum", methods=["POST"])
@require_api_key
def calculate_sum():
    data = request.get_json(silent=True)

    if not data or "numbers" not in data:
        return jsonify({"error": "Request body must contain a 'numbers' key."}), 400

    numbers = data["numbers"]

    if not isinstance(numbers, list):
        return jsonify({"error": "'numbers' must be an array."}), 422

    if len(numbers) == 0:
        return jsonify({"error": "'numbers' array cannot be empty."}), 422

    if not all(isinstance(n, (int, float)) for n in numbers):
        return jsonify({"error": "All elements must be integers or floats."}), 422

    # Sequential sum — addition performed exactly n times, no shortcuts
    total = 0
    for num in numbers:
        total += num

    logger.info(f"Sequential sum of {len(numbers)} numbers = {total}")

    return jsonify({
        "result": total,
        "operations_performed": len(numbers),
        "message": "All numbers added sequentially. "
    }), 200