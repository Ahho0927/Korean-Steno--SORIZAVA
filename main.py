from pynput.keyboard import Listener, Key
from keybd.stroke import Stroke
from os import system
stroke = Stroke()
from keybd.keys import Keys
keys = Keys()


def text() -> None:
    print('''

 ██████╗  ██████╗  ██████╗  ██╗ ███████╗  █████╗  ██║  ██║  █████╗
██╔════╝ ██╔═══██╗ ██╔══██╗ ██║     ██╔╝ ██╔══██╗ ██║  ██║ ██╔══██╗
╚█████╗  ██║   ██║ ██████╔╝ ██║   ███╔╝  ███████║ ██║  ██║ ███████║
 ╚═══██║ ██║   ██║ ██╔══██╗ ██║  ██╔╝    ██╔══██║ ██║  ██║ ██╔══██║
██████╔╝ ╚██████╔╝ ██║  ██║ ██║ ███████╗ ██║  ██║ ╚█████╔╝ ██║  ██║
╚═════╝   ╚═════╝  ╚═╝  ╚═╝ ╚═╝ ╚══════╝ ╚═╝  ╚═╝  ╚════╝  ╚═╝  ╚═╝
          
          ''')

# =======================================

if __name__ == '__main__':
    system('cls')
    text()
    keys.block_keys(keys.KEY_BLOCKED)
    with Listener(on_press= stroke.on_press, on_release= stroke.on_release) as listener:
        listener.join()