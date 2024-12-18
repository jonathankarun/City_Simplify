from PyPDF2 import PdfReader

class PDFHandler:
    def extract_text(self, file: bytes) -> str:
        try:
            reader = PdfReader(file)
            text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
            print(text) 
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {e}")