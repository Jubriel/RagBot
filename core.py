# type:ignore
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
from typing import Dict
from langchain_community.document_loaders import (WebBaseLoader,
                                                  UnstructuredPDFLoader)
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain.memory import ConversationBufferWindowMemory, ChatMessageHistory

from langchain_core.prompts import (
    ChatPromptTemplate, MessagesPlaceholder,
    HumanMessagePromptTemplate, SystemMessagePromptTemplate
)
from langchain.agents import tool, create_tool_calling_agent, AgentExecutor
from contextual import contextual_chunking
from config import config, SYSTEM_INSTRUCTIONS, PAGE_URLS


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment
load_dotenv()

# Models
try:
    logger.info("Loading models...")
    # Load models
    llm = ChatOllama(model=config.LLM_MODEL,
                     base_url=config.OLLAMA_HOST)
    embed = OllamaEmbeddings(model=config.EMBED_MODEL,
                             base_url=config.OLLAMA_HOST)
except Exception as e:
    logger.error(f"Error loading models: {e}")
    raise RuntimeError("Failed to load models. Check OLLAMA_HOST or model \
                        names.")
# FAISS store
FAISS_PATH = "digit_index"


class VectorStoreManager:
    def __init__(self, embed_model):
        self.embed = embed_model

    def setup_vectorstore(self):
        try:
            if os.path.exists(FAISS_PATH):
                logger.info("🔁 Loading FAISS index from disk...")
                return FAISS.load_local(FAISS_PATH, self.embed,
                                        allow_dangerous_deserialization=True)

            logger.info("🔨 Creating FAISS index from web & Excel documents...")
            web_docs = WebBaseLoader(web_paths=PAGE_URLS).load()
            pdf_docs = UnstructuredPDFLoader("orwellanimalfarm.pdf",
                                             mode="elements").load()
            all_docs = web_docs + pdf_docs

            chunks = contextual_chunking(all_docs, llm)
            vectorstore = FAISS.from_documents(chunks, self.embed)
            vectorstore.save_local(FAISS_PATH)
            logger.info("✅ FAISS index created and saved.")
            return vectorstore

        except Exception as e:
            logger.error(f"Error setting up vectorstore: {e}")
            raise RuntimeError("Vectorstore setup failed.") from e


# Tools
@tool(response_format="content")
def retrieve(retriever, query: str) -> str:
    """
    This tool is used to retrieve top most relevant documents from the
    vectorstore. This is based on the query.
    It takes the retriever and query as input,
    Args:
        retriever (_type_): the retriever object to use for document retrieval
        query (str): the query string to search for in the vectorstore
    Returns:
        str: the content of the most relevant documents
    """
    try:
        results = retriever.invoke(query)
        return "\n\n".join([doc.page_content for doc in results])
    except Exception as e:
        logger.error(f"Retrieve tool failed: {e}")
        return "Failed to retrieve relevant results."


def date_time() -> str:
    return datetime.now().strftime("%A, %Y-%m-%d %H:%M:%S")


def get_metadata(history: list) -> str:
    """
    This function generates metadata tags and priority based on the
    conversation history. It uses a language model to analyze the conversation
    and generate tags and priority.
    Args:
        history (list): conversation history

    Returns:
        str: metadata tags and priority
    """
    tag_list = ['loan', 'credit', 'business', 'personal', 'investment',
                'sme', 'login', 'signup']
    priority_list = ['high', 'medium', 'low']
    prompt = (
        f"Given the following conversation history:\n{history}\n\n"
        f"Choose one tag from {tag_list} and one priority from {priority_list}"
        f"based on its severity and user urgency. "
        f"Respond in the format: tag:<tag>, priority:<priority>"
    )
    try:
        result = llm.invoke(prompt)
        return result['content']
    except Exception as e:
        logger.warning(f"Metadata tagging failed: {e}")
        return "tag:unknown, priority:low"


def get_summary(history: list) -> str:
    prompt = (
        f"Given the following conversation history:\n{history}\n\n"
        f"Summarize this conversation in a single sentence."
    )
    try:
        result = llm.invoke(prompt)
        return result['content']
    except Exception as e:
        logger.warning(f"Summary generation failed: {e}")
        return "Summary unavailable."


class StoryTeller:
    def __init__(self):
        self.llm = llm
        self.embedding_model = embed
        self.user_sessions: Dict[str, ChatMessageHistory] = {}

        self.vectorstore = (
            VectorStoreManager(self.embedding_model)
            .setup_vectorstore()
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})

        self.instructions = SYSTEM_INSTRUCTIONS

        prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(self.instructions),
                MessagesPlaceholder("chat_history"),
                HumanMessagePromptTemplate.from_template("{input}"),
                MessagesPlaceholder("current_time", default=date_time),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )

        self.conversational_memory = ConversationBufferWindowMemory(
            memory_key='chat_history',
            k=4,
            return_messages=True
        )

        self.agent_executor = AgentExecutor(
            agent=create_tool_calling_agent(self.llm,
                                            [retrieve],
                                            prompt),
            tools=[retrieve],
            memory=self.conversational_memory,
        )

    def chat(self, user_id: str, query: str) -> str:
        try:
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = ChatMessageHistory()

            self.conversational_memory.chat_memory.messages = (
                self.user_sessions[user_id].messages
                )
            self.user_sessions[user_id].add_user_message(query)

            response = self.agent_executor.invoke({
                'input': query,
                'chat_history': self.conversational_memory.chat_memory.messages
            })

            self.user_sessions[user_id].add_ai_message(response['output'])
            return response['output']

        except Exception as e:
            logger.error(f"Chat error for user {user_id}: {e}")
            return "Sorry, an error occurred while processing your request."

    def load_history(self, user_id: str):
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = ChatMessageHistory()
        return self.user_sessions[user_id].messages

    def clear_chat_history(self, user_id: str):
        removed = self.user_sessions.pop(user_id, None)
        return removed is not None
