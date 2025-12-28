import fitz # PyMuPDF
import os
from dotenv import load_dotenv
from apify_client import ApifyClient
from groq import Groq

load_dotenv()
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY  # Ensure GROQ_API_KEY is set for groq library
os.environ["APIFY_API_TOKEN"] = APIFY_API_TOKEN  # Ensure APIFY_API_TOKEN is set for apify-client library

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

apify_client = ApifyClient(os.environ.get("APIFY_API_TOKEN"))

def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file."""
    doc = fitz.open(stream = uploaded_file.read(), filetype = "pdf")
    text = ""
    
    for page in doc:
        text += page.get_text()

    return text


def ask_groqai(prompt,max_tokens=500):
    """Send a prompt to GroqAI and return the response."""
    response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="llama-3.3-70b-versatile",
    max_tokens=max_tokens,
    temperature=0.4

    )
    return response.choices[0].message.content


def fetch_linkeding_jobs(search_query,location='india',rows=60):
    """Fetch job listings from LinkedIn using Apify."""
    run_input = {
        "title": search_query,
        "rows":rows,
        "location":location,
        "proxy":{
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"]
        }
        
    }

    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs


def fetch_naukri_jobs(search_query,location='india',limit=60):
    """Fetch job listings from Naukri using Apify."""
    run_input = {
    "keyword": search_query,
    "maxJobs":rows,
    "freshness":"all",
    "sortBy":"relevance",
     "experience":"all",
    "proxyConfiguration": { "useApifyProxy": False },
    }

    run = apify_client.actor("wsrn5gy5C4EDeYCcD").call(run_input=run_input)