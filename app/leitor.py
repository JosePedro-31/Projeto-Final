# Funções para extrair texto de documentos
import os
import PyPDF2
import docx

# read pdf files
def extract_text_from_pdf(file_path):
    text = ""
    
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    
    return text

# read docx files
def extract_text_from_docx(file_path):
    text = ""
    doc = docx.Document(file_path)
    
    for paragraphs in doc.paragraphs:
        text += paragraphs.text + "\n" # add a new line after each paragraph

    return text

# read txt files
def extract_text_from_txt(file_path):
    # using the encoding utf-8 to read special characters like ç, ã, etc
    with open(file_path, "r", encoding='utf-8') as file:
        return file.read()


def extract_text(folder_path, text_data):
    file_names = os.listdir(folder_path)
    for name in file_names:
        # Get the full path of the file
        file_path = folder_path + "\\" + name    
        
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
        



