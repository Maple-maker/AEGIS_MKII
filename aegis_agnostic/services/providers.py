import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List

from services.prompts import SYSTEM_PROMPT, BRIEFING_INSTRUCTIONS


@dataclass
class AIResponse:
    provider: str
    model: str
    text: str


class AIProvider(ABC):
    name: str

    @abstractmethod
    def generate(self, notes: str, briefing_type: str) -> AIResponse:
        pass


def build_user_prompt(notes: str, briefing_type: str) -> str:
    instruction = BRIEFING_INSTRUCTIONS.get(briefing_type, BRIEFING_INSTRUCTIONS["daily"])
    return f"""Briefing type: {briefing_type}

Instructions:
{instruction}

User notes:
{notes}

Generate the AEGIS output now."""


class AnthropicProvider(AIProvider):
    name = "anthropic"

    def __init__(self):
        from anthropic import Anthropic

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not configured.")

        self.model = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5")
        self.client = Anthropic(api_key=api_key)

    def generate(self, notes: str, briefing_type: str) -> AIResponse:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=700,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": build_user_prompt(notes, briefing_type),
                }
            ],
        )

        if not response.content:
            raise RuntimeError("Anthropic returned an empty response.")

        return AIResponse(
            provider=self.name,
            model=self.model,
            text=response.content[0].text,
        )


class OpenAIProvider(AIProvider):
    name = "openai"

    def __init__(self):
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured.")

        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=api_key)

    def generate(self, notes: str, briefing_type: str) -> AIResponse:
        response = self.client.responses.create(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=build_user_prompt(notes, briefing_type),
            max_output_tokens=700,
        )

        text = getattr(response, "output_text", None)
        if not text:
            raise RuntimeError("OpenAI returned an empty response.")

        return AIResponse(
            provider=self.name,
            model=self.model,
            text=text,
        )


class MockProvider(AIProvider):
    name = "mock"

    def __init__(self):
        self.model = "mock-aegis"

    def generate(self, notes: str, briefing_type: str) -> AIResponse:
        trimmed = notes.strip().splitlines()
        preview = " ".join(line.strip("- ").strip() for line in trimmed[:3]) or "No notes provided."

        text = (
            "AEGIS MOCK BRIEF. "
            "Situation: This is a test response, so no external AI provider was called. "
            f"Your notes appear to focus on: {preview}. "
            "Priority: Confirm the interface works, then configure a real provider key. "
            "Insight: The provider layer is functioning if you can see this message."
        )

        return AIResponse(
            provider=self.name,
            model=self.model,
            text=text,
        )


PROVIDER_CLASSES = {
    "anthropic": AnthropicProvider,
    "openai": OpenAIProvider,
    "mock": MockProvider,
}


def get_available_providers() -> List[Dict[str, object]]:
    return [
        {
            "id": "anthropic",
            "label": "Anthropic / Claude",
            "configured": bool(os.getenv("ANTHROPIC_API_KEY")),
            "default_model": os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5"),
        },
        {
            "id": "openai",
            "label": "OpenAI / GPT",
            "configured": bool(os.getenv("OPENAI_API_KEY")),
            "default_model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        },
        {
            "id": "mock",
            "label": "Mock / Test Mode",
            "configured": True,
            "default_model": "mock-aegis",
        },
    ]


def get_provider(provider_name: str | None = None) -> AIProvider:
    selected = (provider_name or os.getenv("AEGIS_DEFAULT_PROVIDER") or "anthropic").lower()

    if selected not in PROVIDER_CLASSES:
        valid = ", ".join(PROVIDER_CLASSES.keys())
        raise ValueError(f"Unknown provider '{selected}'. Valid providers: {valid}")

    return PROVIDER_CLASSES[selected]()
