import requests
from bs4 import BeautifulSoup

LIMIT = 50
# 스크래핑 하려는 URL 저장
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


# "Indeed" 웹사이트를 스크래핑 하는 Function 생성
def extract_pages():

    # url에 저장된 웹사이트를 requestsdml get Function을 사용하여 가져오기
    result = requests.get(URL)

    # # html을 text로 가져오기
    # print(result.text)
    # bs4를 이용하여 "Indeed" 검색 결과를 html로 가져오기
    soup = BeautifulSoup(result.text, 'html.parser')

    # "div" Tag 중 Class가 "pagination"인 것 가져오기
    pagination = soup.find("div", {"class": "pagination"})
    # "pagination" 변수에 저장된 html 중에서 "anchor" Tag 인 것 모두 가져와서 리스트로 저장
    links = pagination.find_all("a")

    # span을 저장할 빈 리스트 객체 생성
    pages = []
    # "links" 리스트에 저장된 값을 차례대로 "link"라는 객체로 받아온 후 "span" Tag 인 것을 "pages" 리스트에 추가 # [:-1] = "links" 리스트에 저장된 값 중 마지막 값을 제외한다는 뜻
    for link in links[:-1]:
        # pages.append(link.find("span").string)
        # anchor Tag의 String을 가지고 와도 span의 String을 가지고 온다
        pages.append(int(link.string))

        # # "pages" 리스트에 저장된 값 중 마지막에서 1번째 item
        # print(pages[-1])

        # "pages"에 저장된 값 중 가장 큰 값(마지막 값)만 가져오기
        max_page = pages[-1]

    return max_page


def extract_job(html):
    # h2 Tag중 클래스가 title 인것 중에서 anchor Tag속의 attribute 가 "title"인 것
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})

    # company 중에 "a" Tag가 있는 경우
    if company.find("a") is not None:
        company = str(company.find("a").string)
    else:
        company = str(company.string)

    # company 값의 앞/뒤에 있는 공백 삭제하기
    company = company.strip()

    # # locaiton 값이 없는 일자리가 있어서 None이 출력 되는 경우 발생
    # location = html.find("span", {"class":"location"})
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]

    job_id = html["data-jk"]

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://www.indeed.com/viewjob?jk={job_id}"
    }


def extract_jobs(last_pages):
    jobs = []
    for page in range(last_pages):
        print(f"Scrapping Indeed Page : {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')

        # Indeed에서 각 직업별 정보를 리스트로 가져오기
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
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
