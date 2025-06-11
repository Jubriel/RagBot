# import os
import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import Document


def generate_context(document, chunk, llm):
    """
    Generate context for a specific chunk using the language model.
    """
    prompt = ChatPromptTemplate.from_template("""
    <document>
    {{WHOLE_DOCUMENT}}
    </document>
    Here is the chunk we want to situate within the whole document
    <chunk>
    {{CHUNK_CONTENT}}
    </chunk>
    Please give a short succinct context to situate this chunk within the
    overall document for the purposes of improving search retrieval of the
    chunk. Answer only with the succinct context and nothing else.

    """)
    messages = prompt.format_messages(WHOLE_DOCUMENT=document,
                                      CHUNK_CONTENT=chunk)
    response = llm.invoke(messages)
    return response.content


def generate_contextualized_chunks(chunks, document, llm):
    """
    Generate contextualized versions of the given chunks.
    """
    contextualized_chunks = []
    for chunk in chunks:
        context = generate_context(document, chunk.page_content, llm)
        contextualized_content = f"{context}\n\n{chunk.page_content}"
        contextualized_chunks.append(Document(
            page_content=contextualized_content, metadata=chunk.metadata))
    return contextualized_chunks


def contextual_chunking(documents, llm):
    """Splits documents into smaller chunks for better processing."""
    try:

        # Initialize the text splitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            # multithreaded=True
        )
        # Split the documents into chunks
        chunks = splitter.split_documents(documents)
        contexted = generate_contextualized_chunks(chunks, documents, llm)
        return contexted
    except Exception as e:
        logging.error(f"Error during contextual chunking: {e}")
        raise RuntimeError("Chunking failed.") from e
