from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import json

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "Codexia backend running"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    code = data.get("code", "")

    if not code.strip():
        return jsonify({"error": "No code provided"}), 400

    prompt = f"""
Analyze the following code and respond ONLY with valid JSON.
Do NOT include markdown, backticks, or explanations.

Return exactly this structure:
{{
  "language": "string",
  "issue": "string",
  "lines": "string",
  "impact": "string",
  "suggestion": "string",
  "line_number": number
}}

Code:
{code}
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        ai_text = response.output_text.strip()

        parsed = json.loads(ai_text)  # ✅ SAFE
        return jsonify(parsed)

    except Exception as e:
        return jsonify({
            "language": "Unknown",
            "issue": "Backend or AI failure",
            "lines": "N/A",
            "impact": "Low",
            "suggestion": str(e),
            "line_number": None
        }), 200

if __name__ == "__main__":
    app.run()
