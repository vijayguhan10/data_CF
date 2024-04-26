from flask import Flask, render_template

user = Flask(__name__)

@user.route('/')
def rend():
    return render_template('userinterface.html')
if __name__ == "__main__":
    
    user.run(debug=True)
