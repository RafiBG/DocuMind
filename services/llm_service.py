from langchain_openai import ChatOpenAI
from config import Config

class LLMService:
    def __init__(self, config: Config):
        self.config = config

        self.model = ChatOpenAI(
            base_url=config.LLM_BASE_URL,
            api_key=config.API_KEY,
            model=config.MODEL,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
            use_responses_api=False
        )

    def generate(
        self,
        prompt: str,
        system_message: str | None = None
    ) -> str:

        if system_message is None:
            system_message = self.config.SYSTEM_MESSAGE

        response = self.model.invoke([
            ("system", system_message),
            ("human", prompt)
        ])

        return response.content
