import csv

def save_to_csv(jobs):
  # 파일 열기 단, 파일이 없을 경우 생성해줌
  # mode 3가지 설명
  file = open("jobs.csv", mode="w")
  
  # csv를 작성할 수 있도록 하는 변수 생성
  writer = csv.writer(file)

  # row(행)의 값 추가
  writer.writerow(["title", "company", "location", "link"])

  for job in jobs:
    # 딕셔너리에 저장된 값중 Value만 가지고 와서 row의 값 추가
    # 단, dict.value()의 경우 type이 dict_value 이므로 list로 변환하여 저장해야 함
    writer.writerow(list(job.values()))