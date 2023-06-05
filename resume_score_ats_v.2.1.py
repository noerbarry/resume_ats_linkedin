import re
from PyPDF2 import PdfReader
from docx import Document
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import streamlit as st
import os

# Function to read text from a PDF file
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

# Function to read text from a Word file (DOCX)
def read_docx(file_path):
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text
    return text

# Function to validate LinkedIn resume in Indonesian
def validate_resume_id(file_path):
    try:
        # Read text from the resume file
        if file_path.endswith('.pdf'):
            resume_text = read_pdf(file_path)
        elif file_path.endswith('.docx'):
            resume_text = read_docx(file_path)
        else:
            st.warning("Unsupported file format.")
            return
        
        # Process the resume text
        resume_text = resume_text.lower()
        resume_text = re.sub(r'\s+', ' ', resume_text)
        resume_text = re.sub(r'\W', ' ', resume_text)
        resume_words = re.findall(r'\b\w+\b', resume_text)
        
        # Example validation: Check if the keyword "pengalaman" (experience) is present in the resume
        if 'pengalaman' in resume_words:
            st.success("Resume passes ATS (Bahasa Indonesia).")
        else:
            st.warning("Resume does not pass ATS (Bahasa Indonesia).")
        
        # Example validation: Check for stop words in the resume
        stop_words = set(stopwords.words('indonesian'))
        stop_words_in_resume = [word for word in resume_words if word in stop_words]
        if stop_words_in_resume:
            st.warning("Resume contains stop words: {}".format(stop_words_in_resume))
    
    except Exception as e:
        st.error("An error occurred while processing the resume: {}".format(str(e)))

# Function to validate LinkedIn resume in English
def validate_resume_en(file_path):
    try:
        # Read text from the resume file
        if file_path.endswith('.pdf'):
            resume_text = read_pdf(file_path)
        elif file_path.endswith('.docx'):
            resume_text = read_docx(file_path)
        else:
            st.warning("Unsupported file format.")
            return
        
        # Process the resume text
        resume_text = resume_text.lower()
        resume_text = re.sub(r'\s+', ' ', resume_text)
        resume_text = re.sub(r'\W', ' ', resume_text)
        resume_words = re.findall(r'\b\w+\b', resume_text)
        
        # Example validation: Check if the keyword "experience" is present in the resume
        if 'experience' in resume_words:
            st.success("Resume passes ATS (English).")
        else:
            st.warning("Resume does not pass ATS (English).")
        
        # Example validation: Check for stop words in the resume
        stop_words = set(stopwords.words('english'))
        stop_words_in_resume = [word for word in resume_words if word in stop_words]
        if stop_words_in_resume:
            st.warning("Resume contains stop words: {}".format(stop_words_in_resume))
    
    except Exception as e:
        st.error("An error occurred while processing the resume: {}".format(str(e)))

# Streamlit application view
st.title("Linkedin Resume Validation using ATS System method")
st.write('Noer Barrihadianto')

hide_streamlit_style = """
        footer {
	
	visibility: hidden;
	
	}
footer:after {
	content:'goodbye'; 
	visibility: visible;
	display: block;
	position: relative;
	#background-color: red;
	padding: 5px;
	top: 2px;
}
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# File upload form for resume
uploaded_file = st.file_uploader("Upload LinkedIn resume file", type=["pdf", "docx", "doc", "pptx", "ppt"])

# Validation button
if uploaded_file is not None:
    st.write("Evaluating the resume...")
    # Create 'temp' directory if it doesn't exist
    if not os.path.exists("temp"):
        os.makedirs("temp")
    # Save the file to the temporary directory
    with open(os.path.join("temp", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    file_path = os.path.join("temp", uploaded_file.name)
    # Perform validation based on the selected language
    if st.checkbox("Bahasa Indonesia"):
        validate_resume_id(file_path)
    if st.checkbox("English"):
        validate_resume_en(file_path)
