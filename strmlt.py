import streamlit as st
from streamlit_chat import *
import openai
# from test import moto
from test_3 import moto

import time

openai.api_key = st.secrets.OPENAI_API_KEY

# Streamlit page configuration
st.set_page_config(page_title="MotoPay Chatbot", layout="centered")

# Main Chat Interface
# st.title("MotoPay Chatbot")
st.header("Chat with AskMoto 💬")

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": f"Ask me a question about Motopay!"},
    ]


if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])


# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            t1 = time.time()
            response = moto(prompt) #, selected_language
            t2 = time.time()
            dur = t2 - t1
            msg = f'Response time: {round(dur, 2)} secs' if dur < 60 else f'Response time: {round(dur/60, 2)} mins'
            st.write(response)
            st.success(msg)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) # Add response to message history
