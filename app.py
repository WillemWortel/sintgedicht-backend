import os
import random
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
    aantal = random.randint(1, 6)

    prompt = f"""
    Schrijf een Sinterklaasgedicht in het Nederlands voor {naam} in HTML-opmaak.

    Vorm:
    Begin met een aanhef in een h2 tag.
    Kies precies één van de volgende aanhef en neem die 1-op-1 over als:
    1) Beste {naam} 🎁,
    2) Lieve {naam},
    3) Aan {naam}, de beste schoonmoeder,
    4) {naam},
    - Daarna komen precies 2 strofes.
    - Elke strofe heeft 4 of 5 regels.
    - Elke strofe staat in een eigen p element.
    - Binnen elke strofe worden de regels gescheiden door br.
    - Gebruik de rijmschema's AABB, ABAB en AABBA door elkaar heen (varieer per strofe).
    - Gebruik geen exact hetzelfde woord als rijmwoord in één strofe.
    - Schrijf alleen een geldig HTML-fragment voor in een div.

    Inhoud:
    - Het gedicht gaat over: {onderwerp}.
    - Verwerk deze extra informatie subtiel: {info}.
    - Spreek {naam} steeds aan met je en jij.
    - De toon is warm, Sinterklaas-achtig en licht humoristisch.
    - Geen sterretjes (*) of speciale markeringen rond rijmwoorden.

    Voorbeelden van strofen (alleen om de vorm te tonen, NIET herhalen in output):

    (AABB)
    De zon verschijnt en vult het groene veld,
    de ochtend wordt met frisse lucht gesteld.
    Een vogel zingt, zo licht en vrij,
    en nieuwe kansen komen dichterbij.

    (ABAB)
    De bomen dansen zachtjes in de wind,
    een blad dat dwarrelt zoekt zijn plek.
    De wereld verandert zoals een kind,
    dat leert en groeit bij elke trek.


    (AABBA)
    Een wolk drijft zacht door hemelblauw,
    geen haast, geen doel, alleen vertrouwen.
    Hij reist maar voort door dag en nacht,
    de zon die schijnt, een stille pracht,
    en vindt zijn rust in ochtenddauw.


    Kies vervolgens precies één van de volgende afsluitingen als footer willekeurig en neem die 1-op-1 over als:
    <footer>... hier komt de groet ...</footer>

    1) Hartelijke groeten van Sinterklaas 🎁
    2) Vrolijke groetjes van de Sint!
    3) Met warme wensen van Sint en Piet
    4) Tot pakjesavond! — Sint en zijn Pieten
    5) Een vrolijke groet van de Pieten
    6) Dag hoor!

    Let op:
    - Geen opsommingen in de footer
    - Schrijf de gekozen footer als één vloeiende zin
    - Alleen één <footer>-element, geen uitleg erbij

    Schrijf nu het volledige gedicht
    """

    try:
        print("DEBUG: Groq call gaat verstuurd worden…")

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            #max_tokens=700,
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





