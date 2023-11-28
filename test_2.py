import os
import openai
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
_ = load_dotenv(find_dotenv())

# Replace 'YOUR_API_KEY' with your actual OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']

# Load the predefined contents
# General
with open('Data/FAQ data.txt', 'r') as file:
    contentG = file.read()
# Technical
with open('Data/TPD data.txt', 'r') as file:
    contentT = file.read()

model_engine = "gpt-3.5-turbo-instruct"
chatbot_prompt = f"""
instruction = '''
    You are a conversational chatbot focused on Motopay. 
    Provide concise, valuable information specifically about Motopay in no more than 40 words. 
    Use simple terms. Here is the information: general ``{contentG}`` and technical ``{contentT}``. 
    Strictly adhere to the context; avoid answering off-topic queries.
    Keep track of conversation_history for reference.
    Respond in SIMPLIFIED terms.
    Refer users to ``Support@motopayng.com`` ONLY when a query is beyond the scope of provided information or 
    if an immediate answer isn't available.
'''
"""

conversation_history = []
def get_response(conversation_history, user_input):
    prompt = chatbot_prompt + "\n".join(conversation_history) + f"{user_input}\n"

    # Get the response from GPT-3
    response = openai.completions.create(
            model=model_engine, 
            prompt=prompt,
            temperature=0.5, 
            max_tokens = 200,
        )
    # Extract the response from the response object
    response_text = response.choices[0].text.strip()
    return response_text


def moto(user_input): #, target_language
    global conversation_history
    if len(conversation_history) > 7:
        conversation_history.pop(1)
    chatbot_response = get_response(conversation_history, user_input)
    conversation_history.append(f"{user_input}\n{chatbot_response}\n")
    return chatbot_response
