from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser
from templates import pipeline_prompt
from langchain_ollama.llms import OllamaLLM


class ChatHandler:
    def __init__(self, model_name, ollama=False):
        if ollama:
            self.model = OllamaLLM(
                model=model_name
            )
        else:
            self.model = ChatOpenAI(
                model_name=model_name
            )

    def invoke_chain(self, prompt_parameters):
        chain = pipeline_prompt | self.model | StrOutputParser()
        return chain.invoke(prompt_parameters)
