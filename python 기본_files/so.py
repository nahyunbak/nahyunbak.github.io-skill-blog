import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://stackoverflow.com/jobs?q=python&sort=i"


#.get_text(): 태그 안의 빈칸을 가져온다. 참고로 이건 string이다. 그래서 int로 정수형으로 바꿔줌.
# get_text 괄호 안 strip=True은 빈칸을 지워준다. 
# 파이썬은 같은 변수명을 사용할 수 있다. ..def안에서만 사용 가능하지. 
#status_code로 상태를 확인할 수 있다.
def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class":"s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


#for에 들어가는 건 하나만 찾으면 된다. 
#recursive=False   바로 아래 요소들(1단계만 가져옴
#(파이썬 기능: 리스트에 두 개의 요소가 있다는 걸 알고 있을 때) 
#.string 문자열
#쓸모없는 단어 제외 :    .strip("N.A.") ..쓸데없는 단어 없애기    .strip("\n") ..새로운 줄 없애기 
#때로는 문제에 집중하는 것도 좋다. 
def extract_job(html):
    title = html.find("a", {"class":"s-link stretched-link"})['title']
    company, location =html.find("h3", {"class":"fc-black-700 fs-body1 mb4"}).find_all("span", recursive=False)
    company = company.get_text(strip=True).strip("N.A.")
    location = location.get_text(strip=True)
    job_id = html.find("h2",{"class":"fs-body3"}).find("a")["href"]
    return {'title': title, 'company': company, 'location':location, "apply_link":f"https://stackoverflow.com/jobs/{job_id}"}


def extract_jobs(last_page): 
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: page : {page}")
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class":"grid--cell fl1"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)            
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs



#result.에 위에 extract_job 하는 거. 사실, title과 result를 붙여 써도 괜찮음
