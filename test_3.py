import os
import openai
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
_ = load_dotenv(find_dotenv())

# Set your OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']

# Load summarized contents
with open('Data/FAQ data.txt', 'r') as file:
    summaryG = file.read()
with open('Data/TPD data.txt', 'r') as file:
    summaryT = file.read()

model_engine = "gpt-3.5-turbo-instruct"
conversation_history = []
# Function to determine if the question is technical or general
def is_technical(question):
    # Example keywords for technical questions
    technical_keywords = ['Application', 'App'
    'Registration','Login','Otp','Internet Connectivity','Kyc','Transaction',
    'Pin','Two-Factor Authentication', 'Problem', 'Issues'
    'Payment','Wallet','Receipt','Bill Payment','Service Providers','QR Code','Loan','Credit Rating','Dispute Resolution','Profile Settings','Security','User ID','Verification','Connectivity Issues','System Error','Technical Support','Dashboard','Fund Transfer','ccount Balance','Notification','Data Privacy',]
    return any(keyword in question.title() for keyword in technical_keywords)

def get_response(conversation_history, user_input):
    # Decide if the input is technical or general
    content = summaryT if is_technical(user_input) else summaryG

    instruction = f'''
    You are a conversational chatbot focused on Motopay. 
    Provide concise, valuable information specifically about Motopay in no more than 40 words.
    Respond to inquiries about Motopay with concise information using simple terms. Here is the information: ``{content}``. 
    Refer to Support@motopayng.com for queries beyond this scope.
    '''
    
    prompt = instruction + "\n".join(conversation_history[-8:]) + f"{user_input}\n"

    # Get the response from GPT-3
    response = openai.completions.create(
        model=model_engine, 
        prompt=prompt,
        temperature=0.5, 
        max_tokens=500,
    )
    # Extract the response from the response object
    response_text = response.choices[0].text.strip()
    return response_text

def moto(user_input):
    global conversation_history
    chatbot_response = get_response(conversation_history, user_input)
    conversation_history.append(f"{user_input}\n{chatbot_response}\n")
    return chatbot_response
