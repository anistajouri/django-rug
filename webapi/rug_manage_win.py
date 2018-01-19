import json
import threading
import random
from time import strftime
from webapi.models import *
from webapi.views.ListClickRugView import ClickRugList

#import RPi.GPIO as GPIO # Allows us to call our GPIO pins and names it just GPIO
#from webapi.Utils.PlayerManager import PlayerManager
 

t = 0
n = 0

# def inputHigh(channel):
#     print('1');
state = "not_started"

def periodic():
    global t;
    global n;
    #n = random.randint(100,200);
    n = n + 0.5


#    if ((PlayerManager.is_started()) and (n > AlarmClock.stop_seconds_hit_rug)): 
#      PlayerManager.stop()




    print("periodic: n=", n)
    

#    AlarmClock.objects.get(id=id_mp3_playback_to_play)
#    print("periodic: End counting for stop rug:", AlarmClock.stop_seconds_hit_rug )



    #stop playing if stop_seconds_hit_rug is reached

    # if (n > int(AlarmClock.stop_seconds_hit_rug)): 
    #   print("periodic: End counting for stop rug:", AlarmClock.stop_seconds_hit_rug )
    #MP3Playback.objects.get(id=id_mp3_playback_to_play)

    # if (n>200):
    #   n = 0	
    #   return
    #sendmsg(str(n))


   #  GPIO.setmode(GPIO.BOARD)  # Set's GPIO pins to BCM GPIO numbering
   #  # to bu used : Ground 06 / GPIO012
   #  INPUT_PIN = 12           
   #  # Sets our input pin, in this example I'm connecting our button to pin 12. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
   #  GPIO.setup(INPUT_PIN, GPIO.IN)  # Set our input pin to be an input

   #  # Create a function to run when the input is high

   # # GPIO.add_event_detect(INPUT_PIN, GPIO.FALLING, callback=inputLow, bouncetime=200) # Wait for the input to go low, run the function when it does

   #  if (GPIO.input(INPUT_PIN) == True): # Physically read the pin now
   #      sendmsg(str(n))
   #      n = n + 1
   #  else:
   #      n = 0
   #      sendmsg(str(n))

    #sleep(1);           # Sleep for a full second before restarting our loop

    
    t = threading.Timer(0.5, periodic)
    t.start()

def start_rug_manage(message):
    global t 
    global state
    global n
    #print(message,"/", state)
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    if (( message == "start")and(state != "started")):
        periodic()
        state = "started"

        qs = AlertRug.objects.only('is_active_first_pass').get(pk=1).is_active_first_pass
        print("start_rug_manage:start -->", qs )
        if (qs==True):
            print("jouer son si pas actif !(PlayerManager.is_started()) ")
    else:
        state = "not_started"
        if (n > 0):
           clock = strftime("%Y-%m-%dT%H:%M:%S")
           ClickRugList.update_statistics(str(clock), n )           
           n = 0
           #
        t.cancel()
        print("start_rug_manage:stop")

   # message.reply_channel.send({'text':'200'})

