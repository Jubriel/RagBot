# hermex_chat_ui.py
import streamlit as st

from hermex import HermexAssistant

# Initialize assistant
if 'assistant' not in st.session_state:
    st.session_state.assistant = HermexAssistant()

assistant = st.session_state.assistant

# Set page config
st.set_page_config(page_title="Hermex Travel Assistant", page_icon="🧳",
                   layout="centered")

st.title("🧭 Hermex Travel Assistant")
st.markdown("Ask Hera anything about **Hermex Travels**!")

# User session
user_id = "user"  # You can replace this with real user auth/session logic

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask your question..."):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get assistant reply
    with st.chat_message("assistant"):
        with st.spinner("Hera is thinking..."):
            response = assistant.chat(user_id, prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant",
                                              "content": response})
