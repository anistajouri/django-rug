import json
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
import threading
import random
from webapi.models import MP3Playback, AlarmClock

import RPi.GPIO as GPIO # Allows us to call our GPIO pins and names it just GPIO
from webapi.Utils.PlayerManager import PlayerManager


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
    # to bu used : Ground 06 / GPIO012
    INPUT_PIN = 32
    # Sets our input pin, in this example I'm connecting our button to pin 12. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
    GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)  # Set our input pin to be an input

    # Create a function to run when the input is high

   # GPIO.add_event_detect(INPUT_PIN, GPIO.FALLING, callback=inputLow, bouncetime=200) # Wait for the input to go low, run the function when it does

    if (GPIO.input(INPUT_PIN) == True): # Physically read the pin now
        n = 0
        sendmsg("rien:"+str(n))
    else:
        n = n + 1
        sendmsg("pression detecté:"+str(n))

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
