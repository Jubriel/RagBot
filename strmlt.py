# import streamlit as st
# from streamlit_chat import message
# from test import moto

# #Creating the chatbot interface
# st.set_page_config(
#     page_title="Ask-Moto | Friendly Assistant",
#     page_icon= "✅",
#     layout="centered",
#     # initial_sidebar_state='collapsed',
# )
# st.title("Ask-Moto")

# # Storing the chat
# if 'past' not in st.session_state:
#     st.session_state['past'] = []
# if 'generated' not in st.session_state:
#     st.session_state['generated'] = []

    
# st.empty()
# if st.session_state['generated']:
#     for i in range(len(st.session_state['generated'])-1, -1, -1):
#         message(st.session_state['past'][-i], is_user=True, key=str(i) + '_user')
#         message(st.session_state["generated"][-i], key=str(i))

# # We will get the user's input by calling the get_text function
# def get_text():
#     input_text = st.text_input("You: ", key="input", )
#     return input_text

# user_input = get_text()

# if user_input:
#     output = moto(user_input)

#     st.session_state.past.append(user_input)
#     st.session_state.generated.append(output)






import streamlit as st
from streamlit_chat import message
from test import moto

def initialize_chat_history():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def display_chat_history():
    chat_container = st.empty()
    with st.container():
        st.write("Chat History")
        for i, (user_msg, moto_msg) in enumerate(reversed(st.session_state.chat_history), start=1):
            message(moto_msg, key=str(i))
            message(user_msg, is_user=True, key=f"{i}_user")
    chat_container.markdown("")


st.set_page_config(
    page_title="Ask-Moto | Friendly Assistant",
    page_icon="✅",
    layout="centered",
)
st.title("Ask-Moto")
initialize_chat_history()


with st.form(key='my_form', clear_on_submit=True):
    user_input = st.text_input("You: ", key="input")
    submit_button = st.form_submit_button(label='Submit')

    if submit_button and user_input:
        try:
            output = moto(user_input)
            st.session_state.chat_history.append((user_input, output))
            display_chat_history()
        except Exception as e:
            st.error(f"An error occurred: {e}")
