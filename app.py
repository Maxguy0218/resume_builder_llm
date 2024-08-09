import streamlit as st
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import io

# Function to generate the summary using Google Generative AI
def generate_result(prompt):
    response = model.generate_content(prompt)
    return response.text

# Function to generate the resume PDF
def generate_resume(output_filename, details):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    normal_style = styles['BodyText']

    title = Paragraph(f"{details['Name']}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))

    contact_info = f"""
    <b>{details['Name']}</b><br/>
    {details['Email']}<br/>
    {details['Phone']}<br/>
    {details['Address']}
    """
    contact_paragraph = Paragraph(contact_info, normal_style)
    elements.append(contact_paragraph)
    elements.append(Spacer(1, 12))

    summary_heading = Paragraph("Summary", heading_style)
    elements.append(summary_heading)

    prompt = f"Craft a resume summary for a {details['Desired Role']} position, tools used {', '.join(details['Tools'])} fresher, concise but professional, no headline"
    summary_text = generate_result(prompt)
    summary_paragraph = Paragraph(summary_text, normal_style)
    elements.append(summary_paragraph)
    elements.append(Spacer(1, 12))

    experience_heading = Paragraph("Experience", heading_style)
    elements.append(experience_heading)

    experience_text = ""
    for experience in details['Experiences']:
        role = generate_result(f"Sample responsibilities about {experience} for resume, no heading, and in bullet points, concise, at most 3 points")
        experience_text += f"""
        - <b>{experience}</b><br/>
        {role}<br/>
        """
    experience_paragraph = Paragraph(experience_text, normal_style)
    elements.append(experience_paragraph)
    elements.append(Spacer(1, 12))

    education_heading = Paragraph("Education", heading_style)
    elements.append(education_heading)
    education_text = f"""
    <b>{details['Education'][0]}</b> from {details['Education'][1]}
    """
    education_paragraph = Paragraph(education_text, normal_style)
    elements.append(education_paragraph)
    elements.append(Spacer(1, 12))

    skills_heading = Paragraph("Skills", heading_style)
    elements.append(skills_heading)
    skills_text = f"""
    - Programming Languages: {', '.join(details['Programming Languages'])}<br/>
    - Web Technologies: {', '.join(details['Web Technologies'])}<br/>
    - Tools: {', '.join(details['Tools'])}
    """
    skills_paragraph = Paragraph(skills_text, normal_style)
    elements.append(skills_paragraph)
    elements.append(Spacer(1, 12))

    doc.build(elements)

# Streamlit app
st.title("Resume Generator")

api_key = st.text_input("Enter your Google API Key", type="password")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    details = {
        "Name": st.text_input("Name"),
        "Email": st.text_input("Email"),
        "Phone": st.text_input("Phone"),
        "Address": st.text_input("Address"),
        "Desired Role": st.text_input("Desired Role"),
        "Programming Languages": st.text_input("Programming Languages (comma separated)").split(","),
        "Web Technologies": st.text_input("Web Technologies (comma separated)").split(","),
        "Tools": st.text_input("Tools (comma separated)").split(","),
        "Experiences": st.text_input("Experiences (comma separated)").split(","),
        "Education": [
            st.text_input("Education Degree"),
            st.text_input("Education Institution")
        ]
    }

    if st.button("Generate Resume"):
        output = io.BytesIO()
        generate_resume(output, details)
        st.success("Resume generated successfully!")

        # Download button
        st.download_button(
            label="Download Resume",
            data=output,
            file_name="resume.pdf",
            mime="application/pdf"
        )
