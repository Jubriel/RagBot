import os
import openai
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
_ = load_dotenv(find_dotenv())

# Replace 'YOUR_API_KEY' with your actual OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']

# Load the predefined content
with open('FAQ.txt', 'r') as file:
    contents = file.read()


# Simplified system instruction for clarity and relevance
system_instruction = f'''You are an assistant. Provide ONLY short and valuable information about Motopay within 40 words. 
                            REFRAIN from answering questions not related to this FOCUS,
                            Prioritize ``{contents}``.
                            STRICTLY answer ONLY questions related to the specified FOCUS.
                            Any deviation will not be tolerated.'''

conversations = [
    {'role': 'system', 'content': system_instruction}
]  # Initialize the conversation with the system instruction

# def moto(query:str):
#     answer = ''
#     conversations.append({'role': 'user', 'content': query})

#     response = openai.ChatCompletion.create(
#         model='gpt-3.5-turbo',
#         messages=conversations,
#         max_tokens = 200,
#         stream = True,
#         )3E
#     # ['choices'][0]['message']['content']

#     for event in response: 
#         # STREAM THE ANSWER
#         print(answer, end='', flush=True) # Print the response    
#         event_text = event['choices'][0]['delta']
#         answer = event_text.get('content', '')
            
#     conversations.append({'role': 'assistant', 'name': 'Hannah', 'content': answer})
#     return answer
#         print('\n')


def moto(query:str):
    
    conversations.append({'role': 'user', 'content': query})

    # Limit the conversations list to a maximum of 7 entries
    if len(conversations) > 7:
        # Remove the oldest conversations, but keep the system instruction at the beginning
        conversations.pop(1)

    response = openai.ChatCompletion.create(
        model= 'gpt-4',#,'gpt-3.5-turbo'
        messages=conversations,
        temperature = 0.5,
        max_tokens = 200,

        )['choices'][0]['message']['content']

    conversations.append({'role': 'assistant', 'name': 'AskMoto', 'content': response})
    
    return response




# model_engine = "text-davinci-003"
# chatbot_prompt = f"""
# You are an assistant. Provide ONLY short and valuable information about Motopay within 40 words. 
#                             REFRAIN from answering questions not related to this FOCUS,
#                             Prioritize ``{contents}``. 
#                             if question is not related to `contents` return "Not Related",
#                             STRICTLY answer ONLY questions related to the specified FOCUS.
#                             Any deviation will not be tolerated.'''


# <conversation_history>
# User: <user input>
# Hannah:"""

# conversation_history = []
# def get_response(conversation_history, user_input):
#     prompt = chatbot_prompt.replace(
#         "<conversation history>", "".join(conversation_history)).replace("<user input>", user_input)

#     # Get the response from GPT-3
#     response = openai.Completion.create(
#         engine=model_engine, prompt=prompt, max_tokens=2048, n=2, stop=None, temperature=0.5)

#     # Extract the response from the response object
#     response_text = response["choices"][0]["text"]

#     chatbot_response = response_text.strip()

#     return chatbot_response


# def main(user_input):
#     chatbot_response = get_response(conversation_history, user_input)
#     conversation_history.append(f"User: {user_input}\nHannah: {chatbot_response}\n")
#     print(len(conversation_history))
#     return f"Hannah: {chatbot_response}"
