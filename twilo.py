from flask import Flask, render_template, request
from twilio.rest import Client

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
    auth_token = 'YOUR_TWILIO_AUTH_TOKEN'

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body='Your Mobile has been hacked!',
        from_='+16467621360',
        to='+918438434868'
    )

    print(message.sid)  

    return 'Message sent successfully'

if __name__ == '__main__':
    app.run(debug=True)
