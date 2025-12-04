import os
from flask import Flask, jsonify, request
from groq import Groq

app = Flask(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return "API werkt!"

@app.route("/api/gedicht")
def api_gedicht():
    naam = request.args.get("naam", "vriend")
    onderwerp = request.args.get("onderwerp", "iets leuks")
    info = request.args.get("info", "")

    prompt = f"""
Schrijf een Sinterklaasgedicht voor {naam}.

Onderwerp: {onderwerp}
Extra informatie: {info}

Eisen:
- 12 tot 20 regels
- Rijm om de 2 regels
- Spreek {naam} aan met je/jij
- Geen titel bovenaan
"""

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "Je bent een grappige Nederlandse Sinterklaasdichter."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.9,
        max_tokens=350,
    )

    text = completion.choices[0].message.content or ""
    return jsonify({"gedicht": text})

if __name__ == "__main__":
    app.run()
