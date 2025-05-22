from langchain_openai import ChatOpenAI
from langchain_ollama.llms import OllamaLLM
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from operator import itemgetter
from langchain.prompts import PromptTemplate


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
        self.conversation_buffer_memory = ConversationBufferMemory(
            return_messages=True)
        self.conversation_buffer_memory.load_memory_variables({})

    def invoke_chain(self, prompt_parameters, prompt, history_template):
        chain = RunnablePassthrough.assign(history=RunnableLambda(
            self.conversation_buffer_memory.load_memory_variables) | itemgetter("history")) | prompt | self.model
        response = chain.invoke(prompt_parameters)
        self.conversation_buffer_memory.save_context({"input": PromptTemplate.from_template(history_template).format(**prompt_parameters)},
                                                     {"output": response.content})
        print(self.conversation_buffer_memory.load_memory_variables({}))
        return response
