from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello World!</h1>"

@app.route("/abc")
def abc():
    a = "{1:aa, 2:bb}"
    return a

@app.route("/univ/<aaa>")
def univ(aaa):
    a = aaa
    return a

@app.route("/message/<string:message_id>")
def get_message(message_id):
    print(type(message_id))
    return "message id : %s" % message_id

@app.route("/first/<int:messageid>")
def get_first(messageid):
    print(type(messageid))
    return "<h1>%d</h1>" % (messageid + 5)

@app.route("/<user>")
def test(user):
    return user

@app.route("/test")
def get_html():
    return render_template("view.html", data="전달메시지")

@app.route("/test1")
def get_html1():
    return render_template("view.html", aa="전달메시지", bb="1234", cc=[1, 2, 3])

@app.route("/hello")
def hello_flask():
    return "<h1>Hello Flask!</h1>"

@app.route("/first")
def hello_first():
    return "<h3>Hello First!<h3>"

@app.route("/index")
def index():
    return render_template("index.html", aaa="Hi My Homepage!")

if __name__ == "__main__":
    app.run()


"""
host_addr = "127.0.0.1"
port_num = "8080"

if __name__ == "__main__":
    app.run(host=host_addr, port=port_num)
"""