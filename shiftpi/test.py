#!/usr/bin/env python2
# example uses/tests
import sys, time, random
from gslib import getch
from __init__ import ShiftPi

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
                s.write(7 if i==0 else i-1, s.LOW)
                s.write(i, s.HIGH)
                time.sleep(speed)
    
    elif sys.argv[1] == "pong":
        while True:
            for i in range(0,8):
                s.write(7 if i==0 else i-1, s.LOW)
                s.write(i, s.HIGH)
                time.sleep(speed)
            
            for i in reversed(range(1,7)):
                s.write(i+1, s.LOW)
                s.write(i, s.HIGH)
                time.sleep(speed)
    
    elif sys.argv[1] == "rand":
        
        while True:
            s.write(s.ALL, s.LOW)
            s.write(random.randint(0,7), s.HIGH)
            time.sleep(speed)
    
    elif sys.argv[1] == "police":
       left, right = s.HIGH, s.LOW
       
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
           s.write(s.ALL, s.HIGH)
           time.sleep(speed)
           s.write(s.ALL, s.LOW)
           time.sleep(speed)
    
    elif sys.argv[1] == "keys":
        print("press ESC to quit")
        
        up = [False, False, False, False, False, False, False, False]
        s.write(s.ALL, s.LOW)
        
        while True:
            c = getch()
            if ord(c) == 27: break
            
            try:
                i = int(c)-1
                if i in range(0,8):
                    if up[i]: s.write(i, s.LOW)
                    else: s.write(i, s.HIGH)
                    
                    up[i] = not up[i]
                
            except ValueError:
                print("(1-8):", c)
