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
system_instruction = f'''You are a conversational chatbot focused on Motopay. Provide concise, valuable information specifically about Motopay in no more than 40 words. 
    Use simple terms. Here is the information: ``{contents}``. 
    Strictly adhere to the context; avoid answering off-topic queries. 
    Deviating from these guidelines should result in a non-response or a reminder to stay on topic.
    keep track of <conversation_history> and <User> for reference.
    Respond in SIMPLIFIED terms.
    Refer users to ``Support@motopayng.com`` ONLY when a query is beyond the scope of provided information or if an immediate answer isn't available.'''

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
        model= 'gpt-3.5-turbo',
        messages=conversations,
        temperature = 0.5,
        max_tokens = 200,
        # stream = True
        ).choices[0].message.content

        
    conversations.append({'role': 'assistant', 'name': 'AskMoto', 'content': response})
    
    return response
