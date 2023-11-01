import streamlit as st
from streamlit_chat import *
# from llama_index import VectorStoreIndex, ServiceContext, Document
# from llama_index.llms import OpenAI
# from llama_index import SimpleDirectoryReader
import openai
from test import moto

openai.api_key = st.secrets.OPENAI_API_KEY
st.header("Chat with AskMoto 💬")

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Motopay!"}
    ]
# reader = SimpleDirectoryReader(input_files=["FAQ.txt"], recursive=True)
# docs = reader.load_data()

# @st.cache_resource(show_spinner=False)
# def load_data():
#     with st.spinner(text="Loading and indexing the Streamlit docs – hang tight! This should take 1-2 minutes."):
#         service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-4", temperature=0.5, 
#                         system_prompt=f"""You are a friendly assistant.Your role is to provide valuable information about Motopay.
#                                             Respond with maximum of 40 words. 
#                                             Refrain from answering questions not related to this focus. 
#                                             """)
#                         )
#         index = VectorStoreIndex.from_documents(docs, service_context=service_context)
#         return index

# index = load_data()

# chat_engine = index.as_chat_engine(chat_mode="openai", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])


# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = moto(prompt)
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) # Add response to message history