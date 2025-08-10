import PyPDF2

def read_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader=PyPDF2.PdfReader(file)
            print(f"Total pages in PDF: {len(pdf_reader.pages)}")
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text() or ""
            return text
    except Exception as e:
        return f"Error reading pdf: {str(e)}"