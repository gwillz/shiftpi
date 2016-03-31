#!/usr/bin/env python2

import RPi.GPIO as GPIO, time

class ShiftPi(object):
    
    # Define MODES
    ALL  = -1
    HIGH = 1
    LOW  = 0
    
    # is used to store states of all pins
    _registers = []

    def __init__(self, ser_pin=27, sck_pin=22, rck_pin=23, num_registers=1):
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
        if pin == self.ALL:
            self._all(mode)
        else:
            if len(self._registers) == 0:
                self._all(self.LOW)

            self._setPin(pin, mode)
        self._execute()

    def _all_pins(self):
        return self._REG_num * 8

    def _all(self, mode, execute=True):
        all_shr = self._all_pins()

        for pin in range(0, all_shr):
            self._setPin(pin, mode)
        if execute:
            self._execute()

        return self._registers

    def _setPin(self, pin, mode):
        try:
            self._registers[pin] = mode
        except IndexError:
            self._registers.insert(pin, mode)

    def _execute(self):
        all_pins = self._all_pins()
        GPIO.output(self._RCLK_pin, GPIO.LOW)

        for pin in range(all_pins -1, -1, -1):
            GPIO.output(self._SRCLK_pin, GPIO.LOW)

            pin_mode = self._registers[pin]

            GPIO.output(self._SER_pin, pin_mode)
            GPIO.output(self._SRCLK_pin, GPIO.HIGH)

        GPIO.output(self._RCLK_pin, GPIO.HIGH)

