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
from langchain import hub
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()

# Models
llm = ChatOllama(model='qwen2:latest', temperature=0)
embed = OllamaEmbeddings(model='mxbai-embed-large:latest')import os
import logging
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
from langchain.chains import RetrievalQA

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Models
llm = ChatOllama(model='qwen2:latest', temperature=0)
embed = OllamaEmbeddings(model='mxbai-embed-large:latest')

# FAISS path
FAISS_PATH = "hermex_faiss_index"

# URLs to load
page_urls = [
    "https://hermextravels.com/",
    "https://hermextravels.com/features.html",
    "https://hermextravels.com/contact.html",
    "https://hermextravels.com/investors.html",
    "https://hermextravels.com/investors.html#investment-tiers"
]

def setup_vectorstore():
    try:
        if os.path.exists(FAISS_PATH):
            logging.info("🔁 Loading FAISS index from disk...")
            return FAISS.load_local(FAISS_PATH, embed, 
                                    allow_dangerous_deserialization=True)
        else:
            logging.info("🔨 Creating FAISS index from webpages...")

            web_loader = WebBaseLoader(web_paths=page_urls)
            web_docs = web_loader.load()

            text_loader = TextLoader("hermex.txt", encoding="utf-8")
            text_docs = text_loader.load()

            all_docs = web_docs + text_docs
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, 
                                                      chunk_overlap=200, 
                                                      multithreaded=True)
            chunks = splitter.split_documents(all_docs)

            vectorstore = FAISS.from_documents(chunks, embed)
            vectorstore.save_local(FAISS_PATH)
            logging.info("✅ FAISS index created and saved.")
            return vectorstore
    except Exception as e:
        logging.error(f"Error setting up vectorstore: {e}")
        raise RuntimeError("Vectorstore setup failed.") from e


class HermexAssistant:
    def __init__(self):
        try:
            self.llm = llm
            self.embedding_model = embed
            self.user_sessions: dict[str, ChatMessageHistory] = {}
            self.vectorstore = setup_vectorstore()

            self.instructions = """
                You are Hera, a professional and efficient travel assistant for 
                Hermex Travels. Your purpose is to provide accurate, concise, and 
                helpful answers strictly based on the provided context.
                Avoid speculation and only provide facts relevant to Hermex services
                and the travel/tourism industry.

                Use the following context to answer the user's question. 
                If the answer is not in the context, reply with:
                "I'm sorry, I can not provide such information at the moment."
            """

            prompt = ChatPromptTemplate(
                messages=[
                    SystemMessagePromptTemplate.from_template(self.instructions),
                    MessagesPlaceholder("chat_history"),
                    HumanMessagePromptTemplate.from_template("{input}"),
                    MessagesPlaceholder("agent_scratchpad"),
                ]
            )

            # Define tools
            @tool(response_format="content_and_artifact")
            def retrieve():
                """Retrieve information related to a query to 
                provide an informative response."""
                try:
                    return self.vectorstore.as_retriever(search_kwargs={"k": 2}), \
                            self.conversational_memory.chat_memory
                except Exception as e:
                    logging.error(f"Error during retrieval: {e}")
                    return "Retrieval failed."

            @tool(response_format="content")
            def ip_address():
                """Retrieve IP-address information of the user"""
                try:
                    from requests import get
                    return get('https://api.ipify.org').text
                except Exception as e:
                    logging.error(f"Error fetching IP address: {e}")
                    return "Could not retrieve IP address."

            @tool(response_format="content")
            def date_time():
                """Retrieve current day, date, and time in a readable format"""
                try:
                    from datetime import datetime
                    now = datetime.now()
                    return now.strftime("%A, %Y-%m-%d %H:%M:%S")
                except Exception as e:
                    logging.error(f"Error getting date and time: {e}")
                    return "Could not retrieve date/time."

            self.conversational_memory = ConversationBufferWindowMemory(
                memory_key='chat_history',
                k=5,
                return_messages=True
            )

            self.agent_executor = AgentExecutor(
                agent=create_tool_calling_agent(self.llm, [retrieve, 
                                                           date_time, 
                                                           ip_address], prompt),
                tools=[retrieve, date_time, ip_address],
                memory=self.conversational_memory,
                # verbose=True,
            )
            logging.info("🤖 HermexAssistant initialized successfully.")

        except Exception as e:
            logging.critical(f"Failed to initialize HermexAssistant: {e}")
            raise

    def chat(self, user_id: str, query: str) -> str:
        """Handles chat with a specific user session."""
        try:
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = ChatMessageHistory()

            self.conversational_memory.chat_memory = self.user_sessions[user_id]
            self.user_sessions[user_id].add_user_message(query)

            response = self.agent_executor.invoke({'input': query})
            output = response.get('output', 
                                  "I'm sorry, I couldn't generate a response.")
            self.user_sessions[user_id].add_ai_message(output)
            return output

        except Exception as e:
            logging.error(f"Chat error for user {user_id}: {e}")
            return "Something went wrong. Please try again later."

    def load_history(self, user_id: str) -> list:
        """Returns user's conversation history or initializes it if missing."""
        try:
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = ChatMessageHistory()
            return self.user_sessions[user_id].messages
        except Exception as e:
            logging.error(f"Error loading history for user {user_id}: {e}")
            return []

    def clear_chat_history(self, user_id: str):
        try:
            if user_id in self.user_sessions:
                del self.user_sessions[user_id]
                logging.info(f"Cleared chat history for user {user_id}")
                return True
            return False
        except Exception as e:
            logging.error(f"Error clearing chat history for user {user_id}: {e}")
            return False


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
                                                  chunk_overlap=200,
                                                  multithreaded=True)
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
        self.vectorstore = setup_vectorstore()
        # self.qa_chain = self._setup_qa_chain()

        self.instructions = """
            You are Hera, a professional and efficient travel assistant for
            Hermex Travels.Your purpose is to provide accurate, concise, and
            helpful answers strictly based on the provided context. Avoid
            speculation and only provide facts relevant to Hermex services
            and the travel/tourism industry.

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
        @tool(response_format="content_and_artifact")
        def retrieve():
            """
            Retrieve information related to a query to provide and 
            informative response.
            """
            retrieved = self.vectorstore.as_retriever(search_kwargs={"k": 2})
            return retrieved, self.conversational_memory.chat_memory

        # Define tools
        @tool(response_format="content")
        def ip_address() -> str:
            """
            Retrieve IP-address information of the user
            """
            from requests import get

            ip = get('https://api.ipify.org').text
            return ip

        # Define tools
        @tool(response_format="content")
        def date_time():
            """
            Retrieve current day, date, and time in a readable format
            """
            from datetime import datetime

            now = datetime.now()
            return now.strftime("%A, %Y-%m-%d %H:%M:%S")

        self.conversational_memory = ConversationBufferWindowMemory(
            memory_key='chat_history',
            k=5,
            return_messages=True
        )

        self.agent_executor = AgentExecutor(
            agent=create_tool_calling_agent(self.llm, [retrieve,
                                                       date_time,
                                                       ip_address], prompt),
            tools=[retrieve, date_time, ip_address],
            memory=self.conversational_memory,
            # verbose=True,
        )

    def chat(self, user_id: str, query: str) -> str:
        """Handles chat with a specific user session."""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = ChatMessageHistory()

        self.conversational_memory.chat_memory = self.user_sessions[user_id]

        self.user_sessions[user_id].add_user_message(query)
        response = self.agent_executor.invoke({'input': query})
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
