import mysql.connector
import os
import PyPDF2
from tkinter import Tk, filedialog
from transformers import pipeline
import torch
from datetime import datetime


if not torch.cuda.is_available() and not torch.backends.mps.is_available() and not torch.__version__:
    raise ImportError("PyTorch is not installed. Please install PyTorch to use Hugging Face models. Visit https://pytorch.org/get-started/locally/ for installation instructions.")

def create_db_connection():
    return mysql.connector.connect(
        host="localhost",      
        user="root",           
        password="itzmelokesh18",   
        database="project_mini"      
    )

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text if text.strip() else None
    except Exception as e:
        print(f"Error: Unable to extract text from PDF. {e}")
        return None

def upload_pdf():
    root = Tk()
    root.withdraw()  
    file_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])
    return file_path

def answer_question(context, question, qa_pipeline):
    try:
        response = qa_pipeline(
            question=question,
            context=context,
            max_answer_len=100,  
            handle_impossible_answer=True 
        )
        return response['answer'] if response['answer'] else "No answer found"
    except Exception as e:
        return f"Error: Unable to process the question. {e}"
def save_pdf_data(pdf_name, pdf_path, question, answer):
    try:
        conn = create_db_connection()
        cursor = conn.cursor()

        upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not answer:
        
            cursor.execute('''INSERT INTO pdf_data (pdf_name, pdf_path, upload_date, question, answer)
                          VALUES (%s, %s, %s, %s, %s)''',
                       (pdf_name, pdf_path, upload_date, question, answer))

            conn.commit()  
        
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()  

def check_saved_data():
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pdf_data')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

if __name__ == "__main__":
    print("Please upload a PDF file.")
    pdf_path = upload_pdf()
    
    if pdf_path:
        print("Extracting text from the PDF...")
        pdf_text = extract_text_from_pdf(pdf_path)
        
        if pdf_text:
            print("PDF text extracted successfully.")
            print("\nYou can now ask questions about the PDF content.\n")

            try:
                qa_pipeline = pipeline(
                    "question-answering",
                    model="bert-large-uncased-whole-word-masking-finetuned-squad"
                )
            except Exception as e:
                print(f"Error: Unable to initialize the QA pipeline. {e}")
                exit(1)

            while True:
                question = input("Enter your question (or type 'exit' to quit): ")
                
                if question.lower() == "exit":
                    print("Exiting. Goodbye!")
                    break
                elif question.lower() == "show table":
                    check_saved_data()
                else:
                    answer = answer_question(pdf_text, question, qa_pipeline)
                    
                    if not answer or answer in ["Error", "No answer found"]:  
                        print("No valid answer found or an error occurred, skipping save.")
                    else:
                        print(f"Answer: {answer}")
                        save_pdf_data(os.path.basename(pdf_path), pdf_path, question, answer)
                    
        else:
            print("Failed to extract text or the PDF contains no text.")
    else:
        print("No file was selected.")
