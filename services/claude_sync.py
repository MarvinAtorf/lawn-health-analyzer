from services.claude import ClaudeService

class ClaudeServiceSync(ClaudeService):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        super().__init__(api_key, model)

    def chat(self, message: str, system_prompt: str, history: list) -> str:
        messages = self._build_messages(message, history)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=messages
        )
        return response.content[0].text