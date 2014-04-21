import RPi.GPIO as GPIO
import time


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

def main():
    config()
    while True:
        for i in xrange(1, 2**16):
            out(i)
            if geteye():
                out(0)
                break
    
    




if __name__ == "__main__":
    main()
