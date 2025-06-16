# StoryLens – Multi-modal Photo Story Generator

StoryLens turns any photo into a short, creative story (or poem) and narrates it with an AI voice.

| Feature | Model / Library |
|---------|-----------------|
| Visual story generation | microsoft/kosmos-2 (Vision-to-Language) |
| Text-to-Speech | coqui-ai/XTTS-v2 (Multi-lingual TTS) |
| Backend | Python 3 + Flask |
| Front-end | HTML / JavaScript + Fetch API |

---

## Demo
1. Choose a photo from your computer.
2. Click **Generate**.
3. Wait a few seconds – a short story appears and starts playing as audio.
4. Share the page link or download the `.mp3`.

![StoryLens screenshot](docs/screenshot.png)

---

## Quick-start (local)

```bash
# 1. Clone repo & enter folder
$ git clone https://github.com/hemaharshini18/StoryLens.git
$ cd storylens

# 2. Create Python venv (recommended)
$ python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install deps (≈ 1-2 min; models download on first run)
$ pip install -r requirements.txt

# 4. Run server
$ flask --app app run --reload

# 5. Open browser
Go to http://127.0.0.1:5000
```

---

## Deployment
StoryLens is backend-only; any static host that can run a Python process works (Render, Railway, Fly, etc.).
Set `HF_HOME` to a persistent volume/cache to avoid re-downloading models.

---

## Endpoints
| Method | Path | Body | Description |
|--------|------|------|-------------|
| POST | `/generate` | `multipart/form-data` field `photo` | Returns JSON `{story, audio_url}` |
| GET | `/audio/<filename>` | – | Streams generated `.mp3` |

---

## Configuration
Environment variables:

| Name | Default | Meaning |
|------|---------|---------|
| `STORYLENS_LANGUAGE` | `en` | Target narration language/voice (see XTTS docs) |
| `STORYLENS_OUTPUT_DIR` | `outputs` | Folder for generated audio |

---

## Models
1. **microsoft/kosmos-2** – Vision-Language model from Microsoft Research
   * Tasks: image tagging, captioning, VQA, V2L generation.
   * License: MIT.
2. **coqui-ai/XTTS-v2** – Cross-lingual multi-speaker TTS (Coqui).
   * License: Apache-2.0.

Both models are downloaded automatically from the 🤗 Hugging Face Hub on first use.

---

## Acknowledgements
* Microsoft Research for Kosmos-2.
* Coqui for XTTS-v2.
* HuggingFace for Transformers, TTS and model hosting.

---

## License
MIT © 2025 StoryLens contributors
