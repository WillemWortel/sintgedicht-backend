import os
from flask import Flask, jsonify, send_from_directory
from groq import Groq

# =====================
# Config
# =====================
app = Flask(__name__, static_folder="static", static_url_path="")

# Zorg dat je deze environment variable zet:
#   GROQ_API_KEY= "niets"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

PERSOON_NAAM = "Paula"  # <--- pas hier de naam aan

POEM_PROMPT = """
Schrijf een Sinterklaasgedicht in het Nederlands voor {name}.

Eisen:
- 12 tot 20 regels.
- Rijm ongeveer elke 2 regels.
- Luchtig, vriendelijk en een beetje grappig.
- Spreek {name} aan met 'je' en 'jij'.
- Geen grove taal, geen kwetsende opmerkingen.
- Sinterklaas en zijn Pieten mogen genoemd worden, maar houd het actueel en speels.

Begin direct met het gedicht, zonder titel of uitleg.
""".strip()


# =====================
# Routes
# =====================

@app.route("/")
def index():
    # serve index.html uit de static-map
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/gedicht")
def api_gedicht():
    """Maakt een nieuw Sinterklaasgedicht via Groq en geeft het terug als JSON."""
    prompt = POEM_PROMPT.format(name=PERSOON_NAAM)

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",  # kies hier je Groq-model
        messages=[
            {
                "role": "system",
                "content": "Je bent een creatieve Nederlandse Sinterklaasdichter.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.9,
        max_tokens=512,
    )

    text = completion.choices[0].message.content
    return jsonify({"gedicht": text})


if __name__ == "__main__":
    app.run(debug=True)
