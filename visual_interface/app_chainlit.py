# Cf. https://tinztwinshub.com/software-engineering/build-a-local-chatbot-in-minutes-with-chainlit/
import chainlit as cl
#from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from chainlit.types import ThreadDict
from chainlit.cli import run_chainlit

@cl.on_chat_start
async def on_chat_start():
    model = OllamaLLM(model="deepseek-r1:14b")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a financial expert with an extensive expert knowledge.",
            ),
            ("human", "{question}")
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)

@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable
    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()

@cl.on_stop
def on_stop():
    print("The user wants to stop the task!")

@cl.on_chat_end
def on_chat_end():
    print("The user disconnected!")

@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    print("The user resumed a previous chat session!")

if __name__ == '__main__':
    run_chainlit(__file__)