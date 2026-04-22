import anthropic


class ClaudeService:
    def __init__(self, api_key: str, model: str = "claude-haiku-4-5-20251001"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    async def chat(self, message: str, system_prompt: str, history: list) -> str:
        messages = self._build_messages(message, history)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=messages
        )
        return response.content[0].text

    async def chat_stream(self, message: str, system_prompt: str, history: list):
        messages = self._build_messages(message, history)

        with self.client.messages.stream(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=messages
        ) as stream:
            for text in stream.text_stream:
                yield text

    def _build_messages(self, message: str, history: list) -> list:
        messages = []
        for msg in history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        messages.append({"role": "user", "content": message})
        return messages