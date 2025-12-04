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
    naam = request.args.get("name", "vriend")
    onderwerp = request.args.get("onderwerp", "iets leuks")
    info = request.args.get("info", "")

    prompt = f"""
        Schrijf een Sinterklaasgedicht in het Nederlands voor {naam} in HTML-opmaak.

        Vorm:
        - Begin met:
          <h2>Lieve {naam},</h2>
        - Daarna volgt het gedicht in 4 tot 7 strofen.
        - Elke strofe heeft 4 of 5 regels.
        - Elke strofe staat in een eigen <p>…</p>-element.
        - Binnen elke strofe worden de regels gescheiden door <br>.
        - Gebruik de rijmschema's AABB, ABAB en AABBA door elkaar heen (varieer per strofe).
        - Gebruik geen exact hetzelfde woord als rijmwoord in één strofe.
        - Schrijf alleen een geldig HTML-fragment (dus geen <html>, <body>, <head>).

        Inhoud:
        - Het gedicht gaat over: {onderwerp}.
        - Verwerk deze extra informatie subtiel: {info}.
        - Spreek {naam} steeds aan met je en jij.
        - De toon is warm, Sinterklaas-achtig en licht humoristisch.
        - Geen sterretjes (*) of speciale markeringen rond rijmwoorden.

        Voorbeelden van strofen (alleen om de vorm te tonen, NIET herhalen in output):

        (AABB)
        <p>
        De zon verschijnt en vult het groene veld,<br>
        de ochtend wordt met frisse lucht gesteld.<br>
        Een vogel zingt, zo licht en vrij,<br>
        en nieuwe kansen komen dichterbij.<br>
        </p>

        (ABAB)
        <p>
        De bomen dansen zachtjes in de wind,<br>
        een blad dat dwarrelt zoekt zijn plek.<br>
        De wereld verandert zoals een kind,<br>
        dat leert en groeit bij elke trek.<br>
        </p>

        (AABBA)
        <p>
        Een wolk drijft zacht door hemelblauw,<br>
        geen haast, geen doel, alleen vertrouwen.<br>
        Hij reist maar voort door dag en nacht,<br>
        de zon die schijnt, een stille pracht,<br>
        en vindt zijn rust in ochtenddauw.<br>
        </p>

        Footer (één keuze maken, willekeurig):
        Kies precies één van de volgende afsluitingen en neem die 1-op-1 over als:
        <footer>... hier komt de groet ...</footer>

        1) Hartelijke groeten van Sinterklaas 🎁
        2) Vrolijke groetjes van de Sint!
        3) Met warme wensen van Sint en Piet
        4) Tot pakjesavond! — Sint en zijn Pieten
        5) Een vrolijke groet van de Pieten
        6) Dag hoor! — Sint knipoogt vriendelijk

        Let op:
        - Geen opsommingen in de footer
        - Schrijf de gekozen footer als één vloeiende zin
        - Alleen één <footer>-element, geen uitleg erbij

        Schrijf nu het volledige gedicht,
        met nieuwe rijmwoorden en nieuwe beelden,
        en passend bij {naam}, {onderwerp} en {info}.

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

