import streamlit as st
from src.helper import extract_text_from_pdf,ask_groqai
from src.job_api import fetch_linkeding_jobs,fetch_naukri_jobs


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

    if st.button("🔄 Get Job Recommendations"):
        with st.spinner("Generating job recommendations..."):
            keywords = ask_groqai(
                f"Based on this resume summary suggest the best job title's and keywords for searching job. Give a comma separated list only, no explanations,:\n\n{summary}",
                max_tokens=100
            )
            search_keywords = keywords.replace("\n","").strip()
        st.success(f"Extracted Job Search Keywords: {search_keywords}")

        with st.spinner("Fetching Jobs from Linkedin and Naukri..."):
            linkeding_jobs = fetch_linkeding_jobs(search_keywords,rows=60)
            naukri_jobs = fetch_naukri_jobs(search_keywords,rows=60)
        st.markdown("---")
        st.header("💼 Top LinkedIn Jobs")

        if linkedin_jobs:
            for job in linkedin_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- 📍 {job.get('location')}")
                st.markdown(f"- 🔗 [View Job]({job.get('link')})")
                st.markdown("---")
        else:
            st.warning("No LinkedIn jobs found.")

        st.markdown("---")
        st.header("💼 Top Naukri Jobs (India)")

        if naukri_jobs:
            for job in naukri_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- 📍 {job.get('location')}")
                st.markdown(f"- 🔗 [View Job]({job.get('url')})")
                st.markdown("---")
        else:
            st.warning("No Naukri jobs found.")    
