from flask import Flask, render_template, request
from gtts import gTTS
from deep_translator import GoogleTranslator
import os, uuid

app = Flask(__name__)

AUDIO_FOLDER = "static/audio"

@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None
    outputvoice = None
    error = None

    if request.method == "POST":
        s = request.form.get("inputlang")
        t = request.form.get("outputlang")
        text = request.form.get("text")

        if not text:
            error = "Enter text"
        else:
            try:
                # Translate
                outputvoice = GoogleTranslator(source=s, target=t).translate(text)

                # Unique file
                filename = f"{uuid.uuid4()}.mp3"
                audio_file = os.path.join(AUDIO_FOLDER, filename)

                # TTS
                tts = gTTS(text=outputvoice, lang=t)
                tts.save(audio_file)

            except Exception as e:
                error = str(e)

    return render_template("index.html",
                           audio_file=audio_file,
                           outputvoice=outputvoice,
                           error=error)

if __name__ == "__main__":
    app.run(debug=True)