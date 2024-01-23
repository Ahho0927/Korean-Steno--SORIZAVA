from keyboard import block_key, unhook_all, write
from pynput.keyboard import Key, Controller
        
class Keys:
    def __init__(self) -> None:
        self.KEY_USED = "12345qwertasdfg7890-uiop[jkl;\'cvbnm,"
        self.KEY_BLOCKED = list(self.KEY_USED) + ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10']
        self.KEY_ALL = '`1234567890-=qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'

        self.key_wrote_count: dict = {key: 0 for key in list(self.KEY_ALL) + [Key.f1, Key.f2, Key.f3, Key.f4, Key.f5, Key.f6, Key.f7, Key.f8, Key.f9, Key.f10]}
        self.key_wrote_count[' '] = 0
        self.key_wrote_count['back'] = 0

    def PressReleaseBackspace(self, count=1):
        for c in range(count):
            Controller().press(Key.backspace)
            self.key_wrote_count['back'] += 1
        Controller().release(Key.backspace)

    def block_keys(self, keys):
        for key in keys:
            block_key(key)

    def unblock_keys(self):
        unhook_all()

    def send_inputs(self, inputs):
        for input in inputs:
            if input in self.KEY_ALL:
                self.key_wrote_count[input] += 1

        write(inputs)