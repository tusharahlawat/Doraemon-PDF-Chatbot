# Doraemon PDF Chatbot

This project is a Flask-based web application that allows users to upload PDF files, extract text from them, and then chat with an AI assistant (powered by Ollama and Llama 3) about the content of the PDF. The AI assistant is designed to answer questions based *solely* on the text provided from the uploaded PDF.

## Features

-   **PDF Upload:** Users can upload PDF files through a web interface.
-   **Text Extraction:** The application extracts text content from the uploaded PDF.
-   **AI-Powered Chat:** Users can ask questions about the PDF content, and a Llama 3 model (via Ollama) will provide answers.
-   **Doraemon Persona:** The AI assistant adopts a friendly "Doraemon" persona.
-   **Contextual Answers:** The AI is strictly instructed to answer only based on the information present in the PDF.
-   **Markdown Rendering:** Bot responses in the chat are rendered with markdown support for better readability (e.g., bold text, lists).
-   **Simple Web Interface:** A clean and user-friendly interface for uploading PDFs and chatting.

## Project Structure

```
Doraemon-PDF-Chatbot/
├── app.py # Main Flask application, handles PDF processing and Ollama interaction
├── uploads/ # Temporary storage for uploaded PDF files (created automatically)
├── processed_texts/ # Storage for extracted text from PDFs (created automatically)
├── static/
│ └── index.html # Frontend HTML, CSS, and JavaScript for the chat interface
│ └── download.png # Doraemon avatar image
├── requirements.txt # Python dependencies
└── README.md 
```
## Images
____________________________________________________________________________________________________________________________________________________________________________________________________________________
![image](https://github.com/user-attachments/assets/7e3039f4-66a4-4ae8-803a-70b0791a582d)
____________________________________________________________________________________________________________________________________________________________________________________________________________________
![image](https://github.com/user-attachments/assets/b87e27e0-9741-4206-a85a-9bf21f2667d3)
____________________________________________________________________________________________________________________________________________________________________________________________________________________
![image](https://github.com/user-attachments/assets/1b2dea22-41e2-4a3d-9b3f-b52398bf0a15)
____________________________________________________________________________________________________________________________________________________________________________________________________________________
![image](https://github.com/user-attachments/assets/126e1156-547c-42b9-ad61-a882ca7be6f6)
____________________________________________________________________________________________________________________________________________________________________________________________________________________

## Setup and Installation

1.  **Clone the repository or download the files.**

2.  **Ensure Ollama is Installed and Running:**
    This application requires Ollama to be installed and running with the `llama3` model available.
    *   Download and install Ollama from [https://ollama.com/download](https://ollama.com/download).
    *   Pull the Llama 3 model: `ollama pull llama3`
    *   Ensure the Ollama service is running.

3.  **Create a Python Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    *   Windows: `venv\Scripts\activate`
    *   macOS/Linux: `source venv/bin/activate`

4.  **Install Dependencies:**
    Navigate to the project directory in your terminal and run:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Application

1.  **Ensure Ollama is running and the `llama3` model is available.**

2.  **Set the Flask App Environment Variable (Optional but good practice):**
    *   Windows (Command Prompt): `set FLASK_APP=app.py`
    *   Windows (PowerShell): `$env:FLASK_APP = "app.py"`
    *   macOS/Linux: `export FLASK_APP=app.py`

3.  **Run the Flask Application:**
    In your terminal, from the project's root directory (`X1/`), run:
    ```bash
    flask run
    ```
    Or directly:
    ```bash
    python app.py
    ```

4.  **Access the Application:**
    Open your web browser and go to `http://127.0.0.1:5000/` or `http://localhost:5000/`.
    If you ran it with `host='0.0.0.0'`, it might also be accessible on your local network IP address.

## Usage

1.  Open the web application in your browser.
2.  Click the "Choose File" button to select a PDF file from your computer.
3.  Click the "Upload and Process PDF" button.
4.  Wait for the status message to indicate that the PDF has been processed successfully.
5.  The chat interface will appear.
6.  Type your questions about the PDF content into the input field and press Enter or click the send button.
7.  Doraemon (the AI assistant) will respond based on the information in the PDF.

## Dependencies

-   Flask
-   PyPDF2
-   ollama
-   python-dotenv (though not explicitly used in the current `app.py` for environment variables, it's good practice for API keys if needed in future)

See `requirements.txt` for specific versions.

## Notes

*   The application creates `uploads` and `processed_texts` directories if they don't exist.
*   Uploaded PDFs are temporarily stored in `uploads` and then deleted after text extraction.
*   Extracted text is stored in `.txt` files in the `processed_texts` folder.
*   Error handling is in place for PDF processing, Ollama API interactions, and file operations.
*   The application attempts to pull the `llama3` model if it's not found locally, but this requires an active internet connection and for Ollama to be correctly configured.
