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


model_engine = "gpt-3.5-turbo-instruct"
chatbot_prompt = f"""
You are a conversational chatbot. Provide ONLY valuable information about Motopay. 
    Here is information about motopay: ``{contents}``. 
    REFRAIN from answering questions not related to the CONTEXT.
    Any deviation will not be tolerated.
    keep track of <conversation_history> and <user input> for reference.
    if <user input> is not related to CONTEXT, respond `Sorry i cannot help you with that information.


<conversation_history>
<user input>
"""

conversation_history = []
def get_response(conversation_history, user_input):
    prompt = chatbot_prompt.replace(
        "<conversation history>", "".join(conversation_history)).replace("<user input>", user_input)

    # Get the response from GPT-3
    response = openai.Completion.create(
            engine=model_engine, 
            prompt=prompt,
            n=2,
            temperature=0.5, 
            max_tokens = 1000
        )

    # Extract the response from the response object
    response_text = response["choices"][0]["text"]
    chatbot_response = response_text.strip()
    return chatbot_response


def moto(user_input):
    if len(conversation_history) > 7:
        conversation_history.pop(1)
    chatbot_response = get_response(conversation_history, user_input)
    conversation_history.append(f"{user_input}\n{chatbot_response}\n")
    return chatbot_response
