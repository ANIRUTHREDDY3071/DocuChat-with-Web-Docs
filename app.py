# Write your code here
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma 
from langchain.chat_models import init_chat_model 
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os 
import requests 

load_dotenv()

urls = [
    "https://docs.langchain.com/oss/python/integrations/document_loaders",
    "https://docs.langchain.com/oss/python/integrations/vectorstores",
    "https://docs.langchain.com/oss/python/integrations/text_embedding"
]

loader = WebBaseLoader(urls)

documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
  chunk_size=1000,      
  chunk_overlap=200, 
  add_start_index=True   
)


#Defining Huggingface model for embeddings
embedding_model = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-mpnet-base-v2"
)

#Defining vector database (chroma), for storing the embeddings
vector_store = Chroma(
    collection_name = "example_collection",
    embedding_function = embedding_model,
    persist_directory = "./chroma_langchain_db"
)


all_splits = text_splitter.split_documents(documents)
document_ids = vector_store.add_documents(documents=all_splits)
sample = vector_store.get(limit =1,include=["embeddings","documents"])


#initialising the model
api_key = os.getenv("GEMINI_API_KEY")
model = init_chat_model(
    "google_genai:gemini-2.5-flash",
    api_key = api_key,
)

def retrieve_context(query:str,k:int =2):
    # Complete the function to retrieve relevant context from the vector store based on a user query
    retrieved_docs =vector_store.similarity_search(query,k=k)
    context = "\n\n".join(
        doc.page_content
        for doc in retrieved_docs
    )

    source_docs = [
        doc.metadata
        for doc in retrieved_docs
    ]

    return context, source_docs

    


def ask_about_pdf(user_query):
    # Complete the function to answer user queries based on the retrieved context
    context,source_docs = retrieve_context(user_query,k=2)
    system_message = f"""You are a helpful AI assistant specialized in explaining LangChain documentation.

                            Use the following context extracted from the LangChain documentation webpages to answer the user's question:
                            {context}
                            INSTRUCTIONS:
                            1. Answer based ONLY on the provided context from the LangChain documentation.
                            2. Do NOT use outside knowledge beyond the documentation.
                            3. If the answer is not present in the context, say:
                                "This information is not available in the provided LangChain documentation context."
                            4. Use exact terminology, class names, method names, and concepts as described.
                            5. Keep explanations clear and technically accurate.
                            6. Mention specific modules, classes, or configuration options when relevant.
                            7. If code snippets are present, explain without modifying logic."""

    messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_query}
  ]

    response = model.invoke(messages)
    return {
    "answer": response.content,
    "source_documents": source_docs,
    "context_used": context
}

result = ask_about_pdf("How to use the HuggingFaceEmbeddings?")
print(result)
print(result["answer"])

# Print the results for each query