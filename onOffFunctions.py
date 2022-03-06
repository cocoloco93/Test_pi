from calendar import leapdays
from operator import countOf
import RPi.GPIO as GPIO
import os
count = 0

def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(27, GPIO.OUT,initial = GPIO.LOW) #led1 pin set as output
    GPIO.setup(22, GPIO.OUT,initial = GPIO.LOW))                    #led2 pin set as output
#   GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#  GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def switch1(ev=None, led2_on=False):
    led1_on = not led1_on

    if led1_on == True:
        GPIO.output(18, GPIO.HIGH)
    else:
        GPIO.output(18, GPIO.LOW)

def switch2(ev=None, led2_on=False):
    global count
    count =+ count
    led2_on = not led2_on

    if led2_on == True:
        GPIO.output(20, GPIO.HIGH)
    else:
        GPIO.output(20, GPIO.LOW)
    if(cout/2):
        led2_on = True
        GPIO.output(20, GPIO.HIGH)


def detectButtonPress(led1_on, led2_on):
    GPIO.add_event_detect(23, GPIO.FALLING, callback=switch1(led1_on), bouncetime=300)
    GPIO.add_event_detect(25, GPIO.FALLING, callback=switch2(led2_on), bouncetime=300)


def getTemperature():
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    return temp