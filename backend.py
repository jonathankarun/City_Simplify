#source venv/bin/activate
#python main.py

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, UploadFile
from app.openai_client import OpenAIClient
from app.pdf_handler import PDFHandler
from app.qdrant_client_wrapper import QdrantClientWrapper

app = FastAPI()

# Initialize clients needed for the program!
qdrant_client = QdrantClientWrapper()
openai_client = OpenAIClient()
pdf_handler = PDFHandler()


@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = None):
    # Specify the file path directly here -> 
    file_location = "/Users/jonathankarun/CITYSIMPLIFY/city_simplify_code/Test_Doc.pdf"
    try:
        with open(file_location, "rb") as f:
            print(f.read(500))  # Read and print the first 500 bytes to verify the file content

        # Directly pass the content from the file to the PDF handler
        with open(file_location, "rb") as f:
            content = f.read()

        # Process the file content
        text = pdf_handler.extract_text(content)
        qdrant_client.upload_text(text)
        
        return {"message": "PDF uploaded and processed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Define the model to accept JSON body
class QuestionRequest(BaseModel):
    question: str

@app.post("/ask_question/")
async def ask_question(request: QuestionRequest):
    try:
        context = qdrant_client.query(request.question)  # Querying context from Qdrant
        answer = openai_client.generate_answer(request.question, context)  # Generating answer using OpenAI
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


