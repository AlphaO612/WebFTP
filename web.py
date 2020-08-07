from flask import Flask, redirect, url_for, request, send_from_directory
from random import randint
import os

app = Flask(__name__)

token = randint(100000, 999999)

pwd = os.getcwd()
dir = os.listdir(pwd)

@app.route("/")
def index():
    return str(token)

def readStorage(name):
    f = open(name, 'r')
    set = f.read()
    f.close()
    return set

@app.route(f"/file/{token}", methods=['GET'])
def files():
    if not request.args.get('path', '') == '':
        pwd = request.args.get('path', '')
        if os.path.isdir(pwd):
            pwd = request.args.get('path', '')
            dir = os.listdir(pwd)
            text = ''
            for i in dir:
                if os.path.isfile(pwd + '/' + i):
                    text += f'<br><a href="/file/{token}?path={pwd}/{i}">{i}</a> - <a href="/file/{token}/{os.path.basename(pwd + "/" + i)}?path={pwd}" style="color: red;" download>(!)</a>'
                else:
                    text += f'<br><a href="/file/{token}?path={pwd}/{i}">{i}</a>'
            return f'<h3> files in {pwd}</h3>' + text
        else:
            return readStorage(pwd)
    else:
        pwd = os.getcwd()
        dir = os.listdir(pwd)
        return redirect(url_for('files', path=pwd))

@app.route(f"/file/{token}/<filename>", methods=['GET'])
def dl(filename):
    pwd = request.args.get('path', '')
    return send_from_directory(pwd, filename)
    
with app.test_request_context():
    print(f"--------------------------------------------------\nSite - {url_for('files', path=pwd)}\n--------------------------------------------------")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
