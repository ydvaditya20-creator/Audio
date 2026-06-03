from flask import Flask, request, jsonify
from gtts import gTTS
import tempfile
import os
import base64

app = Flask(__name__)

@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error":"No text"}), 400

    with tempfile.NamedTemporaryFile(delete=False,suffix=".mp3") as tmp:
        filename = tmp.name

    gTTS(text=text, lang="en").save(filename)

    with open(filename,"rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode()

    os.remove(filename)

    return jsonify({
        "audio": audio_b64
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
