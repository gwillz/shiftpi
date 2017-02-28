from pygpio import Gpio, modes, backends
BACKEND = backends.NativeBackend

try:
    BACKEND = backends.RpiBackend
except (AttributeError, ImportError):
    pass

# pragma pylint: disable=bad-whitespace

class ShiftPi(object):
    """TODO DOCS"""
    
    def __init__(self, num_registers=1, ser_pin=27, sck_pin=22, rck_pin=24):
        self._SER_pin   = ser_pin
        self._RCLK_pin  = rck_pin
        self._SRCLK_pin = sck_pin
        self._REG_num   = num_registers
        
        self._registers = [] #: used to store states of all pins
        
        self._gpio = Gpio(BACKEND)
        self._gpio.setup([self._SER_pin,
                          self._RCLK_pin,
                          self._SRCLK_pin], modes.OUT)
    
    def write(self, pin, mode):
        """TODO DOCS"""
        
        if pin < 0:
            self._all(mode, execute=False)
        else:
            # set all pins low on first write
            if len(self._registers) == 0:
                self._all(False, execute=False)
            self._setPin(pin, mode)
        
        self._execute()
    
    # shorthand for write()
    def up(self, pin):
        """TODO DOCS"""
        self.write(pin, True)
    
    def down(self, pin):
        """TODO DOCS"""
        self.write(pin, False)
    
    # internal methods for stuff
    def _all_pins(self):
        """TODO DOCS"""
        return self._REG_num * 8
    
    def _all(self, mode, execute=True):
        """TODO DOCS"""
        
        for pin in range(0, self._all_pins()):
            self._setPin(pin, mode)
        if execute:
            self._execute()
            
    def _setPin(self, pin, mode):
        """TODO DOCS"""
        
        try:
            self._registers[pin] = mode
        except IndexError:
            self._registers.insert(pin, mode)
            
    def _execute(self):
        """TODO DOCS"""
        
        self._gpio.write(self._RCLK_pin, False)
        
        for pin in range(self._all_pins()-1, -1, -1):
            self._gpio.write(self._SRCLK_pin, False)
            
            pin_mode = self._registers[pin]
            
            self._gpio.write(self._SER_pin, pin_mode)
            self._gpio.write(self._SRCLK_pin, True)
            
        self._gpio.write(self._RCLK_pin, True)
        
