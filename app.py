import os
from flask import Flask, jsonify, request
from groq import Groq
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    Schrijf een volledig Nederlands Sinterklaasgedicht voor {naam} in HTML-opmaak.

    Regels:
    - 20 tot 28 regels, verdeeld in 4 tot 6 strofen.
    - Elke strofe in een aparte <p>.
    - De eerste regel begint altijd met:
      <h2>Lieve {naam},</h2>
    - Gebruik <br> om rijmregels te scheiden binnen de strofe.
    - Rijm om de 2 regels.
    - Humoristisch, warm en respectvol.
    - Laat het gedicht gaan over: {onderwerp}
    - Verwerk deze aanvullende informatie over dat onderwerp ook: {info}
    - Spreek {naam} direct aan met jij en je.
    - Geen uitleg buiten het gedicht.

    Structuur:
    - Start met een <h2> aanspreekvorm.
    - Eindig met een groet van de Sint of van Sint en zijn Pieten
      in een <footer> element, zoals:
      “Hartelijke groetjes van de Sint en zijn Pieten.” of
      “De alleraardigste groeten van Sint.” 🎁
    """

    try:
        print("DEBUG: Groq call gaat verstuurd worden…")

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
            temperature=0.9
        )

        print("DEBUG: Response binnen")
        print("DEBUG COMPLETION:", completion)

        text = completion.choices[0].message.content
        return jsonify({"gedicht": text})

    except Exception as e:
        print("GROQ ERROR:", e)
        return jsonify({"error": str(e), "gedicht": ""})

if __name__ == "__main__":
    app.run()
