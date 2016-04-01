#!/usr/bin/env python2
import RPi.GPIO as GPIO, time

class ShiftPi(object):
    # define modes
    ALL  = -1
    HIGH = 1
    LOW  = 0
    
    # is used to store states of all pins
    _registers = []

    def __init__(self, num_registers=1, ser_pin=27, sck_pin=22, rck_pin=23):
        self._SER_pin   = ser_pin
        self._RCLK_pin  = rck_pin
        self._SRCLK_pin = sck_pin
        self._REG_num   = num_registers
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._SER_pin,   GPIO.OUT)
        GPIO.setup(self._RCLK_pin,  GPIO.OUT)
        GPIO.setup(self._SRCLK_pin, GPIO.OUT)
    
    def write(self, pin, mode):
        # accept bool types
        if isinstance(mode, bool):
            mode = self.HIGH if mode else self.LOW
        
        if pin == self.ALL:
            self._all(mode, execute=False)
        else:
            # set all pins low on first write
            if len(self._registers) == 0:
                self._all(self.LOW, execute=False)
            self._setPin(pin, mode)
        
        self._execute()
    
    # shorthand for write()
    def up(self, pin):
        self.write(pin, self.HIGH)
    
    def down(self, pin):
        self.write(pin, self.LOW)
    
    # internal methods for stuff
    def _all_pins(self):
        return self._REG_num * 8
    
    def _all(self, mode, execute=True):
        for pin in range(0, self._all_pins()):
            self._setPin(pin, mode)
        if execute:
            self._execute()

    def _setPin(self, pin, mode):
        try:
            self._registers[pin] = mode
        except IndexError:
            self._registers.insert(pin, mode)

    def _execute(self):
        GPIO.output(self._RCLK_pin, GPIO.LOW)
        
        for pin in range(self._all_pins()-1, -1, -1):
            GPIO.output(self._SRCLK_pin, GPIO.LOW)
            
            pin_mode = self._registers[pin]
            
            GPIO.output(self._SER_pin, pin_mode)
            GPIO.output(self._SRCLK_pin, GPIO.HIGH)

        GPIO.output(self._RCLK_pin, GPIO.HIGH)

# example uses/tests
if __name__ == "__main__":
    import sys
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
        import random
        
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
        from getch import getch
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
