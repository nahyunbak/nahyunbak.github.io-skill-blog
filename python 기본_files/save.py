#파이썬에는 csv를 다룰 수 있는 기능이 탑재되어 있다.

import csv

#open은 찾아주거나, 생성해준다. 
#mode="w" : 쓰기 전용 (open을 다시 실행하면 사라진다)      mode="r": 읽기전용
#csv.writer(file) : 괄호 안에는 어떤 file에 write할 것인지가 들어간다.
def save_to_file(jobs):
    file = open("jobs.csv", mode="w", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow(["title", "company", "location", "link"])
    for job in jobs:
        writer.writerow(list(job.values()))
    return 