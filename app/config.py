from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = "kraken-rag-takehome"

config = Config()