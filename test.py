# example uses/tests
from __future__ import print_function
import sys, time, random
from gslib import getch
from shiftpi import ShiftPi

if __name__ == "__main__":
    s = ShiftPi()
    speed = 0.1
    
    if len(sys.argv) == 1:
        print("loop, pong, rand, police, strobe, keys")
        exit(0)
    
    if len(sys.argv) > 2:
       speed = float(sys.argv[2])
    
    if sys.argv[1] == "loop":
        while True:
            for i in range(0,8):
                s.write(7 if i==0 else i-1, False)
                s.write(i, True)
                time.sleep(speed)
    
    elif sys.argv[1] == "pong":
        while True:
            for i in range(0,8):
                s.write(7 if i==0 else i-1, False)
                s.write(i, True)
                time.sleep(speed)
            
            for i in reversed(range(1,7)):
                s.write(i+1, False)
                s.write(i, True)
                time.sleep(speed)
    
    elif sys.argv[1] == "rand":
        
        while True:
            s.write(-1, False)
            s.write(random.randint(0,7), True)
            time.sleep(speed)
    
    elif sys.argv[1] == "police":
       left, right = True, False
       
       while True:
           for i in range(0,8):
               if i < 4:
                   s.write(i, left)
               else:
                   s.write(i, right)
           
           time.sleep(speed)
           _right = right
           left, right = _right, left
    
    elif sys.argv[1] == "strobe":
        
        while True:
           s.write(-1, True)
           time.sleep(speed)
           s.write(-1, False)
           time.sleep(speed)
    
    elif sys.argv[1] == "keys":
        print("press ESC to quit")
        
        up = [False, False, False, False, False, False, False, False]
        s.write(-1, False)
        
        while True:
            c = getch()
            if ord(c) == 27: break
            
            try:
                i = int(c)-1
                if i in range(0,8):
                    if up[i]: s.write(i, False)
                    else: s.write(i, True)
                    
                    up[i] = not up[i]
                
            except ValueError:
                print("(1-8):", c)
