# Funções para extrair texto de documentos
import os
import PyPDF2
import docx


def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    text = ""
    doc = docx.Document(file_path)
    for paragraphs in doc.paragraphs:
        text += paragraphs.text + "\n"
    return text

def extract_text_from_txt(file_path):
    with open(file_path, "r") as file:
        return file.read()

def extract_text(file_path, text_data):
    # Check if text has already been extracted for this file
    if file_path in text_data:
        return text_data[file_path]
    
    # Extract text based on file extension
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    elif file_path.endswith(".txt"):
        text = extract_text_from_txt(file_path)
    else:
        raise ValueError("Formato de arquivo não suportado.")
        
    # Store the extracted text in the dictionary
    text_data[file_path] = text
    return text

'''
def get_stored_text(file_path):
    return text_data.get(file_path)

def clear_text_data():
    text_data.clear()
'''

#print(extract_text(r"data\docx\Amor é fogo que arde sem se ver.docx"))
