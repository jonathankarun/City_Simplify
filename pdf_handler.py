import io
from PyPDF2 import PdfReader

class PDFHandler:
    def extract_text(self, file: bytes) -> str:
        try:
            # Convert bytes to file-like object
            file_like_object = io.BytesIO(file)
            
            # Debug: Check the first few bytes of the file
            file_like_object.seek(0)
            print(f"First 500 bytes of PDF: {file_like_object.read(500)}")

            reader = PdfReader(file_like_object)
            text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
            
            if not text.strip():
                raise ValueError("No text found in the PDF.")
            return text
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {e}")
