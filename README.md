# 📚 DocuChat with Web Docs

An AI-powered documentation assistant built with **LangChain, Gemini, Hugging Face Embeddings, and ChromaDB**.

This project loads multiple LangChain documentation webpages, converts the content into searchable vector embeddings, and allows an AI model to answer questions using only the retrieved documentation context.

---

## 🚀 Project Overview

Finding specific information in technical documentation can be time-consuming, especially when working with multiple pages.

**DocuChat with Web Docs** solves this by creating a Retrieval-Augmented Generation (RAG) workflow:

```text
LangChain Documentation
        ↓
    WebBaseLoader
        ↓
   Document Loading
        ↓
RecursiveCharacterTextSplitter
        ↓
    Text Chunks
        ↓
HuggingFaceEmbeddings
        ↓
   Vector Embeddings
        ↓
      Chroma
        ↓
   Similarity Search
        ↓
 Retrieved Context
        ↓
    Gemini LLM
        ↓
    Final Answer
```

The AI is instructed to answer questions **strictly using the retrieved LangChain documentation context**.

---

## ✨ Features

- 🌐 Load multiple LangChain documentation webpages
- ✂️ Split documents into manageable chunks
- 🧠 Generate embeddings using Hugging Face
- 🗄️ Store embeddings in Chroma vector database
- 🔎 Perform similarity-based document retrieval
- 🤖 Use Gemini for context-aware question answering
- 📖 Provide source documents and retrieved context
- 🚫 Prevent answers based on information outside the provided documentation

---

## 🛠️ Technologies Used

- **Python**
- **LangChain**
- **Google Gemini**
- **WebBaseLoader**
- **RecursiveCharacterTextSplitter**
- **HuggingFaceEmbeddings**
- **Chroma**
- **python-dotenv**

---

## 📂 Documentation Sources

The application loads the following LangChain documentation pages:

```text
https://docs.langchain.com/oss/python/integrations/document_loaders

https://docs.langchain.com/oss/python/integrations/vectorstores

https://docs.langchain.com/oss/python/integrations/text_embedding
```

---

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/DocuChatWithWebDocs.git

cd DocuChatWithWebDocs
```

### 2. Install Dependencies

Install the required packages:

```bash
pip install langchain
pip install langchain-community
pip install langchain-huggingface
pip install langchain-chroma
pip install langchain-text-splitters
pip install google-genai
pip install python-dotenv
pip install sentence-transformers
```

Or install them using:

```bash
pip install -r requirements.txt
```

---

## 🔐 Configure Gemini API

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY="your_api_key_here"
```

The application loads the API key using:

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
```

---

## 🧠 Embedding Model

The project uses:

```text
sentence-transformers/all-mpnet-base-v2
```

through:

```python
HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
```

The embedding model converts document chunks into numerical vector representations that can be searched based on semantic similarity.

---

## 🗄️ Chroma Vector Database

The generated embeddings and document chunks are stored in a Chroma vector store.

The vector database enables the application to retrieve documentation that is semantically relevant to a user's question.

---

## 🔎 Retrieval Process

The `retrieve_context()` function performs similarity search against the Chroma vector store.

The retrieved documents are combined into a context that is passed to Gemini.

Conceptually:

```text
User Question
      ↓
Similarity Search
      ↓
Relevant Documentation
      ↓
Context Construction
      ↓
Gemini
      ↓
Answer
```

---

## 🤖 AI Question Answering

The `ask_about_pdf()` function:

1. Receives a user question.
2. Retrieves relevant documentation.
3. Constructs a system message containing the retrieved context.
4. Instructs Gemini to answer only from that context.
5. Invokes the Gemini model.
6. Returns:
   - Answer
   - Source documents
   - Context used

---

## 📌 System Instruction

The AI assistant follows this core instruction:

```text
You are a helpful AI assistant specialized in explaining LangChain documentation.

Use the following context extracted from the LangChain documentation webpages to answer the user's question.

INSTRUCTIONS:

1. Answer based ONLY on the provided context from the LangChain documentation.
2. Do NOT use outside knowledge beyond the documentation.
3. If the answer is not present in the context, say:

"This information is not available in the provided LangChain documentation context."
```

This helps keep the generated answers grounded in the retrieved documentation.

---

## 🧪 Example Queries

The project evaluates the documentation assistant using these questions:

### Query 1

```text
How to use the HuggingFaceEmbeddings?
```

### Query 2

```text
Explain the use this value : sentence-transformers/all-mpnet-base-v2
```

### Query 3

```text
How to use Open AI Embeddings
```

### Query 4

```text
Explain about this: OpenAIEmbeddings
```

The answers generated by Gemini are printed to the console.

---

## ▶️ Run the Project

Run:

```bash
python app.py
```

The application will:

1. Load the environment variables.
2. Load the LangChain documentation.
3. Split the webpages into chunks.
4. Generate embeddings.
5. Store the embeddings in Chroma.
6. Retrieve relevant documentation.
7. Send the retrieved context to Gemini.
8. Print answers for all four example queries.

---

## 📊 RAG Architecture

```text
                 ┌───────────────────────┐
                 │ LangChain Web Docs    │
                 └───────────┬───────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ WebBaseLoader   │
                    └────────┬────────┘
                             │
                             ▼
              ┌────────────────────────────┐
              │ RecursiveCharacterText     │
              │ Splitter                   │
              └─────────────┬──────────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ HuggingFace       │
                  │ Embeddings        │
                  └─────────┬─────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │   Chroma     │
                    │ Vector Store │
                    └───────┬──────┘
                            │
                    Similarity Search
                            │
                            ▼
                   ┌────────────────┐
                   │ Retrieved      │
                   │ Context        │
                   └───────┬────────┘
                           │
                           ▼
                   ┌────────────────┐
                   │ Gemini Model   │
                   └───────┬────────┘
                           │
                           ▼
                     Final Answer
```

---

## 📁 Project Structure

```text
DocuChatWithWebDocs/
│
├── app.py
├── .env
├── requirements.txt
├── chroma_langchain_db/
└── README.md
```

> Add `.env` and local database/cache directories to `.gitignore` before pushing the project to GitHub.

---

## 🔮 Future Enhancements

- 💬 Add an interactive chat interface
- 🌐 Allow users to provide their own URLs
- 📄 Support PDF and document uploads
- 🔍 Improve retrieval with hybrid search
- 📊 Add RAG evaluation metrics
- 🧠 Add conversation memory
- ⚡ Add streaming responses
- 🔐 Add authentication for multi-user applications

---

## 🎯 Key Learning Outcomes

Through this project, I gained practical experience in:

- Building a RAG pipeline with LangChain
- Loading and processing web documentation
- Document chunking and metadata handling
- Creating semantic embeddings
- Working with vector databases
- Performing similarity search
- Integrating Gemini with LangChain
- Grounding LLM responses using retrieved context

---

## 👨‍💻 Author

**Aniruth Reddy Devarapelly**

AI/ML | Generative AI | Data Science

GitHub: `https://github.com/ANIRUTHREDDY3071`

---

## ⭐ Support

If you found this project useful, consider giving the repository a ⭐ on GitHub.
