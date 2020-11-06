from flask import Flask

app = Flask(__name__)
@app.route("/")
def hello():
    return "<h1>Hello Service World!</h1>"

@app.route("/hello")
def hello_flask():
    return "<h1>Hello Flask!</h1>"

@app.route("/first")
def hello_first():
    return "<h3>Hello First</h3>"
#YSH

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")

@app.route("/univ/<aaa>")
def hello3(aaa):
    a = aaa
    return a

@app.route("/message/<string:message_id>")
def get_message(message_id):
    print(type(message_id))
    return "message id: %s" % (message_id)

    #return "<h1>%d</h1>" % (messageid+5)
