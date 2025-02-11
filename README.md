# AskPDF

## Overview
AskPDF is a Python-based application that allows users to extract text from PDF files, ask questions about the extracted content using an AI-powered question-answering model, and store the interactions in a MySQL database.

## Features
- Upload and extract text from PDFs.
- Use a BERT-based AI model for question answering.
- Store uploaded PDF details, questions, and answers in a MySQL database.
- Retrieve stored interactions.

## Requirements
### Dependencies
Ensure you have the following installed:
- Python 3.x
- MySQL Server
- Required Python libraries (install via pip):
  ```bash
  pip install mysql-connector-python torch transformers PyPDF2 tkinter
  ```

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/askpdf.git
   cd askpdf
   ```
2. Configure MySQL Database:
   - Create a database named `project_mini`.
   - Create a table named `pdf_data` using the following SQL script:
     ```sql
     CREATE TABLE pdf_data (
         id INT AUTO_INCREMENT PRIMARY KEY,
         pdf_name VARCHAR(255) NOT NULL,
         pdf_path TEXT NOT NULL,
         upload_date DATETIME NOT NULL,
         question TEXT NOT NULL,
         answer TEXT NOT NULL
     );
     ```
   - Update `create_db_connection()` function with your MySQL credentials.
3. Run the application:
   ```bash
   python main.py
   ```

## Usage
1. The script will prompt you to upload a PDF file.
2. Once uploaded, it will extract text from the PDF.
3. You can then ask questions related to the document's content.
4. Type `show table` to view stored questions and answers.
5. Type `exit` to close the application.

## Future Enhancements
- Web-based UI for better accessibility.
- Support for multiple file formats.
- Improved NLP model integration.

## License
This project is licensed under the MIT License.

## Author
Developed by **[Nelluri Lokesh]**

## Contributing
Feel free to fork this repository, submit issues, and send pull requests to improve the project.

