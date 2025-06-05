from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from llm_utils import analyze_case, chat_followup
from parser_utils import extract_combined_text

app = FastAPI()

# IMPORTANT: Remove trailing slash from origin URL and add allow_credentials if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://medico-llm-assistant.netlify.app",  # No trailing slash
        "http://localhost:3000",  # Add localhost if testing locally
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,  # Add if your frontend sends cookies or auth headers
)

@app.get("/")
def read_root():
    return {"status": "Backend is running"}

@app.post("/analyze/")
async def analyze(
    symptoms: str = Form(...),
    test_results: str = Form(""),
    prescription_text: str = Form(""),
    prescription_files: List[UploadFile] = File(None),
    test_files: List[UploadFile] = File(None)
):
    prescription_content = extract_combined_text(prescription_files or []) if prescription_files else ""
    test_content = extract_combined_text(test_files or []) if test_files else ""

    full_prescription = prescription_text + "\n" + prescription_content
    full_test_results = test_results + "\n" + test_content

    result = analyze_case(symptoms, full_test_results, full_prescription)
    return {"response": result}

@app.post("/chat/")
async def chat(message: str = Form(...)):
    return {"reply": chat_followup(message)}
