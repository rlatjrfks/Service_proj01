from flask import Flask, request, flash
from flask import render_template, make_response, session, escape
import json
import pymysql
import urllib.request
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup
import openpyxl
from kakao_login import *

app = Flask(__name__)
db_root = pymysql.connect(host='ls-360d5e5827a35e0a46fa340307d68f5a00a3b151.cvbhe0hq8rxv.ap-northeast-2.rds.amazonaws.com', port=3306, user='dbmasteruser', passwd='Qa]HHh]dc1NsX>VLfo<=JA^1GcEWOCY$', db='dbmaster', charset='utf8')
code_count = 0
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
    fig = px.line(df, x='date', y='close', title='코스피 지수')

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
    sheet.append(["종목명", "현재가", "등락률"])

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
                span = ta.select("td.number > span")
                if name == None:
                    continue
                sheet.append([name.text, money.text, span[1].text])

    # 작업 마친 후 파일 저장
    wb.save("templates/주식데이터.xlsx")
    session.clear()
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
    global key
    global code_count
    if code_count == 0:
        code = code_login()
        key = str(request.args.get('code'))
        code.save_token(key)

        auth, id_db, name = code.code_auth(key)
        session['userID'] = id_db
        session['userName'] = name
        code_count = 1
    return render_template("index.html", data=session['userName'])

# 배당금 내역
@app.route("/dividend", methods=["GET", "POST"])
def dividend():
    if request.method == "POST":
        # id = request.form.get("id")
        baedang_date = request.form.get("baedang_date")
        name = request.form.get("name")
        baedang_price = request.form.get("baedang_price")

        if id == "" or baedang_date == "" or name == "" or baedang_price == "":
            return render_template("write_dividend.html")

        db = db_root
        cur = db.cursor()
        sql = "INSERT INTO baedang(baedang_date, name, baedang_price) VALUES (%s, %s, %s)"
        cur.execute(sql, (baedang_date, name, baedang_price))
        # sql = "INSERT INTO baedang(id, baedang_date, name, baedang_price) VALUES (%s, %s , %s, %d)"
        # cur.execute(sql, (id, baedang_date, name, baedang_price))
        db.commit()

    db = db_root
    cur = db.cursor()

    sql = "SELECT * from baedang"
    cur.execute(sql)

    data_list = cur.fetchall()

    return render_template("dividend.html", data_list=data_list, data=session['userName'])

# 배당금 write
@app.route("/dividend-write")
def dividend_write():
    return render_template("write_dividend.html", data=session['userName'])

@app.route("/myport", methods=["GET", "POST"])
def myport():
    if request.method == "POST":

        # id = request.form.get("id")
        buy_date = request.form.get("buy_date")
        sell_date = request.form.get("sell_date")
        name = request.form.get("name")
        buy_price = request.form.get("buy_price")
        buy_count = request.form.get("buy_count")
        sell_price = request.form.get("sell_price")
        sell_count = request.form.get("sell_count")

        if id == "" or buy_date == "" or name == "" or buy_price == "" or buy_count == "":
            return render_template("write_myport.html")

        db = db_root
        cur = db.cursor()
        sql = "INSERT INTO jusik(buy_date, sell_date, name, buy_price, buy_count, sell_price, sell_count) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (buy_date, sell_date, name, buy_price, buy_count, sell_price, sell_count))
        # sql = "INSERT INTO baedang(id, baedang_date, name, baedang_price) VALUES (%s, %s , %s, %s)"
        # cur.execute(sql, (id, baedang_date, name, baedang_price))
        db.commit()

    db = db_root
    cur = db.cursor()

    sql = "SELECT * from jusik"
    cur.execute(sql)

    data_list = cur.fetchall()

    return render_template("myport.html", data_list=data_list, data=session['userName'])

# 포트폴리오 내역 write
@app.route("/myport-write")
def myport_write():
    return render_template("write_myport.html", data=session['userName'])

# 투자 현황
@app.route("/invest")
def invest():
    db = db_root
    cur = db.cursor()

    sql = "SELECT * from jusik"
    # sql2 = "SELECT * from jongmok_list where = "

    cur.execute(sql)

    data_list = cur.fetchall()

    return render_template("invest.html", data_list=data_list, data=session['userName'])

# 실현 손익
@app.route("/monthly")
def monthly():
    db = db_root
    cur = db.cursor()

    sql = "SELECT * from jusik"
    # sql2 = "SELECT * from jongmok_list where = "

    cur.execute(sql)

    data_list = cur.fetchall()

    return render_template("monthly.html", data_list=data_list, data=session['userName'])

# 이용 가이드
@app.route("/guide")
def guide():
    return render_template("guide.html", data=session['userName'])

# Q & A
@app.route("/qna", methods=["GET", "POST"])
def qna():
    if request.method == "POST":
        title = request.form.get("title")
        writer = session['userID']
        context = request.form.get("context")

        if title == "" or writer == "" or context == "":
            return render_template("write_qna.html")

        db = db_root
        cur = db.cursor()
        sql = "INSERT INTO board(title, writer, context) VALUES (%s, %s, %s)"
        cur.execute(sql, (title, writer, context))
        db.commit()

    db = db_root
    cur = db.cursor()

    sql = "SELECT * from board"
    cur.execute(sql)

    data_list = cur.fetchall()

    return render_template("qna.html", data_list=data_list, data=session['userName'])

# Q & A write
@app.route("/qna-write")
def qna_write():
    return render_template("write_qna.html", data=session['userName'])


#로그인
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
    app.secret_key = b'asdf[1#"sdg'
    app.run()