# !/usr/bin/env python3

import RPi.GPIO as GPIO
from http.server import BaseHTTPRequestHandler, HTTPServer
from onOffFunctions import setupGPIO , switch1, switch2, getTemperature, detectButtonPress

host_name = '0.0.0.0'  # IP Address of Raspberry Pi
host_port = 8000
led1_on = True
led2_on = True

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
        global led1_on, led2_on
        temp = "getTemperature()"
        if led1_on == True:
            led1 = "On"
        else:
            led1 = "Off"
        if led2_on == True:
            led2 = "On"
        else:
            led2 = "Off"
        self.do_HEAD()
        self.wfile.write(html.format(temp[5:], led1, led2).encode("utf-8"))

    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        [led, post_data] = post_data.split("=")
        global led1_on, led2_on

        if led == "led1":
            if post_data == 'On':
                led1_on = True
                GPIO.output(27, GPIO.HIGH)
            else:
                led1_on = False
                GPIO.output(27, GPIO.LOW)
        else:
            if post_data == 'On':
                led2_on = True
                GPIO.output(22, GPIO.HIGH)
            else:
                led2_on = False
                GPIO.output(22, GPIO.LOW)
        

        print("LED is {}".format(post_data))
        self._redirect('/')  # Redirect back to the root url


# # # # # Main # # # # #

if __name__ == '__main__':
    setupGPIO()
    detectButtonPress(led1_on, led2_on)
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
