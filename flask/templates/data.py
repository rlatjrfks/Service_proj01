import requests
from bs4 import BeautifulSoup
import openpyxl

# 내가 작업할 Workbook 생성하기
wb = openpyxl.Workbook()

# 작업할 Workbook 내 Sheet 활성화
sheet = wb.active

# 데이터 프레임 생성
sheet.append(["종목명", "현재가"])

# 데이터 크롤링
for i in range(1, 40):
    raw = requests.get("https://finance.naver.com/sise/sise_market_sum.nhn?&page="+str(i))
    html = BeautifulSoup(raw.text, 'html.parser')

    container = html.select("table.type_2 > tbody")

    for con in container:
        table = con.select("tr")
        for ta in table:
            name = ta.select_one("td > a")
            money = ta.select_one("td.number")
            if name == None:
                continue
            sheet.append([name.text, money.text])

# 작업 마친 후 파일 저장
wb.save("주식데이터.xlsx")

