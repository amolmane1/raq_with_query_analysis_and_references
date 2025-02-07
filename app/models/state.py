from typing_extensions import List, Annotated, TypedDict
from langchain_core.documents import Document
from pydantic import BaseModel


# Define the request body schema
class QuestionRequest(BaseModel):
    question: str

# Desired schema for response
class Reference(TypedDict):
    """Details about a reference used in the answer."""
    file_name: Annotated[
        str,
        "The name of the document where the referenced information is found.",
    ]
    page_number: Annotated[int, "The page number where the information is located."]
    section_title: Annotated[
        str,
        "The title of the section or subsection containing the information.",
    ]


class AnswerWithReferences(TypedDict):
    """An answer to the question, with SPECIFIC references."""
    answer: str
    references: Annotated[
        List[Reference],
        ...,
        "List of the SPECIFIC references (file name, page number, section title) used to answer the question",
    ]


# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: AnswerWithReferences