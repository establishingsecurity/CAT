from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello():
    print("serving website")
    return render_template('simple.html')

@app.route('/sendAccounts', methods=['GET','POST'])
def getAccounts():
    print("getting accounts")
    data = request.data
    print(data)
    return "done"

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True)