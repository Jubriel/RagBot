import os
import openai
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
_ = load_dotenv(find_dotenv())

# Replace 'YOUR_API_KEY' with your actual OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']

# client = OpenAI(api_key= os.environ['OPENAI_API_KEY'])


# Load the predefined content
with open('FAQ.txt', 'r') as file:
    contents = file.read()


# Simplified system instruction for clarity and relevance
system_instruction = f'''You are an assistant. Provide ONLY concise and valuable information about Motopay within 40 words. 
                            REFRAIN from answering questions not related to this FOCUS,
                            Prioritize ``{contents}``.
                            STRICTLY answer ONLY questions related to the specified FOCUS.
                            Any deviation will not be tolerated.'''

conversations = [
    {'role': 'system', 'content': system_instruction}
]  # Initialize the conversation with the system instruction

def moto(query:str):
    # answer = ''
    conversations.append({'role': 'user', 'content': query})

    # Limit the conversations list to a maximum of 7 entries
    if len(conversations) > 7:
        # Remove the oldest conversations, but keep the system instruction at the beginning
        conversations.pop(1)

    response = openai.chat.completions.create(
        model= 'gpt-4',#,'gpt-3.5-turbo'
        messages=conversations,
        temperature = 0.5,
        max_tokens = 200,
        # stream = True
        ).choices[0].message.content

    # for event in response: 
    #     # STREAM THE ANSWER
    #     print(event.choices[0].delta.content or "")
    #     # print(answer, end='', flush=True) # Print the response    
    #     # event_text = event['choices'][0]['delta']
    #     # answer = event_text.get('content', '')
        
    conversations.append({'role': 'assistant', 'name': 'AskMoto', 'content': response})
    
    return response
