import spidev
import time
import RPi.GPIO as GPIO

spi = spidev.SpiDev()
spi.open(0,0)

def sendimg(im):
    addr = 1
    for l in im:
        #print [addr, l ]
        spi.xfer2([addr, l ])
        addr += 1
        if addr == 9:
            break
        
        
        
def allnum():
    s = range(1,256)
    for i in xrange(0, 255-7):
        sendimg(s[i:])
        
def sinimg():
    s=[1,2,4,8,16,32,64,128,128,128, 64,32,16,8,4,2,1,1]*2
    while True:
        for i in xrange(0, 18):
            sendimg(s[i:])    
            time.sleep(0.02)
            
def geteye():
    return GPIO.input(22)                

BLANK=[[0]*8]
OWALL = [[129,0xff,129,129,129,129,129,0xff]]
IWALL = [[0xff]*8]

data = IWALL + OWALL*5 + IWALL + BLANK * 1000;              
            
def runWorker():
    lastEye = 0
    while True:
        for d in data:
            #out(d)
            eye = geteye()
            if eye:
                break
            sendimg(d)


def setup():        
    spi.xfer2([0x09, 0])     # no BCD decode
    spi.xfer2([0x0b, 0x01])  # scan-limit = all on 7
    spi.xfer2([0x0a, 0x0f])  # intensity full
    spi.xfer2([0x0c, 0x01])  # get out of shutdown

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(22, GPIO.IN)



def main():
    setup()
    runWorker()



if __name__ == "__main__":

    
    main()
