import streamlit as st
import spacy
import pdfplumber
import docx
import re

# Load spaCy model (already installed via requirements.txt)
nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.sidebar.title("👤 Developer Info")
st.sidebar.markdown("""
**Made by:** Pagidimarri Namratha  
📧 [Email](mailto:ppagidimarrinamratha@gmail.com)  
🌐 [GitHub](https://github.com/PN1225)  
""")

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def analyze_resume(text):
    doc = nlp(text)

    word_count = len([t for t in doc if not t.is_punct])
    grammar_errors = len([t for t in doc if t.pos_ == "X"])

    skills = [
        "python","java","c++","javascript","html","css","sql",
        "machine learning","data science","flask","django",
        "git","github","aws","linux","communication","teamwork"
    ]

    found_skills = [s for s in skills if s in text.lower()]
    sections = ["education","experience","projects","skills","certifications"]
    found_sections = [s for s in sections if re.search(s, text, re.I)]

    score = 0
    score += min(10, word_count // 30)
    score += 20 if grammar_errors <= 3 else 10
    score += len(found_skills) * 3
    score += len(found_sections) * 5

    suggestions = []
    if word_count < 150:
        suggestions.append("📄 Resume too short")
    if len(found_skills) < 3:
        suggestions.append("💼 Add more skills")
    if len(found_sections) < 3:
        suggestions.append("🧩 Add missing sections")

    return word_count, grammar_errors, found_skills, found_sections, score, suggestions

st.title("📄 AI Resume Analyzer")

file = st.file_uploader("Upload Resume (PDF / DOCX)", type=["pdf","docx"])

if file:
    if file.type == "application/pdf":
        text = extract_text_from_pdf(file)
    else:
        text = extract_text_from_docx(file)

    wc, ge, skills, sections, score, tips = analyze_resume(text)

    st.success(f"Resume Score: {score}/100")
    st.write("**Word Count:**", wc)
    st.write("**Grammar Issues:**", ge)

    st.subheader("Skills Found")
    st.write(", ".join(skills) or "None")

    st.subheader("Sections Found")
    st.write(", ".join(sections) or "None")

    st.subheader("Suggestions")
    for t in tips:
        st.warning(t)
