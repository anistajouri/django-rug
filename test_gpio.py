import RPi.GPIO as GPIO # Allows us to call our GPIO pins and names it just GPIO

GPIO.setmode(GPIO.BOARD)  # Set's GPIO pins to BCM GPIO numbering
# to bu used : Ground 06 / GPIO012
INPUT_PIN = 12           
# Sets our input pin, in this example I'm connecting our button to pin 12. Pin 0 is the SDA pin so I avoid using it for sensors/buttons
GPIO.setup(INPUT_PIN, GPIO.IN)  # Set our input pin to be an input

# Create a function to run when the input is high

# GPIO.add_event_detect(INPUT_PIN, GPIO.FALLING, callback=inputLow, bouncetime=200) # Wait for the input to go low, run the function when it does
n=0
while (1):
    if (GPIO.input(INPUT_PIN) == True): # Physically read the pin now
        n = n + 1
    else:
        n = 0
    print(n)

