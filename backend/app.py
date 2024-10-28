from flask import Flask, request, jsonify
import PyPDF2
from docx import Document
import spacy

nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("./spacy_training/trained_model")
app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_cv():
    if 'file' not in request.files:
        print("No 'file' part in request.files:", request.files) 
        return jsonify({'error': 'No file part'}), 400

    try:
        file = request.files['file']  #
    except KeyError:
        print("File with key 'file' not found in the request.")
        return jsonify({'error': 'File not found'}), 400

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        try:
            text = ""
            if file.filename.rsplit('.', 1)[1].lower() == 'pdf':
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            elif file.filename.rsplit('.', 1)[1].lower() == 'docx':
                doc = Document(file)
                for para in doc.paragraphs:
                    text += para.text + '\n'

            analysis_results = analyze_cv(text)  # Call analyze_cv
            return jsonify(analysis_results), 200  # Return the results

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route("/analyze", methods=["POST"])  
def analyze_cv(text):  # Modified to accept text as an argument
    doc = nlp(text)

    skills = []
    for ent in doc.ents:
        if ent.label_ == "SKILL": 
            skills.append(ent.text)

    experience = []  # Placeholder for experience analysis

    response = {
        "skills": skills,
        "experience": experience
    }
    return response  # Return the response dictionary (no need for jsonify here)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)