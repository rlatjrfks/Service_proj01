from flask import Flask
from flask import render_template
import pymysql

app = Flask(__name__)
#
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

@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")
# @app.route("/")
# def hello():
#     return "<h1>Hello World!</h1>"
#
# @app.route("/abc")
# def hello2():
#     a ="{1:aa, 2:bb}"
#     return a
#
# @app.route("/message/<string:message_id>")
# def get_message(message_id):
#     print(type(message_id))
#     return"message id :%s" %message_id
#
# @app.route("/first/<int:messageid>")
# def get_first(messageid):
#     print(type(messageid))
#     return "<h1>%d</h1>" % (messageid+5)
#
# @app.route("/<user>")
# def test(user):
#     return user
#
# @app.route("/hello/<users>")
# def hello_name(user):
#     return render_template("index_test.html", data=user)

if __name__ == "__main__":
    app.run()