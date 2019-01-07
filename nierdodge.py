#pip install keyboard
import keyboard, time
from contextlib import suppress

KEY_DELAY = 0.05

K_SHIFT = 'shift'
K_W = 'w'
K_A = 'a'
K_S = 's'
K_D = 'd'

class GuardedKey(object):
    def __init__(self, key):
        self.key = key
        self.was_hw_pressed = False
        self.was_hw_released = False

    def __enter__(self):
        keyboard.on_press_key(self.key, self.on_hw_press)
        keyboard.on_release_key(self.key, self.on_hw_release)
        return self

    def press(self, *args, **kwargs):
        if self.was_hw_pressed or self.was_hw_released:
            raise ValueError
        keyboard.press(self.key, *args, **kwargs)

    def release(self, *args, **kwargs):
        if self.was_hw_released or self.was_hw_pressed:
            raise ValueError
        keyboard.release(self.key, *args, **kwargs)

    def is_pressed(self, *args, **kwargs):
        return keyboard.is_pressed(self.key, *args, **kwargs)

    def on_hw_press(self, *args, **kwargs):
        self.was_hw_pressed = True

    def on_hw_release(self, *args, **kwargs):
        self.was_hw_released = True

    def __exit__(self, exception_type, exception_value, traceback):
#        keyboard.unhook(self.on_hw_press)
#        keyboard.unhook(self.on_hw_release)
        del self

def in_shift(*args, **kwargs):
    if keyboard.is_pressed(K_A):
        do_dodge(K_A)
    elif keyboard.is_pressed(K_D):   
        do_dodge(K_D)
    elif keyboard.is_pressed(K_S):    
        do_dodge(K_S)
    elif keyboard.is_pressed(K_W):
        do_dodge(K_W)

def do_dodge(key):
#    print("dodge", key)
    with suppress(ValueError):
        with GuardedKey(key) as gkey:
            time.sleep(KEY_DELAY)
            gkey.release()
            time.sleep(KEY_DELAY)
            gkey.press()
            time.sleep(KEY_DELAY)
            gkey.release()
            time.sleep(KEY_DELAY)
            gkey.press()
            while gkey.is_pressed() and keyboard.is_pressed(K_SHIFT):
                time.sleep(0.001)
        #    print("end", key)


def start():
    while True:
        if keyboard.is_pressed(K_SHIFT):
            in_shift()
        time.sleep(0.001)

if __name__ == "__main__":
    print("Nier SHIFT Dodge Started [CTRL+C to quit]")
    try:
        start()
    except KeyboardInterrupt:
        print("Nier SHIFT Dodge Exited")
