# This server script is based on <https://gist.github.com/nitaku/10d0662536f37a087e1b>
#!/usr/bin/python3
from urllib.parse import parse_qsl
import http.server
import socketserver
import json
import cgi


# start server
def run(PORT=8081):
    socketserver.TCPServer.allow_reuse_address = True  # Allows for smooth restart
    handler_object = MyHttpRequestHandler # Create an object of the above class
    my_server = socketserver.TCPServer(("", PORT), handler_object)
    
    print('Listening on Port : ' + str(PORT))
    while 1:
        my_server.handle_request()     # Theory: this line does the magic              ;)


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self, type):
        self.send_response(200)
        self.send_header('Content-type', type)
        self.end_headers()
        
        
    def do_HEAD(self):
        #self._set_headers('application/json')
        return
        
    def do_GET(self):
        if self.path[0:5] == '/_do?':        # JSON Response ---------------------------
            self._set_headers('application/json')
            self.data = _do(self.path[5:])
            self.wfile.write(json.dumps(self.data).encode('utf-8'))
            return
        elif self.path[0:8] == '/_fetch?':        # JSON Response ---------------------------
            self._set_headers('application/json')
            self.data = _fetch(self.path[8:])
            self.wfile.write(json.dumps(self.data).encode('utf-8'))
            return
        elif self.path[0:2] == '/_':          # Protect _* files
            self.send_response(400)
            self.end_headers()
            return
        else:                   # Standard HTML Response ---------------------------
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
    # POST echoes the message adding a JSON field
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
            
        # read the message and convert it into a python dictionary
        length = int(self.headers.getheader('content-length'))
        message = json.loads(self.rfile.read(length))
        
        # add a property to the object, just to mess with data
        message['received'] = 'ok'
        
        # send the message back
        self._set_headers('application/json')
        self.wfile.write(json.dumps(message))


import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
ADC.setup()
                                      # ------------- PIN I/O handling
class myScope:
    def __init__(self, pin , io):
        self.data = {}
        self.setType(pin, io)
    def setType(self, pin, io):
        self.data['state'] = 0
        self.data['value'] = 0.0
        self.data['logging'] = 0
        self.data['pin'] = pin
        self.data['type'] = io
        if io == 'o':
            GPIO.setup(pin, GPIO.OUT)
            self.pushState()
        if io == 'i':
            GPIO.setup(pin, GPIO.IN)
            self.getState()
        #if io == 'ai':
        #
    def pushState(self):
        if self.data['type'] != 'o':
            return
        else:
            GPIO.output(self.data['pin'], self.data['state'])
    def setState(self, value):
        self.data['state'] = value
        self.pushState()
    def getState(self):
        if self.data['type'] == 'ai':
            self.data['state'] = '0.5'
            self.data['value'] = '{:.3f}'.format(ADC.read(self.data['pin']))
            #print(self.data['pin'] + ' :  ' + str(ADC.read(self.data['pin'])))
        else:
            self.data['state'] = GPIO.input(self.data['pin'])
    #def setLogging(self, state):
        #
    def getData(self):
        return self.data
    def toggleState(self):
        self.data['state'] = 1 - self.data['state']
        self.pushState()
    

def _do(argString):
        data = dict(parse_qsl(argString))
        data['result'] = 'ok'
        try:
            cmd = data['cmd']
            if cmd == 'toggleState':
                #id = int(data['id'])
                #myPins[id].toggleState()
                GPIO.output(data['pin'], 1 - GPIO.input(data['pin']))
            elif cmd == 'setState':
                GPIO.output(data['pin'], 0 + int(data['state']))
            elif cmd == 'setLogging':
                myPins[id].setLogging(bool(data['state']))
            else:
                data['result'] = 'invalid command: ' + cmd
        except:
            data['result'] = 'server failure'
            
        return data
    
def _fetch(argString):
        data = dict(parse_qsl(argString))
        data['result'] = 'ok'
        cmd = data['cmd']
        if cmd == 'allPins':
            data['data'] = {}
            i = 0
            for w in myPins:
                w.getState()
                data['data'][i] = {}
                data['data'][i] = w.getData()
                i = i + 1
            data['data']['count'] = i
        
        return data
    

# ----- live code ----------------    

myPins =   [
            myScope("USR0",'o'),
            myScope("USR1",'o'),
            myScope("USR2",'o'),
            myScope("USR3",'o'),
            myScope("P8_8",'o'),
            myScope("P8_10",'o'),
            myScope("P8_11",'o'),
            myScope("P8_12",'o'),
            myScope("P8_13",'o'),
            myScope("P9_14",'o'),
            myScope("P8_15",'o'),
            myScope("P8_16",'o'),
            myScope("P8_17",'o'),
            myScope("P8_18",'o'),
            myScope("P9_41",'i'),
            myScope("P9_42",'i'),
            myScope("P9_39",'ai'),
            myScope("P9_40",'ai'),
            ]


if __name__ == "__main__":
    print('starting server...')
    from sys import argv
    
    if len(argv) == 2:
        run(PORT=int(argv[1]))
    else:
        run()