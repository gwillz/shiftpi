#!/usr/bin/env python2
import RPi.GPIO as GPIO

# pragma pylint: disable=bad-whitespace

class ShiftPi(object):
    # define modes
    ALL  = -1
    HIGH = GPIO.HIGH
    LOW  = GPIO.LOW
    
    # is used to store states of all pins
    _registers = []
    
    def __init__(self, num_registers=1, ser_pin=27, sck_pin=22, rck_pin=24):
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
        
