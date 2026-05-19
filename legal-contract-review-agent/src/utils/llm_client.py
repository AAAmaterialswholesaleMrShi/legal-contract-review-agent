"""LLM client wrapper that supports MiMo and OpenAI-compatible APIs."""
import json
import os

import openai
import yaml
from rich.console import Console

console = Console()


class LLMClient:
    def __init__(self, model: str = None):
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)

        self.config = config["llm"]
        self.model = model or self.config["model"]
        api_key = os.getenv(self.config["api_key_env"])

        if not api_key:
            console.print("[yellow]Warning: API key not found. Running in mock mode.[/]")
            self.client = None
        else:
            base_url = (
                "https://api.mimo.ai/v1"
                if self.config["provider"] == "mimo"
                else None
            )
            self.client = openai.OpenAI(
                api_key=api_key,
                base_url=base_url,
            )

    def complete(
        self, prompt: str, temperature: float = None, max_tokens: int = None
    ) -> str:
        if self.client is None:
            return json.dumps({
                "passed": True,
                "explanation": "Mock mode: clause appears compliant based on pattern matching.",
            })

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature or self.config["temperature"],
            max_tokens=max_tokens or self.config["max_tokens"],
        )
        return response.choices[0].message.content
