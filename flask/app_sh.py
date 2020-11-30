from flask import Flask
from flask import render_template
import pymysql

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

#기능
@app.route("/portfolio")
def homepage():
    return render_template("index.html")

@app.route("/static_sidenavigation")
def static_sidenavigation():
    return render_template("layout-sidenav-light.html")


@app.route("/static_navigation")
def static_navigation():
    return render_template("layout-static.html")

@app.route("/tables")
def tables():
    return render_template("tables.html")

@app.route("/charts")
def charts():
    return render_template("charts.html")

#회원가입, 로그인
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/password")
def password():
    return render_template("password.html")

@app.route("/register")
def register():
    return render_template("register.html")

#에러 페이지
@app.errorhandler(404)
def page_not_found(error):
    return render_template("500.html")

@app.errorhandler(401)
def permission_error(error):
    return render_template("401.html")

@app.errorhandler(500)
def connetion_error(error):
    return render_template("500.html")


if __name__ == "__main__":
    app.run()