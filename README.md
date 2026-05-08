# AEGIS - Phase 1.0

A personal AI assistant. Phase 1 generates a daily briefing from your notes
and speaks it aloud.

## First-time setup (do this once)

```bash
# 1. Create a virtual environment (an isolated Python sandbox for this project)
python3 -m venv venv

# 2. Activate it (you must do this every time you open a new terminal)
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your API key
cp .env.example .env
# Now edit .env and paste your real Anthropic API key in place of the placeholder
```

## Daily use

```bash
# 1. Activate the venv (if not already active)
source venv/bin/activate

# 2. Edit aegis.py - put today's notes in the NOTES variable

# 3. Run AEGIS
python3 aegis.py
```

You should see the brief printed in the terminal, then hear it spoken aloud.
