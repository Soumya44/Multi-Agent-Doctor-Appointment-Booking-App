from fastapi import HTTPException, FastAPI, Header
from models.model import GenerationResponse, GenerationRequest, ErrorResponse
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage
from agent import build_graph
import logging
import uvicorn
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Create FastAPI app
app = FastAPI(
    title="Hospital Appointment Booking System",
    description="A comprehensive hospital appointment booking system with AI assistant",
    version="1.0.0"
)

# Build graph on startup
graph = build_graph()
logging.info('Loaded graph')

@app.post("/generate-stream/", response_model=GenerationResponse, responses={500: {"model": ErrorResponse}})
async def generation_streaming(request: GenerationRequest, thread_id: str = Header('111222', alias="X-THREAD-ID")):
    """
    Generate response for hospital appointment queries using the AI assistant.
    
    Args:
        request: The generation request containing the user query
        thread_id: Thread ID for session management (passed in X-THREAD-ID header)
    
    Returns:
        JSON response with the assistant's answer and dialog state
    """
    try:
        query = request.query
        logging.info(f'Received the Query - {query} & thread_id - {thread_id}')
        
        # Prepare input for the graph
        inputs = [
            HumanMessage(content=query)
        ]
        state = {'messages': inputs}
        config = {"configurable": {"thread_id": thread_id, "recursion_limit": 10}}
        
        # Invoke the graph
        response = graph.invoke(input=state, config=config)
        
        logging.info('Generated Answer from Graph')
        logging.info(f'Graph Response: {response}')
        
        # Extract dialog state and messages
        dialog_states = response.get('dialog_state', [])
        dialog_state = dialog_states[-1] if dialog_states else 'primary_assistant'
        
        messages = response.get('messages', [])
        answer = messages[-1].content if messages else ''
        
        return JSONResponse({
            'dialog_state': dialog_state if dialog_state else '',
            'answer': answer if answer else ''
        })
        
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )

# @app.post("/execute", response_model=GenerationResponse, responses={500: {"model": ErrorResponse}})
# async def execute_query(request: GenerationRequest, thread_id: str = Header('111222', alias="X-THREAD-ID")):
#     """
#     Execute query endpoint for compatibility with Streamlit UI.
#     This endpoint provides the same functionality as generate-stream but with a different route.
#     """
#     return await generation_streaming(request, thread_id)

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker containers"""
    return {"status": "healthy", "service": "hospital_booking_backend"}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Hospital Appointment Booking System API",
        "version": "1.0.0",
        "endpoints": {
            "generate_stream": "/generate-stream/",
            "execute": "/execute",
            "health": "/health",
            "docs": "/docs"
        }
    }

# Add CORS middleware for frontend integration
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logging.info(f"Starting Hospital Appointment System on {host}:{port}")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="debug"
    )