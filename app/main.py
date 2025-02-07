import logging
from time import time
from fastapi import FastAPI, Request
from app.routes.query import router as query_router
from app.utils.logging import setup_logging

# Configure logging once
setup_logging()


app = FastAPI(title="RAG Application")

# Middleware to log incoming requests and responses.
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log request details
    start_time = time()
    logging.info(f"Request: {request.method} {request.url}")
    
    # Process the request
    response = await call_next(request)
    
    # Log response details and time taken
    process_time = time() - start_time
    logging.info(f"Response: {response.status_code} (Duration: {process_time:.2f}s)")
    
    return response

# Include routers
app.include_router(query_router, prefix="/api", tags=["Query"])