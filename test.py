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
system_instruction = f'''You are a friendly assistant.Your role is to provide valuable information about Motopay. 
                        "ONLY ANSWER QUESTION RELATED TO THE FOCUS, REFRAIN FROM UNRELATED QUESTIONS." 
                        Respond with maximum of 40 words.
                        "DO NOT answer any question or conversation not related to CONTEXT".
                        Prioritize this ``{contents}.`` '''

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
        model= 'gpt-4',#,'gpt-3.5-turbo-instruct'
        messages=conversations,
        max_tokens = 200,

        )['choices'][0]['message']['content']

    conversations.append({'role': 'assistant', 'name': 'AskMoto', 'content': response})
    
    return response