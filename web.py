from flask import Flask, redirect, url_for, request, send_from_directory, flash
from random import randint
import os

app = Flask(__name__)

token = 0# randint(100000, 999999)

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

@app.route(f"/files", methods=['GET'])
def files():
    global token
    if request.args.get('token', '') == str(token):
        if not request.args.get('path', '') == '':
            pwd = request.args.get('path', '')
            if os.path.isdir(pwd):
                pwd = request.args.get('path', '')
                dir = os.listdir(pwd)
                text = ''
                for i in dir:
                    if os.path.isfile(pwd + '/' + i):
                        text += f'<br><a href="{url_for("files", path=pwd+"/"+i, token=token)}">{i}</a> - <a href="{url_for("dl", path=pwd, token=token, filename=i)}" style="color: red;" download>(!)</a>'
                    else:
                        text += f'<br><a href="{url_for("files", path=pwd+"/"+i, token=token)}">{i}</a>'
                return f'<h3> files in {pwd}-----<a href="{url_for("gain", path=pwd, token=token)}" style="color: #9400d3;">Load</a></h3>' + text
            else:
                return readStorage(pwd)
        else:
            pwd = os.getcwd()
            dir = os.listdir(pwd)
            return redirect(url_for('files', path=pwd, token=token))
    else:
        token = randint(100000, 999999)
        print(token)
        return '<h1>Ops...</h1><p>token was change!</p>'

@app.route(f"/file/<filename>", methods=['GET'])
def dl(filename):
    global token
    global pwd
    print(filename)
    if request.args.get('token', '') == str(token):
        print('hah')
        pwd = request.args.get('path', '')
        return send_from_directory(pwd, filename)
    else:
        token = randint(100000, 999999)
        print(token)
        return '<h1>Ops...</h1><p>token was change!</p>'

@app.route(f"/file/upload", methods=['GET', 'POST'])
def gain():
    global token
    global pwd
    if request.args.get('token', '') == str(token):
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and file.filename:
                # filename = file.filename
                # file.save(os.path.join(pwd, filename))
                for file in request.files.getlist('file'):
                    print(file)
                    print(file.name)
                    file.save(os.path.join(pwd, file.filename))
                return redirect(url_for('files', path=pwd))
        else:
            pwd = request.args.get('path', '')
            return f'<h3>Upload file(s) in {pwd}</h3><form enctype="multipart/form-data" method="POST"><p><input type="file" name="file" required multiple title="Upload..."><input name="token" value="{token}" hidden="true"></p><p><a href="{url_for("files", path=pwd, token=token)}">Back</a> <input type="submit" value="Load"></p> </form>'
    else:
        token = randint(100000, 999999)
        print(token)
        return '<h1>Ops...</h1><p>token was change!</p>'

with app.test_request_context():
    print(f"--------------------------------------------------\nSite - {url_for('files', path=pwd, token=token)}\n--------------------------------------------------")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
