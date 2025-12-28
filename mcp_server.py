from mcp.server.fastmcp import FastMCP
from src.job_api import fetch_linkeding_jobs,fetch_naukri_jobs

mcp = FastMCP("Job Recommender")


@mcp.tool()
async def fetch_jobs(listofkey):
    """Fetch job listings from LinkedIn and Naukri using Apify."""
    linkeding_jobs = fetch_linkeding_jobs(listofkey,rows=60)
    naukri_jobs = fetch_naukri_jobs(listofkey,rows=60)
    return {
        "linkeding_jobs": linkeding_jobs,
        "naukri_jobs": naukri_jobs
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")