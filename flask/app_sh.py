from flask import Flask, request, flash
from flask import render_template, make_response, session, escape
from bs4 import BeautifulSoup
from kakao_login import *
import functools
import json
import pymysql
import urllib.request
import pandas as pd
import plotly.express as px
import requests
import operator
import openpyxl

app = Flask(__name__)
db_root = pymysql.connect(host='ls-360d5e5827a35e0a46fa340307d68f5a00a3b151.cvbhe0hq8rxv.ap-northeast-2.rds.amazonaws.com', port=3306, user='dbmasteruser', passwd='Qa]HHh]dc1NsX>VLfo<=JA^1GcEWOCY$', db='dbmaster', charset='utf8')
code_count = 0

def db_chart(order):

    db = db_root
    cur = db.cursor()
    sql = "SELECT jongmok_name,jongmok_listcol1 FROM jongmok_list ORDER BY jongmok_listcol1 " + order

    cur.execute(sql)
    data_list = cur.fetchall()

    return data_list

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

    fig1 = px.line(df1, x='date', y='close')

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
    wb.save("templates/jusikdata.xlsx")
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
    chart_data_high = db_chart("DESC")
    chart_list_high = list(chart_data_high)
    high_string = list()

    for i in range(0, 10):
        high_string.append(chart_list_high[i])

    session['highest'] = high_string

    chart_data_low = db_chart("ASC")
    chart_list_low = list(chart_data_low)
    low_string = list()

    for i in range(0, 10):
        low_string.append(chart_list_low[i])

    session['lowest'] = low_string

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
    return render_template("index.html", data=session['userName'], chart_high=session['highest'], chart_low=session['lowest'])

# 배당금 내역
@app.route("/dividend", methods=["GET", "POST"])
def dividend():
    userid = session['userID']
    if request.method == "POST":
        baedang_date = request.form.get("baedang_date")
        name = request.form.get("name")
        baedang_price = request.form.get("baedang_price")

        if baedang_date == "" or name == "" or baedang_price == "":
            return render_template("write_dividend.html")

        db = db_root
        cur = db.cursor()
        sql = "INSERT INTO baedang(id, baedang_date, name, baedang_price) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, (userid, baedang_date, name, baedang_price))
        # sql = "INSERT INTO baedang(id, baedang_date, name, baedang_price) VALUES (%s, %s , %s, %d)"
        # cur.execute(sql, (id, baedang_date, name, baedang_price))
        db.commit()

    db = db_root
    cur = db.cursor()

    sql = "SELECT * from baedang where id='%s'"%(userid)
    cur.execute(sql)

    data_list = cur.fetchall()

    return render_template("dividend.html", data_list=data_list, data=session['userName'])

# 배당금 write
@app.route("/dividend-write")
def dividend_write():
    userid = session['userID']
    db = db_root
    cur = db.cursor()

    sql = "SELECT name from jusik where id='%s'"%(userid)
    cur.execute(sql)

    data_list = cur.fetchall()
    return render_template("write_dividend.html",data_list=data_list, data=session['userName'])

@app.route("/myport", methods=["GET", "POST"])
def myport():
    userid = session['userID']
    if request.method == "POST":
        form = request.form.get("form1")
        print(form)
        if form == "포트폴리오 내역 등록":
            print(form)
            buy_date = request.form.get("buy_date")
            sell_date = request.form.get("sell_date")
            name = request.form.get("name")
            buy_price = request.form.get("buy_price")
            count = request.form.get("count")
            sell_price = request.form.get("sell_price")

            if buy_date == "" or name == "" or buy_price == "" or count == "":
                return render_template("write_myport.html")

            db = db_root
            cur = db.cursor()
            sql = "INSERT INTO jusik(id, buy_date, sell_date, name, buy_price, count, sell_price) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (userid, buy_date, sell_date, name, buy_price, count, sell_price))
            db.commit()
        elif form == "포트폴리오 내역 수정":
            print(form)
            buy_date = request.form.get("buy_date")
            name = request.form.get("name")
            sell_date = request.form.get("sell_date")
            sell_price = request.form.get("sell_price")
            if buy_date == "" or name == "" or sell_date == "" or sell_price == "":
                return render_template("modify_myport.html")

            db = db_root
            cur = db.cursor()
            cur1 = db.cursor()
#            sql = "SELECT * from jusik where id='%s' and buy_date='%s' and name='%s'"%(userid, buy_date, name)
#            cur.execute(sql)
#            d_list = cur.fetchall()
#            if d_list == '':
#                return render_template("modify_myport.html")

            sql1 = "UPDATE jusik SET sell_date='%s', sell_price='%s' where id='%s' and buy_date='%s' and name='%s'"%(sell_date, sell_price, userid, buy_date, name)
            cur1.execute(sql1)
            db.commit()


    db = db_root
    cur = db.cursor()

    sql = "SELECT * from jusik where id='%s'"%(userid)
    cur.execute(sql)

    data_list = cur.fetchall()

    return render_template("myport.html", data_list=data_list, data=session['userName'])

# 포트폴리오 내역 write
@app.route("/myport-write")
def myport_write():
    db = db_root
    cur = db.cursor()

    sql = "SELECT jongmok_name from jongmok_list"
    cur.execute(sql)

    data_list = cur.fetchall()
    return render_template("write_myport.html", data_list=data_list, data=session['userName'])

# 포트폴리오 내역 modify
@app.route("/myport-modify")
def myport_modify():
    userid = session['userID']
    db = db_root
    cur = db.cursor()

    sql = "SELECT name from jusik where id='%s' and sell_date='0000-00-00'"%(userid)
    cur.execute(sql)

    data_list = cur.fetchall()
    return render_template("modify_myport.html", data_list=data_list, data=session['userName'])

# 투자 현황
@app.route("/invest")
def invest():
    userid = session['userID']
    db = db_root
    cur = db.cursor()

    sql = "SELECT jusik.id, jusik.buy_date, jusik.sell_date, jusik.name, jusik.buy_price, jusik.count, jusik.sell_price, jongmok_list.jongmok_name, jongmok_list.jongmok_listcol, jongmok_list.jongmok_listcol1 from jusik, jongmok_list where jusik.id='%s' and jusik.name=jongmok_list.jongmok_name and jusik.sell_date='0000-00-00'"%(userid)
    cur.execute(sql)

    data_list = cur.fetchall()
    print(data_list)

    return render_template("invest.html", data_list=data_list, data=session['userName'])

# 실현 손익
@app.route("/monthly")
def monthly():
    userid = session['userID']
    db = db_root
    cur = db.cursor()
    cur2 = db.cursor()
    cur3 = db.cursor()

    sql = "SELECT * from jusik where id='%s' and sell_date!='0000-00-00'"%(userid)
    sql2 = "SELECT sum((sell_price-buy_price)*count) from jusik where id='%s' and sell_date!='0000-00-00'"%(userid)
    sql3 = "SELECT sum(baedang_price) from baedang where id='%s'"%(userid)

    cur.execute(sql)
    cur2.execute(sql2)
    cur3.execute(sql3)

    data_list = cur.fetchall()
    price_s = cur2.fetchall()
    price_b = cur3.fetchall()
    if price_s[0][0] and price_b[0][0]:
        return render_template("monthly.html", data_list=data_list, price_s=price_s[0][0], price_b=price_b[0][0], data=session['userName'])
    else:
        return render_template("monthly.html", data_list=data_list, price_s=0, price_b=0, data=session['userName'])

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
    app.run(host="0.0.0.0", port="5000")