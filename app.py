from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Backend is live 🚀",
        "message": "Codexia API running successfully"
    })

@app.route("/analyze", methods=["POST", "GET"])
def analyze():
    data = request.json if request.is_json else {}

    return jsonify({
        "success": True,
        "input": data,
        "result": "Analyze route working ✅"
    })

# IMPORTANT FOR DEPLOYMENT
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
