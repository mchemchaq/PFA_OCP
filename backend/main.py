# backend/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from pydantic import BaseModel
from contract_extractor import FreeContractExtractor

# Initialize the extractor globally when the app starts
extractor = FreeContractExtractor()

app = FastAPI(
    title="AI Contract Extractor & Chatbot API",
    description="API for extracting information and answering questions from PDF contracts.",
    version="1.0.0"
)

# CORS Middleware to allow requests from your Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust this to your Streamlit app's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    full_contract_text: str
    question: str

@app.get("/")
async def root():
    return {"message": "AI Contract Extractor API is running!"}

@app.post("/extract/")
async def extract_contract_info(pdf_file: UploadFile = File(...)):
    if not pdf_file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(await pdf_file.read())
            tmp_file_path = tmp_file.name
        
        extracted_data, full_text = extractor.extract_to_dict(tmp_file_path)
        
        # Clean up the temporary file
        os.unlink(tmp_file_path)

        return JSONResponse(content={"extracted_data": extracted_data, "full_text": full_text})
    except Exception as e:
        # Clean up in case of error too
        if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.post("/chat/")
async def chat_with_contract(request: QuestionRequest):
    try:
        answer = extractor.ask_question_from_text(request.full_contract_text, request.question)
        return JSONResponse(content={"answer": answer})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during Q&A: {str(e)}")