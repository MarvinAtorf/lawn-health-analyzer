from abc import ABC, abstractmethod

class LLMService(ABC):
    @abstractmethod
    async def chat(self, message: str) -> str:
        pass

    @abstractmethod
    async def chat_stream(self , message: str, system_prompt: str, history:list) -> AsyncGenerator[str, None]:
        pass