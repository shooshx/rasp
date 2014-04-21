import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)

def sendimg(im):
    addr = 1
    for l in im:
        #print [addr, l ]
        spi.xfer2([addr, l >> 1 | l << 7 ])
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
            time.sleep(0.01)
                
            

def setup():        
    spi.xfer2([0x09, 0])     # no BCD decode
    spi.xfer2([0x0b, 0x07])  # scan-limit = all on
    spi.xfer2([0x0a, 0x0f])  # intensity full
    spi.xfer2([0x0c, 0x01])  # get out of shutdown

def main():
    setup()



if __name__ == "__main__":

    
    main()
