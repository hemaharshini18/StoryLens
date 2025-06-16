"""StoryLens Flask application."""

import os
import uuid
from pathlib import Path
from typing import Tuple

from flask import Flask, request, jsonify, send_from_directory, render_template
from PIL import Image

# Lazy imports (heavy) – done inside helper functions

OUTPUT_DIR = Path(os.getenv("STORYLENS_OUTPUT_DIR", "outputs"))
OUTPUT_DIR.mkdir(exist_ok=True)

LANGUAGE = os.getenv("STORYLENS_LANGUAGE", "en")

app = Flask(__name__, static_folder="static", template_folder="templates")


def generate_story(image: Image.Image) -> str:
    """Run Microsoft Kosmos-2 (public checkpoint) to create a short story/poem from an image."""
    from transformers import AutoProcessor, AutoModelForVision2Seq
    import torch

    # Public, no-token checkpoint (224-patch)
    model_name = "microsoft/kosmos-2-patch14-224"
    processor = AutoProcessor.from_pretrained(model_name)
    model = AutoModelForVision2Seq.from_pretrained(model_name)

    # Simple natural-language prompt works fine for this checkpoint
    prompt = "Write a short creative story about this image:"
    inputs = processor(images=image, text=prompt, return_tensors="pt")
    with torch.no_grad():
        generated_ids = model.generate(**inputs, max_length=120)

    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text.strip()


def tts(text: str, language: str = LANGUAGE) -> Tuple[str, Path]:
    """Generate speech audio from text using Coqui XTTS-v2.

    Returns (filename, path).
    """
    from TTS.api import TTS as CoquiTTS

    model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
    tts = CoquiTTS(model_name)
    filename = f"{uuid.uuid4().hex}.wav"
    out_path = OUTPUT_DIR / filename
    tts.tts_to_file(text=text, file_path=str(out_path), speaker_wav=None, language=language)
    return filename, out_path


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    if "photo" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["photo"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        image = Image.open(file.stream).convert("RGB")
    except Exception as exc:
        return jsonify({"error": f"Invalid image: {exc}"}), 400

    # 1. Story
    story_text = generate_story(image)

    # 2. Audio
    audio_filename, _ = tts(story_text)

    return jsonify({"story": story_text, "audio_url": f"/audio/{audio_filename}"})


@app.route("/audio/<path:filename>", methods=["GET"])
def serve_audio(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=False)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
