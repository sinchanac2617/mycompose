import os
import redis
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ----------------------------
# DATABASE CONFIG
# ----------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('DATABASE_HOST', 'db')}:{os.getenv('DATABASE_PORT', 5432)}/{os.getenv('POSTGRES_DB')}"
)
db = SQLAlchemy(app)

# ----------------------------
# REDIS CONFIG
# ----------------------------
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "cache"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

# ----------------------------
# ROUTES
# ----------------------------
@app.route("/")
def index():
    # Render HTML page instead of plain text
    return render_template("index.html")

@app.route("/health")
def health():
    try:
        # Check database
        db.session.execute("SELECT 1")

        # Check Redis
        redis_client.ping()

        return jsonify(status="healthy"), 200

    except Exception as e:
        return jsonify(status="unhealthy", error=str(e)), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

