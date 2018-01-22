import json
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
import threading
import random
from webapi.models import MP3Playback, AlarmClock

import RPi.GPIO as GPIO # Allows us to call our GPIO pins and names it just GPIO
from webapi.Utils.PlayerManager import PlayerManager


import requests,json


def send_message_fcm():
    # Assemble url
    url = "https://fcm.googleapis.com/fcm/send"
    api_key = "AAAAUX6f4nA:APA91bHmAXALv-Ztr4z2Gx4zbZN_ynCJ3sFGzjmv27CbwOm90ABrDSoDaPely-PDuG-kA9TxjBW15IUPAhAQdHDYLO5D3JoN2XRlvn7LgCVzFts-XnOzJDk9qpe_Wank3JVRmnS9Hpu_"
    user_token = "eSqiSTNLkM8:APA91bG7iYCXHQIztzrQ2ZeugIRz1eCMuanKfbhUWt9avaZRO28nSjSDEG9GlTlE_kmHSjseiTn6hKhp14Xbr91fPm2kc1c-gK6nY6Wnhraf3K_nNCzFMGf-aTMrkr0nyhQET-Chk-hV"
    headers = {'Authorization': 'key=' + api_key}

    data = {"body": "quelqu'un sur le tapis", "title":"tapis"}
    payload = {"notification": data, "to": user_token}

    # headers = {'content-type': 'application/json','Authorization': 'key=AAAAUX6f4nA:APA91bHmAXALv-Ztr4z2Gx4zbZN_ynCJ3sFGzjmv27CbwOm90ABrDSoDaPely-PDuG-kA9TxjBW15IUPAhAQdHDYLO5D3JoN2XRlvn7LgCVzFts-XnOzJDk9qpe_Wank3JVRmnS9Hpu_'}
    # body = {'notification':{'body': 'This message ANIS', 'title':'Hello ANIS2'},'to' : 'eSqiSTNLkM8:APA91bG7iYCXHQIztzrQ2ZeugIRz1eCMuanKfbhUWt9avaZRO28nSjSDEG9GlTlE_kmHSjseiTn6hKhp14Xbr91fPm2kc1c-gK6nY6Wnhraf3K_nNCzFMGf-aTMrkr0nyhQET-Chk-hV'}
    try:
        #Send REST API call
        print("REQUEST: POST {}".format(url))
        request = requests.post(url, headers=headers, json=payload)
        request.raise_for_status()
        print(request.text)
        return json.loads(request.text)
    except ConnectionError as e:
        print("send_message_fcm: Failed {0}".format(e))
        print(json.loads(request.text))
    except requests.exceptions.HTTPError as e:
        print("send_message_fcm: Failed {0}".format(e))
        print(request.text)
    except requests.exceptions.ConnectionError as e:
        print("send_message_fcm: Failed {0}".format(e))



def sendmsg(num):
    Group('stocks').send({'text':num})

t = 0
n = 0

# def inputHigh(channel):
#     print('1');

def periodic():
    global t;
    global n;
#    n = random.randint(100,200);
#    sendmsg(str(n))

    #stop playing if reached
#    if ((PlayerManager.is_started()) and (n > AlarmClock.stop_seconds_hit_rug)): 
#      PlayerManager.stop()

    GPIO.setmode(GPIO.BOARD)  # Set's GPIO pins to BCM GPIO numbering
    # to bu used : Ground 06 / GPIO012 (pin 32)
    INPUT_PIN_1 = 32


    # to be used : Ground 14 / GPIO016 (pin 36)
    INPUT_PIN_2 = 36

    # Sets our input pin, in this example I'm connecting our button to pin 32. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
    GPIO.setup(INPUT_PIN_1, GPIO.IN, pull_up_down = GPIO.PUD_UP)  # Set our input pin to be an input

    GPIO.setup(INPUT_PIN_2, GPIO.IN, pull_up_down = GPIO.PUD_UP)  # Set our input pin to be an input

    # Create a function to run when the input is high

   # GPIO.add_event_detect(INPUT_PIN, GPIO.FALLING, callback=inputLow, bouncetime=200) # Wait for the input to go low, run the function when it does
    STATE_RUG_1 = (GPIO.input(INPUT_PIN_1) == False)
    STATE_RUG_2 = (GPIO.input(INPUT_PIN_1) == False)

    if ((STATE_RUG_1 == False)and(STATE_RUG_1 == False)):
        n = 0
        sendmsg("rien:"+str(n))
    else:
        n = n + 1
        sendmsg("pression detecté:"+str(n))

        qs = AlertRug.objects.only('is_audio_active').get(pk=1).is_audio_active
        print("start_rug_manage:start -->", qs )
        if ((qs==True)and((PlayerManager.is_started()):
            print("jouer son si pas actif !(PlayerManager.is_started()) ")



    # if (GPIO.input(INPUT_PIN_1) == True): # Physically read the pin now
    #     n = 0
    #     sendmsg("rien:"+str(n))
    # else:
    #     n = n + 1
    #     sendmsg("pression detecté:"+str(n))


    #sleep(1);           # Sleep for a full second before restarting our loop

    
    t = threading.Timer(1, periodic)
    t.start()

def ws_message(message):
    global t 
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    print(message.content['text'])
    if ( message.content['text'] == "start"):
        periodic()
    else:
        t.cancel()
   # message.reply_channel.send({'text':'200'})

def ws_connect(message):
    print("ws_connect:Someone connected.")
    Group('stocks').add(message.reply_channel)
    Group('stocks').send({'text':'connected'})



def ws_disconnect(message):
    Group('stocks').send({'text':'disconnected'})
    Group('stocks').discard(message.reply_channel)
