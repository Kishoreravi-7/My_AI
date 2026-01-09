import os
from typing import List
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


class LisaAI:
    def __init__(self):
        # Read API key from environment variable
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not set. Please set it as an environment variable."
            )

        # Connect to Groq using OpenAI-compatible API
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

        self.model = "llama-3.3-70b-versatile"

        self.system_prompt = (
            "You are Lisa, an intelligent and friendly voice-enabled AI assistant. "
            "Be concise but helpful in your responses."
        )

        self.conversation_history: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.system_prompt}
        ]

    def process_command(self, user_input: str) -> str:
        self.conversation_history.append(
            {"role": "user", "content": user_input}
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                max_tokens=500
            )

            reply = response.choices[0].message.content or ""

            self.conversation_history.append(
                {"role": "assistant", "content": reply}
            )

            # Keep system prompt + last 20 messages
            if len(self.conversation_history) > 21:
                self.conversation_history = (
                    [self.conversation_history[0]] +
                    self.conversation_history[-20:]
                )

            return reply

        except Exception as e:
            return f"Error: {str(e)}"

    def clear_context(self):
        self.conversation_history = [
            {"role": "system", "content": self.system_prompt}
        ]
        return "Conversation history cleared."
