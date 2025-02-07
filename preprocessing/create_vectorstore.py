from dotenv import load_dotenv
import os
from langchain_unstructured import UnstructuredLoader
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec


# Load the .env file
load_dotenv()
pinecone_api_key = os.environ["PINECONE_API_KEY"]
pc = Pinecone(api_key=pinecone_api_key)
index_name = "kraken-rag-takehome"

# create new index
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )


## parse pdfs
print("Parsing PDFs")
dir_path = "../docs/"
file_paths = os.listdir(dir_path)
all_docs = []

for file_path in file_paths:
    print(file_path)
    loader = UnstructuredLoader(
        file_path=dir_path + file_path,
        strategy="hi_res",
        partition_via_api=True,
        coordinates=True,
    )

    file_docs = []
    for doc in loader.lazy_load():
        file_docs.append(doc)
    
    print(len(file_docs))
    all_docs.extend(file_docs)


## preprocess parsed pdfs - group titles and content immediately underneath titles together
print("Grouping PDF sections together")
grouped_docs = []
parent_id = -1
group_docs = []
for doc in all_docs:
    if doc.metadata["category"] == "Title":
        if len(group_docs) > 1:
          grouped_docs.append(group_docs)
          group_docs = []
        parent_id = doc.metadata["element_id"]
        group_docs = [doc]
    if doc.metadata.get("parent_id") == parent_id:
        group_docs.append(doc)
if len(group_docs) > 1:
    grouped_docs.append(group_docs)


## combine title-content groups into Documents. Add metadata for metadata filtering
print("Creating Langchain Documents")
docs_merged = []
for i, group in enumerate(grouped_docs):
  # combine the text. prep metadata filters for vectorstore.
  file_name = group[0].metadata['filename']
  details = file_name.split(".")[0].split(" ")
  year = int(details[0])
  quarter = details[1]
  company = details[2]
  page_number = group[0].metadata['page_number']
  section_title = group[0].page_content

  page_content = ""
  for d in group:
    if d.metadata['category'] == "Table":
      page_content += d.metadata['text_as_html'] + "\n\n"  
    else:
      page_content += d.page_content + "\n\n"
  
  merged_doc = Document(page_content=page_content, 
                        metadata={"file_name": file_name, 
                                  "year": year,
                                  "quarter": quarter,
                                  "company": company,
                                  "section_title": section_title, 
                                  "page_number": page_number})
  docs_merged.append(merged_doc)
  
## upload to pinecone vectorstore
print("Uploading Documents to Pinecone")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
pinecone_vectorstore = PineconeVectorStore.from_documents(
    docs_merged, embeddings, index_name=index_name
)