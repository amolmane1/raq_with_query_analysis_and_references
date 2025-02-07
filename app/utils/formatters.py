from typing import List
from langchain_core.documents import Document


def format_docs(docs: List[Document]) -> str:
    formatted = [
        f"file_name: {doc.metadata['file_name']}\nsection_title: {doc.metadata['section_title']}\npage_number: {doc.metadata['page_number']}\nSnippet: {doc.page_content}"
        for doc in docs
    ]
    return "\n\n" + "\n\n".join(formatted)