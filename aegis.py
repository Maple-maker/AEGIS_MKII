"""
AEGIS - Phase 1.0
A simple daily briefing assistant.

Run with:  python3 aegis.py

Edit the NOTES variable below with your actual notes for the day,
then run this script. AEGIS will print AND speak your daily brief.
"""

import os
import subprocess
from anthropic import Anthropic
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Initialize the Claude client (it reads ANTHROPIC_API_KEY from environment automatically)
client = Anthropic()

# This is AEGIS's "personality" - tells Claude how to behave
SYSTEM_PROMPT = """You are AEGIS, a calm, precise personal assistant for a US Army officer.

Your tone is direct and professional, like a trusted aide-de-camp. You are not a chatbot.
You are mission-focused, respect the user's time, and never waste words.

When asked for a daily brief, structure your response as:
1. SITUATION: One sentence summary of where things stand.
2. PRIORITIES: The 2-3 most important things to accomplish today.
3. CONTEXT: Any background, deadlines, or context worth remembering.
4. INSIGHT: One proactive observation, recommendation, or question worth considering.

Keep the entire brief under 200 words - it will be spoken aloud during a commute.
Use natural spoken language. Avoid bullet symbols, markdown, or anything that sounds awkward when read."""


# ---- Edit this section with your actual notes ----
NOTES = """
Tasks today:
- Finalize training schedule for next month
- Review NCOER bullets for SSG Martinez
- 1500 PT brief with battalion S3
- Pick up dry cleaning before 1800

Notes:
- BN commander wants the operation order draft by Friday
- I keep putting off updating my finance spreadsheet
- Considering reading "Extreme Ownership" again

Goals this week:
- Establish a consistent morning writing routine
- Make progress on the Series 7 study plan
- Call mom (it has been 11 days)
"""
# ---------------------------------------------------


def get_brief(notes: str) -> str:
    """Send the notes to Claude and get back a daily brief."""
    response = client.messages.create(
        model="claude-haiku-4-5",  # Fast and cheap, perfect for daily briefings
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Here are my notes for today:\n\n{notes}\n\nGenerate my daily brief.",
            }
        ],
    )
    # The response has a list of "content blocks" - we want the text from the first one
    return response.content[0].text


def speak(text: str) -> None:
    """Speak the text aloud using macOS built-in 'say' command.
    'Daniel' is a British male voice that sounds appropriately JARVIS-like.
    Run 'say -v ?' in Terminal to see all available voices."""
    subprocess.run(["say", "-v", "Daniel", text])


if __name__ == "__main__":
    print("AEGIS: Generating daily brief...\n")
    brief = get_brief(NOTES)
    print(brief)
    print("\n--- Speaking now ---")
    speak(brief)
    print("Brief complete.")
