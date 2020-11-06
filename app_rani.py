# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello World<h1>"

# host_addr = "127.0.0.1"
# port_num = "8080"

if __name__ == "__main__":
    app.run()


