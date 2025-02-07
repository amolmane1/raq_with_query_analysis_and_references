import logging
from langchain import hub
from langchain_core.documents import Document
from langgraph.graph import START, StateGraph

from app.data_access.pinecone_client import retriever
from app.models.state import State, AnswerWithReferences
from app.data_access.openai import llm
from app.utils.formatters import format_docs


# Define prompt for question-answering
prompt = hub.pull("rlm/rag-prompt")

# Define application steps
def retrieve(state: State):
    retrieved_docs = retriever.invoke(state["question"])
    logging.info("Retrieved context for question: \n%s", retrieved_docs)
    return {"context": retrieved_docs}


def generate(state: State):
    # format context to include file name, page number and section title 
    # so that with_structured_output can use it to give accurate references.
    formatted_docs = format_docs(state["context"])
    logging.info("Formatted context for question: \n%s", formatted_docs)
    
    messages = prompt.invoke({"question": state["question"], "context": formatted_docs})
    logging.info("Full prompt for question: \n%s", messages)
    
    # get answer along with references
    structured_llm = llm.with_structured_output(AnswerWithReferences)
    response = structured_llm.invoke(messages)
    logging.info("Response for question: \n%s", response)
    return {"answer": response}


# Build the graph
def build_graph():
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    return graph_builder.compile()

graph = build_graph()