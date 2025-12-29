from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/analyze", methods=["POST"])
def analyze():
    code = request.json.get("code", "")

    if not code.strip():
        return jsonify({"error": "No code provided"}), 400

    prompt = f"""
You are a static code analysis tool.
Analyze the following code and respond ONLY in valid JSON.

Return this exact structure:
{{
  "language": "...",
  "issue": "...",
  "lines": "...",
  "impact": "...",
  "suggestion": "...",
  "line_number": number
}}

Code:
{code}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    ai_output = response.choices[0].message.content

    try:
        return jsonify(eval(ai_output))
    except:
        return jsonify({
            "language": "Unknown",
            "issue": "AI parsing failed",
            "lines": "N/A",
            "impact": "Low",
            "suggestion": "Try simpler code",
            "line_number": None
        })

if __name__ == "__main__":
    app.run()
