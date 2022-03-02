# !/usr/bin/env python3

import RPi.GPIO as GPIO
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '0.0.0.0'  # IP Address of Raspberry Pi
host_port = 8000
led1_on = False
led2_on = False

def setupGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def switch1(ev=None):
    global led1_on
    led1_on = not led1_on

    if led1_on == True:
        GPIO.output(18, GPIO.HIGH)
    else:
        GPIO.output(18, GPIO.LOW)

def switch2(ev=None):
    global led2_on
    led2_on = not led2_on

    if led1_on == True:
        GPIO.output(20, GPIO.HIGH)
    else:
        GPIO.output(20, GPIO.LOW)

def detectButtonPress():
    GPIO.add_event_detect(23, GPIO.FALLING, callback=switch1, bouncetime=300)
    GPIO.add_event_detect(25, GPIO.FALLING, callback=switch2, bouncetime=300)


def getTemperature():
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    return temp

def getLED1():
    if GPIO.output(18) == LOW:
        return "OFF"
    else: 
        return "ON"

def getLED2():
    if GPIO.output(18) == LOW:
        return "OFF"
    else: 
        return "ON"



class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        html = '''
           <html>
           <body 
            style="width:960px; margin: 20px auto;">
           <h1>Welcome to my Raspberry Pi</h1>
           <p>Current GPU temperature is {}</p>
           <form action="/" method="POST">
               Turn LED :
               <input type="submit" name="led1" value="On">
               <input type="submit" name="led1" value="Off">
               <br>
               <br>
               LED Status: {}
           </form>
           <hr/>
           <form action="/" method="POST">
               Turn LED :
               <input type="submit" name="led2" value="On">
               <input type="submit" name="led2" value="Off">
               <br>
               <br>
               LED Status: {}
           </form>
           </body>
           </html>
        '''
        temp = "getTemperature()"
        led1 = getLED1()
        led2 = getLED2()
        self.do_HEAD()
        self.wfile.write(html.format(temp[5:], led1, led2).encode("utf-8"))

    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        [led, post_data] = post_data.split("=")

        if led == "led1":
            if post_data == 'On':
                GPIO.output(18, GPIO.HIGH)
            else:
                GPIO.output(18, GPIO.LOW)
        else:
            if post_data == 'On':
                GPIO.output(20, GPIO.HIGH)
            else:
                GPIO.output(20, GPIO.LOW)

        print("LED is {}".format(post_data))
        self._redirect('/')  # Redirect back to the root url


# # # # # Main # # # # #

if __name__ == '__main__':
    setupGPIO()
    detectButtonPress()
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
