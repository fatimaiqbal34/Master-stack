from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.blog_agent import generate_blog
from agents.reasoning_agent import ask_reasoning_agent
from agents.chat_agent import chat_with_assistant


app = FastAPI(
    title="Master AI Stack API",
    description="Backend API for AI Agents",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BlogRequest(BaseModel):
    notes: str


class ReasonRequest(BaseModel):
    question: str


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Master AI Stack API is running 🚀",
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
    }


@app.post("/api/blog")
def create_blog(request: BlogRequest):
    if not request.notes.strip():
        raise HTTPException(
            status_code=400,
            detail="Project notes cannot be empty.",
        )

    try:
        blog = generate_blog(request.notes)
        return {
            "success": True,
            "blog": blog,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.post("/api/reasoning")
def reason(request: ReasonRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        result = ask_reasoning_agent(request.question)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.post("/api/chat")
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty.",
        )

    try:
        reply = chat_with_assistant(request.message, request.history)
        return {
            "reply": reply,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )