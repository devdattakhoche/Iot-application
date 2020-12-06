from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/')
def home():
    file1 = open("data.txt" , "r")
    data = file1.readlines()
    final = {}
    for d in data:
        d = d.replace("\n", "")
        temp = d.split(',')
        temp_dict  = {}
        for i in temp:
            temp_dict[i] = i
        final[temp[0]] = temp_dict
    file1.close()
    print(final['Rainbow Beach'])
    return render_template('home.html', resp=final)

@app.route('/getData')
# @cross_origin(support_credentials=True)
def getData():
    file1 = open("data.txt" , "r")
    data = file1.readlines()
    final = {}
    for d in data:
        d = d.replace("\n", "")
        temp = d.split(',')
        final[temp[0]] = temp
    final = jsonify(final)
    file1.close()
    return final

@app.route('/safety')
def safety():
    return render_template('safety.html')

if __name__ == '__main__':
    app.run(debug=True)