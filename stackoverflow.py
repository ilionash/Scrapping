import requests
from bs4 import BeautifulSoup

# 스크래핑 하려는 URL 저장
URL = f"https://stackoverflow.com/jobs?q=python"

def extract_pages():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")

  pages = soup.find("div", {"class":"s-pagination"}).find_all("a")

  last_page = pages[-2].get_text(strip=True)
  
  return int(last_page)

def extract_job(html):
  title = html.find("h2").find("a")["title"]
  company, location  = html.find("h3").find_all("span", recursive=False)
  company = company.get_text(strip=True)
  location = location.get_text(strip=True).strip("-").strip(" \r").strip("\n")
  job_id = html["data-jobid"]

  return{
    "title": title,
    "company": company,
    "location": location,
    "link": f"https://stackoverflow.com/jobs/{job_id}"
  }


def extract_jobs(last_pages):
    jobs = []
    for page in range(last_pages):
        print(f"Scrapping StackOverFlow Page : {page}")
        result = requests.get(f"{URL}&pg={page}")
        soup = BeautifulSoup(result.text, 'html.parser')

        # Indeed에서 각 직업별 정보를 리스트로 가져오기
        results = soup.find_all("div", {"class": "-job"})
        # 여러개의 결과에서 1개 일자리에 대한 정보 찾기
        for result in results:
            job = extract_job(result)

            jobs.append(job)

    return jobs


def get_jobs():
    # "indeed" Object의 "extract_pages" Function 호출
    last_page = extract_pages()
    # "indeed" Object의 "extract_jobs" Function 호출
    jobs = extract_jobs(last_page)

    return jobs
