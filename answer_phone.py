from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Record, Gather

app = Flask(__name__)

recording=''

#**********************************************************************************
#function and route for initial IVR menu
@app.route("/answer", methods=['GET', 'POST'])
def answer_call():
    #begin twilio response
    resp = VoiceResponse()

    # Read out the base IVR menu option
    resp.say("Welcome to Dr. Brewer's test message line!", voice='alice')
    resp.say("Press 1 to record a message for later use!", voice='alice')

    #grab the next digit entered
    resp.gather(numDigits=1, action='/start-recording')

    return str(resp)

#*******************************************************************************
#function and route for recording the message
@app.route("/start-recording", methods=['GET','POST'])
def start_recording():
    resp = VoiceResponse()
    #check to see if the caller actually pressed 1, and start the recording if so
    if ('Digits' in request.values) and (request.values['Digits']=='1'):
        resp.say("Please record your message after the tone, and press star to finish", voice='alice')
        resp.record(max_length="30", finishOnKey='*', action='/retrieve-recording')

    return str(resp)
#*******************************************************************************
#function and route for retrieving the recorded message
@app.route("/retrieve-recording", methods=['GET','POST'])
def retrieve_recording():
    resp=VoiceResponse()
    global recording
    recording=request.form.get('RecordingUrl')
    print(recording)

    resp.say("If you would like to hear the message you just recorded, please press 2 now. Otherwise, you may hang up to end the call.", voice='alice')
    resp.gather(numDigits=1,action='/play-recording')

    return str(resp)
#************************************************************************************
#function and route for playing the recorded message, should the user want to
@app.route("/play-recording", methods=['GET','POST'])
def play_recording():
    resp=VoiceResponse()
    print(recording)
    if ('Digits' in request.values) and (request.values['Digits']=='2'):
        #print("recording="+recording)
        resp.play(recording,loop=1)
    return str(resp)
#***********************************************************************

if __name__ == "__main__":
    app.run(debug=True)
