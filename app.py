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

    prompt = f"Schrijf een Sinterklaasgedicht voor {naam} over {onderwerp}. Extra info: {info}"

    try:
        print("DEBUG: Groq call gaat verstuurd worden…")

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=350,
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
