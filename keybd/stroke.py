from pynput.keyboard import Key
from keybd.translation import Translation
translation = Translation()
from keybd.keys import Keys
keys = Keys()

KEYBOARD_LAYOUT = '''
    1 2 3 4 5     7 8 9 0 -
    q w e r t     u i o p [
    a s d f g     j k l ; '
          c v b n m ,
'''

class Stroke:
    def __init__(self) -> None:
        self.current_pressed_key = set()
        self.pressed_key = set()

    def on_press(self, key: Key):
        try:
            key = key.char
        except AttributeError:
            pass

        if key in list(keys.KEY_USED) or key in translation.KEY_NUM:
            if keys.key_wrote_count[key] == 0:
                self.current_pressed_key.add(key)
                self.pressed_key.add(key)
            else:
                keys.key_wrote_count[key] -= 1
                
        if key == Key.esc:
            return False
        if key == Key.backspace:
            if keys.key_wrote_count['back']:
                keys.key_wrote_count['back'] -= 1

    def on_release(self, key: Key):
        try:
            try:
                key = key.char
            except AttributeError:
                pass

            if key in list(keys.KEY_USED) or key in translation.KEY_NUM:
                self.current_pressed_key.remove(key)

                if not self.current_pressed_key:
                    print(self.pressed_key)
                    result = translation.get_result(self.pressed_key)
                    print(result)
                    print(translation.previous_result)
                    if translation.stick:
                        keys.PressReleaseBackspace()

                    if result:
                        keys.send_inputs(result)

                    self.reset(result)
        except Exception:
            pass

    def reset(self, result):
        self.pressed_key = set()
        translation.stick = False
        if len(translation.previous_result) > 10:
            translation.previous_result = translation.previous_result[2:]
        if result:
            translation.previous_result += result