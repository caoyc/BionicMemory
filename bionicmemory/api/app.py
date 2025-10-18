"""FastAPI application for BionicMemory"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import uuid
from typing import Optional

from ..models.api_models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    MemoryAddRequest,
    MemoryQueryRequest,
    MemoryResponse,
    MemoryListResponse
)
from ..core.system import BionicMemorySystem
from ..core.proxy import OpenAIProxy
from ..config import settings


# Global instances
memory_system: Optional[BionicMemorySystem] = None
openai_proxy: Optional[OpenAIProxy] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    global memory_system, openai_proxy
    
    # Startup
    print("Initializing BionicMemory System...")
    memory_system = BionicMemorySystem()
    openai_proxy = OpenAIProxy()
    print("BionicMemory System initialized successfully")
    
    yield
    
    # Shutdown
    print("Shutting down BionicMemory System...")
    if openai_proxy:
        await openai_proxy.close()
    print("Shutdown complete")


app = FastAPI(
    title="BionicMemory",
    description="Bionic brain-inspired AI memory management system",
    version="0.1.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "BionicMemory",
        "version": "0.1.0",
        "description": "Bionic brain-inspired AI memory management system"
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """
    OpenAI-compatible chat completion endpoint with memory integration.
    
    Automatically retrieves relevant memories and injects them into context.
    """
    try:
        # Extract user_id from request (use 'user' field or default)
        user_id = request.user or "default_user"
        
        # Get last user message for memory query
        user_messages = [m for m in request.messages if m.role == "user"]
        if user_messages:
            last_message = user_messages[-1].content
            
            # Query relevant memories
            memories = memory_system.query_memories(
                user_id=user_id,
                query=last_message,
                n_results=5
            )
        else:
            memories = []
        
        # Forward to OpenAI with memory context
        response = await openai_proxy.chat_completion(request, memories)
        
        # Store the conversation in memory
        if user_messages:
            memory_system.add_memory(
                user_id=user_id,
                content=last_message,
                metadata={
                    "type": "user_message",
                    "model": request.model
                }
            )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/memories", response_model=dict)
async def add_memory(request: MemoryAddRequest):
    """Add a memory to the system"""
    try:
        result = memory_system.add_memory(
            user_id=request.user_id,
            content=request.content,
            metadata=request.metadata
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/memories/query", response_model=list)
async def query_memories(request: MemoryQueryRequest):
    """Query memories"""
    try:
        memories = memory_system.query_memories(
            user_id=request.user_id,
            query=request.query,
            n_results=request.n_results
        )
        return memories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/memories/stats/{user_id}")
async def get_memory_stats(user_id: str):
    """Get memory statistics for a user"""
    try:
        stats = memory_system.get_user_stats(user_id)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/memories/cleanup")
async def cleanup_memories(user_id: Optional[str] = None):
    """Clean up cold memories"""
    try:
        cleaned = memory_system.cleanup_memories(user_id)
        return {"cleaned": cleaned}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time()
    }
