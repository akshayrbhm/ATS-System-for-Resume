from dotenv import load_dotenv
import streamlit as st
import os 
import io
from PIL import Image
import pdf2image
import base64
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_llm_response(input, pdf_content,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response= model.generate_content([input, pdf_content[0], prompt])
    return response.text


def setup_input_pdf(uploaded_file):
    if uploaded_file is not None:
        image = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = image[0]

        #conversion to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.get_value()
        
        pdf_parts = [
            { 'mimi_type' :"image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() }    ]
        return pdf_parts
    else:
        raise FileNotFoundError('No File uploaded')
 



# Streamlit
st.set_page_config(page_title='Resume Analysis Expert')
st.header("ATS Tracking System")
input_text = st.text_area("Job Description", key='input')
uploaded_file = st.file_uploader("Upload your resume in pdf format", type=['pdf'])

if uploaded_file is not None:
    st.write('PDF Uploaded Successfully')

submit_a = st.button("Tell me about the Resume")
submit_b = st.button("What are the scope of Improvement")
submit_c = st.button('What are the keywords are missing')
submit_d = st.button('What are the percentage of match with JD')

input_promt1 = """
You are an Experienced HR with technical experience in the field of data analysis, data science, data, engineer, mlops, machine learning engineer, deep learning, 
generative ai, natural language processing, software development, fullstack development  and your task is to oreview the uploaded
resume in pdf format against the job description for the given profiles.
Please share your professional evaluation on whether the candidates profile alligns with the given job description
and also heighlights the  strength and weaknesses of the applicants in relation to the specific job description
"""

input_promt2 = """
You are skilled ATS (application tracking system) scanner with the deep understanding of data analysis, data science, data, engineer, mlops, machine learning engineer, deep learning, 
generative ai, natural language processing, software development, fullstack development and deep ATS functionality,
Your task is to evaluate whether the resume matches against the given job description. and suggest the scope of improvement in skills
"""

input_promt3 = """
You are skilled ATS (application tracking system) scanner with the deep understanding of data analysis, data science, data, engineer, mlops, machine learning engineer, deep learning, 
generative ai, natural language processing, software development, fullstack development and deep ATS functionality,
Your task is to evaluate which keywords are missing in resume against the given job description. Give me the missing key words as an output.
"""

input_promt4 = """
You are skilled ATS (application tracking system) scanner with the deep understanding of data analysis, data science, data, engineer, mlops, machine learning engineer, deep learning, 
generative ai, natural language processing, software development, fullstack development and deep ATS functionality,
Your task is to evaluate whether the resume matches against the given job description. Give me the percentage of match . first give the
output as percentage match value
"""


if submit_a:
    if uploaded_file is not None:
        pdf_content = setup_input_pdf(uploaded_file)
        response = get_llm_response(input_promt1, pdf_content, input_text)
        st.subheader("The Response is ")
        st.write(response)
    else:
        st.write('Please upload the Resume')

if submit_b:
    if uploaded_file is not None:
        pdf_content = setup_input_pdf(uploaded_file)
        response = get_llm_response(input_promt2, pdf_content, input_text)
        st.subheader("The Response is ")
        st.write(response)
    else:
        st.write('Please upload the Resume')

if submit_c:
    if uploaded_file is not None:
        pdf_content = setup_input_pdf(uploaded_file)
        response = get_llm_response(input_promt3, pdf_content, input_text)
        st.subheader("The Response is ")
        st.write(response)
    else:
        st.write('Please upload the Resume')

if submit_d:
    if uploaded_file is not None:
        pdf_content = setup_input_pdf(uploaded_file)
        response = get_llm_response(input_promt4, pdf_content, input_text)
        st.subheader("The Response is ")
        st.write(response)
    else:
        st.write('Please upload the Resume')

