from indeed import get_jobs as get_indeed_jobs 
from stackoverflow import get_jobs as get_stackoverflow_jobs
from save_to_csv import save_to_csv

# Indeed Site 스크랩
indeed_jobs = get_indeed_jobs() 

# StackOverflow 스크랩
stackoverflow_jobs = get_stackoverflow_jobs() 

# Indeed + StackOverflow 스크랩 자료 합치기
jobs = indeed_jobs + stackoverflow_jobs

# csv로 저장하기
save_to_csv(jobs)