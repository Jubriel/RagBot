import os
import openai
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
_ = load_dotenv(find_dotenv())

# Replace 'YOUR_API_KEY' with your actual OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']

# Load the predefined content for English
with open('FAQ.txt', 'r') as file:
    contentE = file.read()
# # Load the predefined content for Pidgin
# with open('FAQ-Pid.txt', 'r') as file:
#     contentP = file.read()

model_engine = "gpt-3.5-turbo-instruct"
chatbot_prompt = f"""
instruction = '''
    You are a conversational chatbot focused on Motopay. Provide concise, valuable information specifically about Motopay in no more than 40 words. 
    Use simple terms. Here is the information: ``{contentE}``. 
    Strictly adhere to the context; avoid answering off-topic queries. 
    Deviating from these guidelines should result in a non-response or a reminder to stay on topic.
    Respond in SIMPLIFIED terms.
    Refer users to ``Support@motopayng.com`` ONLY when a query is beyond the scope of provided information or if an immediate answer isn't available.
'''


<conversation_history>
<user input>
"""
 
conversation_history = []
def get_response(conversation_history, user_input):
    prompt = chatbot_prompt.replace(
        "<conversation history>", "".join(conversation_history)).replace("<user input>", user_input)

    # Get the response from GPT-3
    response = openai.completions.create(
            model=model_engine, 
            prompt=prompt,
            temperature=0.5, 
            max_tokens = 2000,
        )
    # Extract the response from the response object
    response_text = response.choices[0].text.strip()
    return response_text

# def translate(text, target_language): 
#     response = openai.completions.create(
#         model= "text-davinci-003", 
#         prompt=f"Translate the text into {target_language}: {text}\n", 
#         max_tokens = 2000,  
#         temperature = 0.5, 
#     ) 
#     return response.choices[0].text.strip()


def moto(user_input): #, target_language
    # global chatbot_prompt, contentE, contentP
    if len(conversation_history) > 7:
        conversation_history.pop(1)
    # if target_language != 'English':
    #     chatbot_prompt = chatbot_prompt.replace('``content``','``{contentP}``' )
    #     chatbot_response = get_response(conversation_history, user_input)
    # else:
        # chatbot_prompt = chatbot_prompt.replace('``content``','``{contentE}``' )
    chatbot_response = get_response(conversation_history, user_input)

    conversation_history.append(f"{user_input}\n{chatbot_response}\n")
    return chatbot_response
