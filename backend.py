# backend.py
from fastapi import FastAPI, HTTPException, UploadFile
from app.openai_client import OpenAIClient
from app.pdf_handler import PDFHandler
from app.qdrant_client_wrapper import QdrantClientWrapper


app = FastAPI()

# Initialize clients
qdrant_client = QdrantClientWrapper()
openai_client = OpenAIClient()
pdf_handler = PDFHandler()

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile):
    file_location = f"./Karun_Jonathan_resume.pdf"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}
    #Upload pdf endpoint
    try:
        content = await file.read()
        text = pdf_handler.extract_text(content)
        qdrant_client.upload_text(text)
        return {"message": "PDF uploaded and processed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask_question/")
async def ask_question(question: str):
    #Ask question endpoint
    try:
        context = qdrant_client.query(question)
        answer = openai_client.generate_answer(question, context)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

