import os
from flask import Flask, jsonify, request
from groq import Groq
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/api/gedicht")
def api_gedicht():
    naam = request.args.get("naam", "vriend")
    onderwerp = request.args.get("onderwerp", "iets leuks")
    info = request.args.get("info", "")

    user_prompt = f"""
Schrijf een Sinterklaasgedicht voor {naam}.

Onderwerp: {onderwerp}
Extra informatie: {info}

Vereisten:
- 12 tot 20 regels
- Rijm om de 2 regels
- Humor en positiviteit
- Spreek {naam} aan met 'je' en 'jij'
- Geen titel bovenaan
"""

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "Je bent een grappige Nederlandse Sinterklaasdichter."},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.9,
            max_tokens=350,
        )
        text = completion.choices[0].message.content or ""
        return jsonify({"gedicht": text})

    except Exception as e:
        print("API ERROR:", e)
        return jsonify({"error": str(e), "gedicht": ""})
    

if __name__ == "__main__":
    app.run(debug=True)
