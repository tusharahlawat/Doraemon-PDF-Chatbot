from flask import Flask, request, jsonify
import os
import PyPDF2 # For PDF processing
import ollama # For Llama 3 interaction
import uuid # For generating unique filenames

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_TEXT_FOLDER = 'processed_texts'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PROCESSED_TEXT_FOLDER):
    os.makedirs(PROCESSED_TEXT_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_TEXT_FOLDER'] = PROCESSED_TEXT_FOLDER

# Helper function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() or "" # Add empty string if extract_text() returns None
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None
    return text

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file provided'}), 400
    
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        try:
            # Save the uploaded PDF temporarily
            temp_pdf_filename = str(uuid.uuid4()) + ".pdf"
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_pdf_filename)
            file.save(pdf_path)

            # Extract text from the PDF
            extracted_text = extract_text_from_pdf(pdf_path)
            if extracted_text is None or not extracted_text.strip():
                os.remove(pdf_path) # Clean up temp PDF
                return jsonify({'error': 'Could not extract text from PDF or PDF is empty.'}), 500

            # Save the extracted text to a .txt file
            text_filename = os.path.splitext(temp_pdf_filename)[0] + '.txt'
            text_file_path = os.path.join(app.config['PROCESSED_TEXT_FOLDER'], text_filename)
            with open(text_file_path, 'w', encoding='utf-8') as f:
                f.write(extracted_text)
            
            # Clean up the temporary uploaded PDF file
            os.remove(pdf_path)

            return jsonify({'message': 'PDF processed successfully!', 'filename': text_filename}), 200
        except Exception as e:
            # Clean up temp PDF if it exists and an error occurs
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid file type. Please upload a PDF.'}), 400

@app.route('/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    query = data.get('query')
    text_filename = data.get('filename')

    if not query or not text_filename:
        return jsonify({'error': 'Query or filename missing'}), 400

    text_file_path = os.path.join(app.config['PROCESSED_TEXT_FOLDER'], text_filename)
    if not os.path.exists(text_file_path):
        return jsonify({'error': 'Processed text file not found. Please upload PDF again.'}), 404

    try:
        with open(text_file_path, 'r', encoding='utf-8') as f:
            context = f.read().strip() # Read and strip whitespace

        if not context:
            return jsonify({'answer': 'The processed PDF content is empty. Please try a different PDF.'}), 200
        
        # Check if Ollama Llama 3 model is available
        ollama_models_response = ollama.list()
        available_model_names = []
        if ollama_models_response and 'models' in ollama_models_response and isinstance(ollama_models_response['models'], list):
            for model_info in ollama_models_response['models']:
                if isinstance(model_info, dict) and 'name' in model_info:
                    available_model_names.append(model_info['name'])
        
        if 'llama3:latest' not in available_model_names and 'llama3' not in available_model_names: # Check for llama3:latest or just llama3
             # Attempt to pull the model if not available
            print("Llama 3 model not found locally. Attempting to pull...")
            try:
                ollama.pull('llama3')
                print("Llama 3 model pulled successfully.")
            except Exception as e:
                print(f"Failed to pull Llama 3 model: {e}")
                return jsonify({'error': 'Llama 3 model not available and could not be pulled. Please ensure Ollama is running and the model is installed.'}), 500

        prompt = f"""You are Doraemon, a friendly and helpful AI assistant. Your primary goal is to answer questions based *solely* on the provided text. Your task is to carefully analyze the 'Provided Text' and answer the 'Question' using only information found within that text. Start your responses by introducing yourself as Doraemon if it's the beginning of a conversation or if it feels natural. 

        **Strict Instructions:**
        1.  **Base your answer ONLY on the 'Provided Text'.** Do not use any external knowledge or make assumptions beyond what is explicitly stated in the text.
        2.  If the answer to the 'Question' cannot be found in the 'Provided Text', you MUST respond with the exact phrase: "The information to answer this question is not available in the provided document."
        3.  Do not add any information that is not present in the 'Provided Text'.
        4.  Be concise and directly answer the question.
        5.  Maintain a friendly and helpful tone, like Doraemon.

        Provided Text:
        ---BEGIN PROVIDED TEXT---
        {context}
        ---END PROVIDED TEXT---

        Question: {query}

        Answer:"""

        response = ollama.generate(
            model='llama3', # Use llama3, Ollama will pick the specific version like llama3:latest
            prompt=prompt
        )
        
        return jsonify({'answer': response['response']}), 200

    except ollama.ResponseError as e:
        if "Model 'llama3' not found" in str(e) or "pull model" in str(e):
             return jsonify({'error': 'Llama 3 model not found. Please ensure Ollama is running and the model `llama3` is pulled (e.g., `ollama pull llama3`).'}), 500
        return jsonify({'error': f'Ollama API error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    # Make sure to run with `flask run` or `python app.py` after setting FLASK_APP=app.py
    # For development, debug=True is helpful.
    # Host '0.0.0.0' makes it accessible on the network.
    app.run(debug=True, host='0.0.0.0', port=5000)