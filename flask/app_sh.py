import math

from flask import Flask, request
from flask import render_template
import pymysql
import urllib.request
import pandas as pd
# 필요한 모듈 import 하기
import plotly.express as px
import plotly.io as po

app = Flask(__name__)

# @app.route("/")
# def hello():
#     db = pymysql.connect(host='127.0.0.1',
#                          port=3306, user='root', passwd='@science9110',
#                          db='test', charset='utf8')
#     cursor = db.cursor()
#     sql = 'select * from test.table1'
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     print(result[0][0])
#     data = result[0]
#     print(type(data))
#     db.close()
#
#     return str(data)

# return "<h1>hellowolrd!</h1>"

# #기능
# 기본 페이지 실습중
# @app.route("/")
# def crawling():
#     return render_template("index2.html")

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
        df1 = df.append(pd.read_html(url, header=0)[0], ignore_index=True)

    # df.dropna()를 이용해 결측값 있는 행 제거
    df1 = df1.dropna()

    df1 = df1.rename(columns={'날짜': 'date', '체결가': 'close'})
    # 데이터의 타입을 int형으로 바꿔줌
    df1['close', 'volume'] = df1['close'].astype(int)

    # 컬럼명 'date'의 타입을 date로 바꿔줌
    df1['date'] = pd.to_datetime(df1['date'])

    # 반응형 그래프 그리기
    fig1 = px.line(df, x='date', y='close', title='코스닥 지수')

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

    return render_template("home.html")

# 코스피
@app.route("/kospi")
def kospi():
    return render_template("kospi_g.html")

# 코스닥
@app.route("/kosdaq")
def kosdaq():
    return render_template("kosdaq_g.html")

# 포트폴리오 첫 페이지
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
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='@science9110', db='test', charset='utf8')
    cur = db.cursor()

    sql = "SELECT * from board"
    cur.execute(sql)

    data_list = cur.fetchall()

    return render_template("qna.html", data_list=data_list)

# 회원가입, 로그인
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/password")
def password():
    return render_template("password.html")

@app.route("/register")
def register():
    return render_template("register.html")

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