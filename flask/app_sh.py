import math

from flask import Flask, request
from flask import render_template
import pymysql
import urllib.request

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
    return render_template("home.html")

# 포트폴리오 첫 페이지
@app.route("/portfolio")
def homepage():
    return render_template("index.html")

# 배당금 내역
@app.route("/dividend")
def dividend():
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1234', db='service', charset='utf8')
    cur = db.cursor()

    sql = "SELECT * from board"
    cur.execute(sql)

    data_list = cur.fetchall()

    return render_template("qna.html", data_list=data_list)

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