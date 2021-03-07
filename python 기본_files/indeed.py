#페이지 접속
#얼마나 많은 페이지일까?
#indeed 고급 잡 서치

#1단계: requests 와 beautifulsoup4 가져오기
#requets 공부 참고: https://github.com/psf/requests
#beautifulsoup4 공부 참고: https://pypi.org/project/beautifulsoup4/
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/


#2단계: 페이지 접속하기 
# indeed_result = requests.get("https://www.indeed.co.uk/jobs?q=python&limit=50")
# indeed_soup = BeautifulSoup(indeed_result.text, "html.parser")

#3단계: 홈페이지 들어가서 구조 보고 선택자 넣기
#div 요소의 클래스가 pagination이라는 뜻임. 
#.find(): 하나만 찾는다.
#.find_all: 해당하는 모두를 찾는다.
# pagination = indeed_soup.find("div", {"class":"pagination"})
# links = pagination.find_all('li')

#4단계: 빈 리스트 생성 
# pages = []


#5단계: pages에 있는 'li'들에게..: find_all의 결과는 list
# 각각 span이 있으면 spans에 놓거라.
# append(a)> a를 리스트 뒤에 달기 
#conquer and devide가 중요하다. 두 개 이상 연속해서 메소드를 붙이면 실행이 안됨.
#[1:-1]은 두 번째 요소부터 마지막에서 하나 제외하고~ 라는 의미다.


#for link in links[1:-1]:
#  pages.append(int(link.string))


#max_page = pages[-1]
#print(range(max_page))

#for n in range(max_page):
#    print(f"start={n*50}")

#이하 구조는 스크래핑 할 사이트에 따라 달라질 수 있다.

#함수를 만든다는 건, 코드를 재사용할 수 있다는 것.  

#빈칸 없애기: python strip

#.string 메소드를 사용하기 어려울 경우: none이 출력되면 .string 메소드를 사용하기 어렵다. 

#url과 연결하여 웹사이트로 연결시키기

#id는 하나밖에 없으므로 바로 찾기 가능! html["id값"]

import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.co.uk/jobs?q=python&limit={LIMIT}"

def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.find("div", {"class":"pagination"})

    links = pagination.find_all('li')
    pages = []

    for link in links[1:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find("h2", {"class":"title"}).find("a")["title"]
    company = html.find("span", {"class":"company"})
    company_anchor = company.find("a")
    if company_anchor != None:
        company = company_anchor.string
    else:
        company = company.string
    company = company.strip()
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {
        'title': title, 
        'company': company, 
        'location': location, 
        "link": f"https://www.indeed.co.uk/viewjob?jk={job_id}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed: page {page}")
        result = requests.get(f"{URL}&start={0*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results: 
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs






