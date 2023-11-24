import streamlit as st
from streamlit_chat import *
from test import moto
import time

# Function to initialize session state
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Ask me a question about Motopay!"}
        ]
initialize_session_state()

# Function for handling predefined questions from buttons
def ask_predefined_question(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    generate_chatbot_response(prompt)

# Buttons for predefined questions
question = st.button("Ask: 'What is motopay?'", on_click= st.chat_input('What is motopay?'))
st.button("Ask: 'What is cashfinder?'", on_click=lambda: ask_predefined_question('What is cashfinder?'))
st.button("Ask: 'What is Budget?'", on_click=lambda: ask_predefined_question('What is Budget?'))
st.button("Ask: 'What is shop?'", on_click=lambda: ask_predefined_question('What is shop?'))
st.button("Ask: 'What is motopay loan?'", on_click=lambda: ask_predefined_question('What is motopay loan?'))

def generate_chatbot_response(user_input):
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                t1 = time.time()
                response = moto(user_input)
                t2 = time.time()
                dur = t2 - t1
                msg = f'Response time: {round(dur, 2)} secs' if dur < 60 else f'Response time: {round(dur/60, 2)} mins'
                st.write(response)
                st.success(msg)
                message = {"role": "assistant", "content": response}
                st.session_state.messages.append(message)

# Handling chat input
if prompt := st.chat_input("Your question") or question:
    st.session_state.messages.append({"role": "user", "content": prompt})
    generate_chatbot_response(prompt)

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
