# Cf. https://medium.com/@gelsonm/building-a-local-chat-application-with-streamlit-ollama-and-llama-3-2-8f5b116dd8ee
import logging
import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from config import CHAT_PROMPT_TEMPLATE
from langchain_core.output_parsers import StrOutputParser


logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s %(levelname)s %(message)s')



def main():
    logging.info("main_page.main()")

    st.markdown(
        "<h2 style='text-align: center; color: #4CAF50; font-family: Arial;'>HAL🪶</h2>",
        unsafe_allow_html=True,
    )
    template = CHAT_PROMPT_TEMPLATE
    prompt = ChatPromptTemplate.from_template(template)

    # Load the local model that we pulled using ollama
    model = OllamaLLM(model="deepseek-r1:14b")
    chain = prompt | model | StrOutputParser()

    # Maintain a chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! How may I help you?"}
        ]
    # Display the chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    if user_input := st.chat_input("How may I help you?"):
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate assistant response
        with st.chat_message("assistant"):
            #response = chain.invoke({"question": user_input})
            response = chain.stream({"question": user_input})
            #st.markdown(response)
            st.write_stream(response)

        # Add assistant response to session state
        st.session_state.messages.append({"role": "assistant", "content": response})



if __name__ == '__main__':
    main()