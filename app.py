import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from services.providers import get_available_providers, get_provider

load_dotenv()

app = Flask(__name__)

MAX_INPUT_CHARS = int(os.getenv("MAX_INPUT_CHARS", "12000"))


@app.get("/")
def index():
    return render_template(
        "index.html",
        providers=get_available_providers(),
        default_provider=os.getenv("AEGIS_DEFAULT_PROVIDER", "anthropic"),
    )


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "providers": get_available_providers(),
        }
    )


@app.post("/api/brief")
def generate_brief():
    data = request.get_json(silent=True) or {}

    notes = (data.get("notes") or "").strip()
    briefing_type = (data.get("briefing_type") or "daily").strip()
    provider_name = (data.get("provider") or os.getenv("AEGIS_DEFAULT_PROVIDER") or "anthropic").strip()

    if not notes:
        return jsonify({"error": "Please enter notes before generating a brief."}), 400

    if len(notes) > MAX_INPUT_CHARS:
        return jsonify(
            {
                "error": f"Notes are too long. Limit is {MAX_INPUT_CHARS} characters."
            }
        ), 400

    try:
        provider = get_provider(provider_name)
        result = provider.generate(notes=notes, briefing_type=briefing_type)

        return jsonify(
            {
                "brief": result.text,
                "provider": result.provider,
                "model": result.model,
                "briefing_type": briefing_type,
            }
        )

    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(debug=True)
