import sys
import time
import pigpio
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import os
import thread

# needs sudo ~/PIGPIO/pigpiod

pi = pigpio.pi() # connect to local Pi


#step_out1=4
#step_out2=18

#-dir_out = 11
#dir_out1 = 17
#dir_out2 = 27


#pi.set_mode(step_out1, pigpio.OUTPUT)
#pi.set_mode(step_out2, pigpio.OUTPUT)
#pi.set_mode(dir_out1, pigpio.OUTPUT)
#pi.set_mode(dir_out2, pigpio.OUTPUT)



def do_wave():
    square = []

    #                          ON           OFF    MICROS\
    to_on = 1 << step_out1 | 1 << step_out2
    square.append(pigpio.pulse(to_on, 0,       10000))
    square.append(pigpio.pulse(0, to_on , 10000))

    pi.wave_add_generic(square)

    wid = pi.wave_create()

    try:
        if wid >= 0:
           pi.wave_send_repeat(wid)
           time.sleep(4)
           GPIO.output(dir_out, 1)
           time.sleep(60)
           pi.wave_tx_stop()
           pi.wave_delete(wid)
    except:
        pass

    pi.wave_tx_stop()
    pi.stop()


# tension


class Motor:
    def __init__(self, step_out, dir_out):
        self.step_out = step_out
        self.dir_out = dir_out
        self.cur_ten = 0
        
        pi.set_mode(step_out, pigpio.OUTPUT)
        pi.set_mode(dir_out, pigpio.OUTPUT)


    def p(self, c):  
                  
        if c > 0:
            if self.cur_ten <= 0:
                pi.write(self.dir_out, 1)
                c += 16+8+4  # redraw tension in this new direction
        else: 
            if self.cur_ten >= 0:
                pi.write(self.dir_out, 0)
                c -= 16+8+4
        self.cur_ten = c
            
        time.sleep(0.001)
        for i in xrange(0, abs(c)):
            pi.write(self.step_out, 1)
            time.sleep(0.001)
            pi.write(self.step_out, 0)
            time.sleep(0.001)

        
m1 = Motor(4, 17)   # positibe=right 
m2 = Motor(18, 27)  # positive=down
        
        

def sq(c):
    m1.p(c)
    m2.p(c)
    m1.p(-c)
    m2.p(-c)
    
def sq2(c):
    m1.p(c)
    m2.p(-c)
    m1.p(-c)
    m2.p(c)    
    
def squares():
    #m1.p(200)
    sq(-100)
    #sq(-100)
    sq(100)
    #sq(100)
    sq2(100)
    #sq2(100)
    sq2(-100)
    #sq2(-100)
    
    sq(-200)
    sq(200)
    sq2(200)
    sq2(-200)    
    
     
    
def mv(dx, dy):
    print "MV", dx, dy   
    m1.p(dx)
    m2.p(dy) 

def rel_line_to(dx, dy):
    if dx == 0:
        mv(0, dy)
        return
    if dy == 0:
        mv(dx, 0)
        return
    
    fdx = float(dx)
    fdy = float(dy)

    ly = 0
    lmx = 0
    
    movedX = 0
    movedY = 0
    sign = 1 if dx > 0 else -1
    # TBD - divide to x and y
    for x in xrange(0, dx + sign, sign):
        y = int(fdy * float(x) / fdx)
        print x, y
        if y != ly: # or x == dx:
            sx = x - lmx
            sy = y - ly
            mv(sx, sy)
            movedX += sx
            movedY += sy
        
            ly = y
            lmx = x
            
    assert movedX == dx, "Bug in movedX %d != %d" % (movedX, dx)
    assert movedY == dy, "Bug in movedY %d != %d" % (movedY, dy)
    
                

def diamond():
    rel_line_to(-100, 200)
    rel_line_to(-100, -200)
    rel_line_to(100, -200)
    rel_line_to(100, 200)
    
    
def run_gcode(text):
    posx = None
    posy = None
    for line in text.splitlines():
        spl = line.split()
        if len(spl) == 0:
            continue
        if spl[0] == "G01":
            x = int(spl[1][1:])
            y = int(spl[2][1:])
            if posx is None:
                posx = x
                posy = y
            else:
                dx = x - posx
                dy = y - posy
                posx = x
                posy = y
                print dx, dy
                rel_line_to(dx, dy)
        else:
            raise Exception("Unknown command " + repr(spl))

    
class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print "got GET", self.path
            
        filename = self.path[1:]
        if filename == "/":
            filename == "index.html"
        if os.path.exists(filename):
            print "getting file", filename
            with open(filename, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            
    def do_POST(self):
        print "got POST", self.path
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        print "DATA=" + post_body
        
        self.send_response(200)
        thread.start_new_thread(run_gcode, (post_body,))
            
            
PORT_NUMBER = 80

def gcodeserver(argv):
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER

    server.serve_forever()

    #rel_line_to(int(argv[1]), int(argv[2]))
    

def main(argv):
    gcodeserver(argv)
    #rel_line_to(1, 70)


    
main(sys.argv)    

