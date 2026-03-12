from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.services.code_analyzer import analyze_python_code
from app.services.ai_service import explain_code
from app.services.bug_detector import detect_bugs
from app.services.vector_store import add_documents, search
from app.services.code_loader import split_code_into_chunks
from app.services.rag_ai import generate_answer

app = FastAPI(title="AI Developer Assistant")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "AI Developer Assistant API running"}


# Analyze code
@app.post("/analyze-code/")
async def analyze_code(file: UploadFile = File(...)):
    content = await file.read()
    code = content.decode("utf-8")

    analysis = analyze_python_code(code)

    return {
        "filename": file.filename,
        "analysis": analysis
    }


# Explain code
@app.post("/explain-code/")
async def explain_uploaded_code(file: UploadFile = File(...)):
    content = await file.read()
    code = content.decode("utf-8")

    explanation = explain_code(code)

    return {
        "filename": file.filename,
        "explanation": explanation
    }


# Detect bugs
@app.post("/detect-bugs/")
async def detect_code_bugs(file: UploadFile = File(...)):
    content = await file.read()
    code = content.decode("utf-8")

    bugs = detect_bugs(code)

    return {
        "filename": file.filename,
        "issues": bugs
    }


# Upload codebase for RAG
@app.post("/upload-codebase/")
async def upload_codebase(file: UploadFile = File(...)):
    content = await file.read()
    code = content.decode("utf-8")

    chunks = split_code_into_chunks(code)
    add_documents(chunks)

    return {"message": "Code indexed successfully"}


# Chat with codebase
@app.post("/chat-codebase/")
async def chat_codebase(request: QuestionRequest):

    question = request.question

    results = search(question)
    context = "\n".join(results)

    answer = generate_answer(question, context)

    return {
        "question": question,
        "answer": answer,
        "context_used": context
    }

@app.get("/get-file/")
def get_file(name: str):
    try:
        with open(name, "r", encoding="utf-8") as f:
            code = f.read()
        return {"code": code}
    except:
        return {"code": "File not found"}