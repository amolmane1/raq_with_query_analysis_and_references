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
