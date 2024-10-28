import os
import csv
import spacy
from spacy.training.example import Example
import random
from docx import Document
import PyPDF2

# Load a blank English language model
nlp = spacy.blank("en")

# Add the NER component to the pipeline
ner = nlp.add_pipe("ner")
ner.add_label("SKILL")

# Define the folder where the CV files are located
data_folder = "cv_data/data"  # Changed to "data" folder

# Define the path to the CSV file
csv_filepath = "cv_data/Resume/Resume.csv"

# Initialize an empty list to store the training data
TRAIN_DATA = []

# Function to extract text from a PDF file
def extract_text_from_pdf(filename):
    pdf_reader = PyPDF2.PdfReader(open(filename, "rb"))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(filename):
    doc = Document(filename)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Iterate through the industry subfolders
for industry_folder in os.listdir(data_folder):
    industry_path = os.path.join(data_folder, industry_folder)
    if os.path.isdir(industry_path):
        # Iterate through the files in each subfolder
        for filename in os.listdir(industry_path):
            # Check if the file is a PDF or DOCX
            if filename.endswith((".pdf", ".docx")):
                filepath = os.path.join(industry_path, filename)
                # Extract the text from the file based on its format
                if filename.endswith(".pdf"):
                    text = extract_text_from_pdf(filepath)
                elif filename.endswith(".docx"):
                    text = extract_text_from_docx(filepath)

                # Append the text to the training data list
                TRAIN_DATA.append((text, {"entities": []}))  # No entities initially

# Read the CSV file
with open(csv_filepath, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    # Iterate through each row in the CSV file
    for row in reader:
        # Extract the resume text from the "Resume_str" column
        resume_text = row["Resume_str"]
        # Append the resume text to the training data list
        TRAIN_DATA.append((resume_text, {"entities": []}))

# Shuffle the training data
random.shuffle(TRAIN_DATA)

# Initialize the optimizer
optimizer = nlp.begin_training()

# Training loop
for itn in range(100):  # Adjust the number of iterations as needed
    random.shuffle(TRAIN_DATA)
    losses = {}
    # Iterate through the training data
    for text, annotations in TRAIN_DATA:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        nlp.update([example], drop=0.5, sgd=optimizer, losses=losses)
    print("Iteration:", itn, "Losses:", losses)

# Save the trained model
nlp.to_disk("./spacy_training/trained_model")  # Save in spacy_training folder