from SimpleHTTPServer import *
import BaseHTTPServer;
import thread
import time
import gc
import sys

import RPi.GPIO as GPIO


prefix = "/change_bits?"
data = [0]

class BitsHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        global data
        if self.path.startswith(prefix):
            sdata = self.path[len(prefix):]
            print "GOT DATA"
            self.wfile.write("BITS")
            data = [int(i) for i in sdata.split(',')]
        else:
            SimpleHTTPRequestHandler.do_GET(self)

def runServer(HandlerClass = BitsHandler, ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)


def runWorker_sleep():
    while True:
        print data
        time.sleep(1)
        



pinsOrder = [15, 21, 3, 18, 7, 13, 23, 24, 5, 8, 16, 10, 19, 22, 12, 11]    

def config():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    for p in pinsOrder:
        GPIO.setup(p, GPIO.OUT)
    GPIO.setup(26, GPIO.IN)
  

def out(n):
    c = n
    for p in pinsOrder:
        b = c & 1
        GPIO.output(p, b)
        c >>= 1
    
def geteye():
    return GPIO.input(26)    

def runWorker():
    config()
    turnCount = 0;
    lastClk = time.clock()
    lastEye = 0
    while True:
        for d in data:
            out(d)
            eye = geteye()
            if eye:
                out(0)
                #turnCount += 1
                #if (turnCount % 50) == 0:
                #    clk = time.clock()
                #    print turnCount, clk - lastClk
                #    lastClk = clk 
                break
            out(d)


def rotMeasure():
    config()
    turnCount = 0;
    lastClk = time.clock()
    lastEye = 0
    while True:
        eye = geteye()
        if eye == 1 and lastEye == 0:
            turnCount += 1
            if (turnCount % 10) == 0:
                clk = time.time()
                print turnCount, clk - lastClk
                lastClk = clk 
        lastEye = eye
    
            
def main(argv):
    gc.set_debug(gc.DEBUG_STATS)
    if len(argv) > 1:
        if argv[1] == "rot":
            rotMeasure()
            return
            
    thread.start_new_thread(runServer, ())
    runWorker()

         
#sudo nice --20  python ./server.py        

if __name__ == '__main__':
    main(sys.argv)    
    
    
    
    
    
    

