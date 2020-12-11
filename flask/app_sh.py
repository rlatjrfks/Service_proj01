from flask import Flask, request
from flask import render_template
import pymysql
import urllib.request
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup
import openpyxl

app = Flask(__name__)

# 홈
@app.route("/")
def first():
    # 코스피
    df = pd.DataFrame()
    for page in range(1, 21):
        url = 'https://finance.naver.com/sise/sise_index_day.nhn?code=KOSPI'
        url = '{url}&page={page}'.format(url=url, page=page)
        # print(url)
        df = df.append(pd.read_html(url, header=0)[0], ignore_index=True)

    # df.dropna()를 이용해 결측값 있는 행 제거
    df = df.dropna()

    df = df.rename(columns={'날짜': 'date', '체결가': 'close'})
    # 데이터의 타입을 int형으로 바꿔줌
    df['close', 'volume'] = df['close'].astype(int)

    # 컬럼명 'date'의 타입을 date로 바꿔줌
    df['date'] = pd.to_datetime(df['date'])

    # 반응형 그래프 그리기
    fig = px.line(df, x='date', y='close')

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig.write_html("templates/kospi_g.html")


    # 코스닥
    df1 = pd.DataFrame()
    for page in range(1, 21):
        url1 = 'https://finance.naver.com/sise/sise_index_day.nhn?code=KOSDAQ'
        url1 = '{url}&page={page}'.format(url=url1, page=page)
        # print(url)
        df1 = df1.append(pd.read_html(url1, header=0)[0], ignore_index=True)

    # df.dropna()를 이용해 결측값 있는 행 제거
    df1 = df1.dropna()

    df1 = df1.rename(columns={'날짜': 'date', '체결가': 'close'})
    # 데이터의 타입을 int형으로 바꿔줌
    df1['close', 'volume'] = df1['close'].astype(int)

    # 컬럼명 'date'의 타입을 date로 바꿔줌
    df1['date'] = pd.to_datetime(df1['date'])

    fig1 = px.line(df1, x='date', y='close', title='코스닥 지수')

    fig1.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig1.write_html("templates/kosdaq_g.html")


    # 주식 데이터 크롤링
    # 내가 작업할 Workbook 생성하기
    wb = openpyxl.Workbook()

    # 작업할 Workbook 내 Sheet 활성화
    sheet = wb.active

    # 데이터 프레임 생성
    sheet.append(["종목명", "현재가"])

    # 데이터 크롤링
    for i in range(1, 40):
        raw = requests.get("https://finance.naver.com/sise/sise_market_sum.nhn?&page=" + str(i))
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
    wb.save("templates/주식데이터.xlsx")

    return render_template("home.html")

# 코스피
@app.route("/kospi")
def kospi():
    return render_template("kospi_g.html")

# 코스닥
@app.route("/kosdaq")
def kosdaq():
    return render_template("kosdaq_g.html")


# 웹 페이지
# 포트폴리오
@app.route("/portfolio")
def homepage():
    return render_template("index.html")

# 배당금 내역
@app.route("/dividend")
def dividend():
    return render_template("dividend.html")

# 투자 현황
@app.route("/invest")
def invest():
    return render_template("invest.html")

# 월간 이력
@app.route("/monthly")
def monthly():
    return render_template("monthly.html")

# 이용 가이드
@app.route("/guide")
def guide():
    return render_template("guide.html")

# Q & A
@app.route("/qna")
def qna():
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234', db='service', charset='utf8')
    cur = db.cursor()

    sql = "SELECT * from board"
    cur.execute(sql)

    data_list = cur.fetchall()

    return render_template("qna.html", data_list=data_list)



# 로그인
@app.route("/login")
def login():
    return render_template("login.html")



# 에러 페이지
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")

@app.errorhandler(401)
def permission_error(error):
    return render_template("401.html")

@app.errorhandler(500)
def connetion_error(error):
    return render_template("500.html")


if __name__ == "__main__":

    app.debug = True
    app.config['DEBUG'] = True
    app.run()
    # app.run(host="0.0.0.0", port="5000")