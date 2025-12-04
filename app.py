import os
from flask import Flask, jsonify, request
from groq import Groq
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = "Je bent een creatieve Nederlandse Sinterklaasdichter."

@app.route("/")
def home():
    return "Sinterklaas API actief 🎁"

@app.route("/api/gedicht")
def api_gedicht():
    naam = request.args.get("naam", "vriend")

    user_prompt = f"""
Schrijf een Sinterklaasgedicht in het Nederlands voor {naam}.

Eisen:
- 12 tot 20 regels.
- Rijm elke 2 regels.
- Gebruik humor en een vriendelijke toon.
- Noem Sinterklaas en Pieten.
- Begin direct met het gedicht, geen titel.
- Spreek {naam} aan met 'je' en 'jij'.
"""

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.9,
            max_tokens=300,
        )

        text = completion.choices[0].message.content or ""
        return jsonify({"gedicht": text})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e), "gedicht": ""})
    

if __name__ == "__main__":
    app.run(debug=True)
