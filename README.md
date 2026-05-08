# AEGIS - Model-Agnostic Web App

AEGIS is a personal AI assistant web app designed for daily briefings, commander updates, weekly reviews, and second-brain style analysis.

This version is model-agnostic. You can choose between:

- Anthropic / Claude
- OpenAI / GPT
- Mock provider for testing without an API key

## Local setup

```bash
cd aegis_agnostic
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and add whichever API keys you want to use.

Then run:

```bash
flask --app app run --debug
```

Open:

```text
http://127.0.0.1:5000
```

## Railway deployment

Push this folder to GitHub, then deploy the repo on Railway.

Add Railway variables:

```text
AEGIS_DEFAULT_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key
ANTHROPIC_MODEL=claude-haiku-4-5
OPENAI_API_KEY=sk-your-openai-key
OPENAI_MODEL=gpt-4o-mini
MAX_INPUT_CHARS=12000
```

You do not need both API keys. Add only the providers you plan to use.

## Provider selection

The browser interface lets you pick the provider per request.

Recommended early use:

- Daily Brief: Claude or OpenAI
- Commander Update: Claude
- Fast summaries: OpenAI small model
- Testing UI: Mock

## Security warning

Do not paste classified, sensitive operational, or private soldier information into a cloud-hosted app.
