from Adafruit_CharLCD import Adafruit_CharLCD

import termios, sys, os
TERMIOS = termios

def getkey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 10)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return c

lcd = Adafruit_CharLCD()

def terminal():
    lcd.begin(40,2)
    lcd.cursor()
    lcd.testfun()
    col = 0;
    row = 0;
    while True:
        x = getkey()
        c = x[0]
        rest = x[1:]
        n = ord(c)
        print col, row, n, rest, [ord(i) for i in rest]
        if n == 127:
            col = max(col - 1,0)
            lcd.setCursor(col,row)
        elif n == 10:
            col = 0
            row = 1-row
            lcd.setCursor(col,row)
        elif n == 27:
            if len(rest) == 0:
                lcd.clear()
                col = 0
                row = 0
            else:
                if rest == '[D':
                    col = max(col - 1, 0);
                elif rest == '[C':
                    col = col + 1
                elif rest == '[A' or rest == '[B':
                    row = 1 - row
                lcd.setCursor(col,row)
        else:
            lcd.message(x)
            col = col + 1
            if col >= lcd.numcols:
                col = 0;
                row = 1 - row
        

terminal()