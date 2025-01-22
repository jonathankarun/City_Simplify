import io
from PyPDF2 import PdfReader

class PDFHandler:
    def extract_text(self, file: bytes) -> str:
        try:
            
            file_like_object = io.BytesIO(file)
        
            file_like_object.seek(0)
            print(f"First 500 bytes of PDF: {file_like_object.read(500)}")

            reader = PdfReader(file_like_object)
            text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
            
            if not text.strip():
                raise ValueError("No text found in the PDF.")
            return text
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {e}")
