import streamlit as st
from src.helper import extract_text_from_pdf,ask_groqai


st.set_page_config(
    page_title ="Job Recommender",layout="wide"
)

st.title("🤖 AI-Powered Job Recommendation System")
st.markdown("Upload your resume and get personalized job recommendations!")

uploaded_file  = st.file_uploader("Choose your resume (PDF format)", type="pdf")

if uploaded_file is not None:
    with st.spinner("Processing your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Summarizing your resume..."):
        summary = ask_groqai(
            f"Summarize this resume highlighting the skills, education and experience: \n\n{resume_text}",
            max_tokens=1000
        )
    with st.spinner("Finding skill gaps..."):
        gaps = ask_groqai(
            f"Analyze this resume and highlight missing skills than certifications and experiences needed for better job opportunities: \n\n{resume_text}",
            max_tokens=500
        )  
    with st.spinner("Creating Future roadmap..."):
        roadmap = ask_groqai(
            f"Based on this resume suggest a future roadmap to improve this person's career prospects(Skills to learn, certification needed, industry exposure): \n\n{resume_text}",
            max_tokens=400
        )        
# Display nicely formatted results
st.markdown("---")
st.header("📑 Resume Summary")
st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{summary}</div>", unsafe_allow_html=True)

st.markdown("---")
st.header("🛠️ Skill Gaps & Missing Areas")
st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{gaps}</div>", unsafe_allow_html=True)

st.markdown("---")
st.header("🚀 Future Roadmap & Preparation Strategy")
st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{roadmap}</div>", unsafe_allow_html=True)

st.success("✅ Analysis Completed Successfully!")

