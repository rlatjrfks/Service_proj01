from flask import Flask, request, redirect, url_for, render_template
import math
import json
import requests
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

@app.route('/oauth')
def oauth():
    code = str(request.args.get('code'))
    #return str(code)

    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=authorization_code&client_id=7de6eba98a900d9c18e21fedc74b92ae&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Foauth&code=" + str(code)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
         }
    response = requests.request("POST", url, data=payload, headers=headers)
    access_token = json.loads(((response.text).encode('utf-8')))['access_token']
    #return access_token

    url = "https://kapi.kakao.com/v1/user/signup"

    headers.update({'Authorization': "Bearer" + str(access_token)})
    response = requests.request("GET", url, headers=headers)

    url = "https://kapi.kakao.com/v2/user/me"
    response = requests.request("POST", url, headers=headers)
    return (response.text)

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
    #app.run(debug=True)
    app.debug = True
    app.config['DEBUG'] = True
    app.run()
    # app.run(host="0.0.0.0", port="5000")