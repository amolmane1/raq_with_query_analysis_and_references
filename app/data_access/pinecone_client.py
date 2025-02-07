from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.chains.query_constructor.schema import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from app.config import config
from app.data_access.openai import llm, embeddings

# Initialize Pinecone
pc = Pinecone(api_key=config.PINECONE_API_KEY)
index = pc.Index(config.PINECONE_INDEX_NAME)

# Get Pinecone Vector Store
pinecone_vectorstore = PineconeVectorStore(index=index, embedding=embeddings)

metadata_field_info = [
    AttributeInfo(
        name="year",
        description="The year the company report is for",
        type="integer",
    ),
    AttributeInfo(
        name="quarter",
        description="Which quarter the company's report is for (Q1, Q2, Q3, Q4)",
        type="string",
    ),
    AttributeInfo(
        name="company",
        description="The ticker symbol (eg. AAPL, NVDA, MSFT) of the company that released the report",
        type="string",
    ),
    AttributeInfo(
        name="section_title",
        description="The title of the (sub)section that the content belongs to",
        type="string",
    ),
        AttributeInfo(
        name="page_number",
        description="What page of the report the information is in",
        type="integer",
    ),
]

retriever = SelfQueryRetriever.from_llm(
    llm=llm,
    vectorstore=pinecone_vectorstore,
    document_contents="A snippet from a company's 10Q report.",
    metadata_field_info=metadata_field_info,
    enable_limit=True,
    verbose=True,
    search_kwargs={"k": 7}
)