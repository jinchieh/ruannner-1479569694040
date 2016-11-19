# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, jsonify
#import Twilio libraries
from flask import request
from twilio import twiml

#set twilio params
app = Flask(__name__)

# Update with your own phone number in E.164 format
MODERATOR = '+18609692438'
#End Twilio params

app = Flask(__name__)

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/startcall')
def StartCall():
    return 'About to call Twilio!'

#Begin Twilio
@app.route("/voice", methods=['GET', 'POST'])
def call():
    """Returns TwiML for a moderated conference call"""
    # Start our TwiML response
    response = twiml.Response()

    # Start with a <Dial> verb
    with response.dial() as dial:
        # If the caller is our MODERATOR, then start the conference when they
        # join and end the conference when they leave
        if request.values.get('From') == MODERATOR:
            dial.conference(
                'My conference',
                startConferenceOnEnter=True,
                endConferenceOnExit=True)
        else:
            # Otherwise have the caller join as a regular participant
            dial.conference('My conference', startConferenceOnEnter=False)

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)    
#End Twilio

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'
    
@app.route('/api/people')
def GetPeople():
    list = [
        {'name': 'John', 'age': 28},
        {'name': 'Bill', 'val': 26}
    ]
    return jsonify(results=list)

@app.route('/api/people/<name>')
def SayHello(name):
    message = {
        'message': 'Hello ' + name
    }
    return jsonify(results=message)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
