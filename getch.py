## from http://code.activestate.com/recipes/134892/

class _Getch:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()


if __name__ == "__main__":
    
    while True:
        c = getch()
        print ord(c)
        if c == 'q':
            print c
            break
        elif ord(c) == 65:
            print 'up'
        elif ord(c) == 68:
            print 'left'
        elif ord(c) == 66:
            print 'down'
        elif ord(c) == 67:
            print 'right'
            
        elif ord(c) == 3:
            print "break"
            break
        elif ord(c) == 27:
            print "ESC"
            break
        else:
            print ord(c), c.replace("\n", "").replace("\r", "")
    
    print 'exit'
    
