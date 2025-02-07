from fastapi import APIRouter, HTTPException
from app.models.state import AnswerWithReferences, QuestionRequest
from app.services.rag_graph import graph

router = APIRouter()

@router.post("/query", response_model=AnswerWithReferences)
async def query(request: QuestionRequest):
    try:
        question = request.question
        result = graph.invoke({"question": question})
        return result['answer']
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again later.")