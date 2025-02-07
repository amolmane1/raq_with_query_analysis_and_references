# RAG with Query Analysis and References

This app allows users to ask questions about a company's 10Q.

- 10Q data was parsed from PDFs
- I used a Self query retriever to to infer metadata filters (like year, quarter,
  company, page number, and section title) (query analysis) from the user's
  question to pre-filter the vectorstore embeddings
- I used structured outputs with the generator to make it give references for the
  answer.

Tools/Stack:

- Pinecone vectorstore
- Langgraph object with a retriever node and a generator node
- Run in a FastAPI server
- OpenAI gpt-4o and embeddings-large-3 models
- Unstructured.io for parsing PDFs

# Installation instructions

- Add API keys for OpenAI, Langchain, [Unstructured](https://unstructured.io/) and Pinecone into a `.env` file at the same level as the `app` folder

```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY="your key here"
OPENAI_API_KEY="your key here"
UNSTRUCTURED_API_KEY="your key here"
PINECONE_API_KEY="your key here"
```

- Install dependencies

```
pip install -r requirements.txt
```

- Install other dependencies outside of pip

```
brew install libmagic poppler tesseract qpdf
```

- Paste all the pdf documents into the `/docs` folder.
- Run the script to parse the pdfs and create the vectorstore

```
python preprocessing/create_vectorstore.py
```

- run the FastAPI server

```
fastapi dev app/main.py
```

Send POST requests to use solution:

```
curl -X POST http://localhost:8000/api/query \
     -H "Content-Type: application/json" \
     -d '{"question": "who is msft CEO?"}'
```
