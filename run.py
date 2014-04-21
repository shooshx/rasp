import time
x = 0
while True:
  print x
  if (x % 10) == 0:
    print "HELLO ***********************"
  x = x + 1
  time.sleep(0.2)
