import requests
from bs4 import BeautifulSoup

LIMIT = 50

URL = "https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def extract_indeed_pages():
    result = requests.get(URL)

    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.find("div", {"class":"pagination"})

    links = pagination.find_all('a')

    pages = []

    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]

    return max_page

def extract_job(html):
    title = html.find("h2", {"class": "jobTitle"}).find("span", title=True).string
    company = html.find("span", {"class":"companyName"})
    company_anchor = company.find("a")
    if company_anchor is not  None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    location = html.find("div", {"class":"companyLocation"}).text
    job_id = html["data-jk"]
    return {'title': title,'company': company, 'location':location, 'link': f"https://www.indeed.com/viewjob?jk={job_id}"}

def extract_indeed_jobs(last_page):
    jobs= []
    for page in range(last_page):
        print(f"Scrapping page{page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("a", {"class":"tapItem"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs