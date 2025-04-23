import os
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferWindowMemory, ChatMessageHistory
from langchain_core.prompts import (ChatPromptTemplate, MessagesPlaceholder,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.agents import tool, create_tool_calling_agent, AgentExecutor
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain_azure_ai.embeddings import AzureAIEmbeddingsModel

# Load environment variables
load_dotenv()


# from langchain
import asyncio
import nest_asyncio
nest_asyncio.apply()

load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
# loading AI models

llm = AzureAIChatCompletionsModel(
    model_name="Llama-3.3-70B-Instruct",
    endpoint=endpoint,
    max_tokens=500,
    # api_version="2024-05-01-preview",
)
embed = AzureAIEmbeddingsModel(
    model_name="text-embedding-ada-002"
    )

# File path for persistent FAISS index
FAISS_PATH = "hermex_faiss_index"

# URLs to load
page_urls = [
    "https://hermextravels.com/",
    "https://hermextravels.com/features.html",
    "https://hermextravels.com/contact.html",
    "https://hermextravels.com/investors.html",
    "https://hermextravels.com/investors.html#investment-tiers"
]


# Setup or load FAISS vectorstore
def setup_vectorstore():
    if os.path.exists(FAISS_PATH):
        print("🔁 Loading FAISS index from disk...")
        return FAISS.load_local(FAISS_PATH, embed,
                                allow_dangerous_deserialization=True)
    else:
        print("🔨 Creating FAISS index from webpages...")
        # Load from web
        web_loader = WebBaseLoader(web_paths=page_urls)
        web_docs = web_loader.load()

        # Load from text file
        text_loader = TextLoader("hermex.txt", encoding="utf-8")
        text_docs = text_loader.load()

        # Combine both document sets
        all_docs = web_docs + text_docs
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                  chunk_overlap=200)
        chunks = splitter.split_documents(all_docs)
        vectorstore = FAISS.from_documents(chunks, embed)
        vectorstore.save_local(FAISS_PATH)
    return vectorstore


class HermexAssistant:
    def __init__(self, streaming: bool = True):
        self.llm = llm
        self.embedding_model = embed
        self.streaming = streaming
        self.user_sessions: dict[str, ChatMessageHistory] = {}
        self.retrieved = setup_vectorstore().as_retriever(search_kwargs={
            "k": 2,
        })

        self.instructions = """
            You are Hera, a professional and efficient travel assistant for
            Hermex Travels.Your purpose is to provide accurate, concise, and
            helpful answers strictly based on the provided context. Avoid
            speculation and only provide facts relevant to Hermex services
            and the travel/tourism industry. You functionality is not limited 
            to connecting to live agents, budget planning, translator.
            Act Human-like.

            Translator: This feature will enable real-time translation to
            facilitate communication across different languages, enhancing
            user interactions.
            
            Budget Planner: Users will be able to create and manage their
            budgets, making it easier to plan for trips and activities based
            on their financial preferences.
            
            Weather Monitor: This feature will provide up-to-date weather
            information, allowing users to plan their activities according to
            current and forecasted weather conditions.
            
            Activity Matcher: Users can receive suggestions for activities
            tailored to their interests and preferences, ensuring a more
            personalized experience.
            
            Destination Suggester: This feature will offer recommendations for
            travel destinations based on user inputs, helping them find the
            perfect place to visit.

            Use the following context to answer the user's question.
            If the answer is not in the context, reply with:
            "I'm sorry, I can not provide such information at the moment."

            """

        prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(self.instructions),
                # The `variable_name` here is what must align with memory
                MessagesPlaceholder("chat_history"),
                HumanMessagePromptTemplate.from_template("{input}"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )

        # Define tool
        @tool(response_format="content")
        def retrieve(query: str):
            """
            Retrieve information related to a query to provide and
            informative response.
            """
            content = self.retrieved.invoke(query)
            return content

        # Define tools
        @tool(response_format="content")
        def ip_address() -> str:
            """
            Retrieve IP-address information of the user
            """
            from requests import get

            ip = get('https://api.ipify.org').text
            return ip

        def date_time():
            """
            Retrieve current day, date, and time in a readable format
            """
            from datetime import datetime

            now = datetime.now()
            return now.strftime("%A, %Y-%m-%d %H:%M:%S")
        
        @tool(response_format="content")
        def live_agent():
            """
            Helps the user to connect with a live agent
            """
            time = date_time()
            location = ip_address()
            print(
                f"User connected to live agent at {time} from IP: {location}"
                  )
            return "Please wait while we connect you to a live agent."

        self.conversational_memory = ConversationBufferWindowMemory(
            memory_key='chat_history',
            k=5,
            return_messages=True
        )

        self.agent_executor = AgentExecutor(
            agent=create_tool_calling_agent(self.llm, [retrieve,
                                                       live_agent], prompt),
            tools=[retrieve, live_agent],
            memory=self.conversational_memory,
            # verbose=True,
        )

    def chat(self, user_id: str, query: str) -> str:
        """Handles chat with a specific user session."""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = ChatMessageHistory()

        self.conversational_memory.chat_memory = self.user_sessions[user_id]

        self.user_sessions[user_id].add_user_message(query)
        response = self.agent_executor.invoke(
            {'input': query,
             "chat_history": self.user_sessions[user_id].messages})
        
        self.user_sessions[user_id].add_ai_message(response['output'])
        return response['output']

    def load_history(self, user_id: str) -> list:
        """Returns user's conversation history or initializes it if missing."""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = ChatMessageHistory()
        return self.user_sessions[user_id].messages

    def clear_chat_history(self, user_id: str):
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]
            return True
        return False
