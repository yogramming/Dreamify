import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

dream_keywords = ["dream", "nightmare", "sleep", "woke up", "last night I dreamed"]

def is_dream_related(text):
    return any(keyword.lower() in text.lower() for keyword in dream_keywords)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/interpret", methods=["POST"])
def interpret():
    data = request.get_json()
    user_input = data.get("prompt", "")

    if not is_dream_related(user_input):
        return jsonify({"reply": "Hmm, that doesn't seem like a dream. Try describing a dream!"})

    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "contents": [{
            "parts": [{"text": f"Interpret this dream: {user_input}"}]
        }]
    }

    try:
        response = requests.post(GEMINI_URL, headers=headers, json=body)
        response.raise_for_status()
        reply_text = response.json()['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"reply": reply_text})
    except Exception as e:
        print("Gemini API error:", e)
        return jsonify({"reply": "Oops! Something went wrong while contacting Gemini."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

