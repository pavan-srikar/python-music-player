# main.py

from gui import create_gui
from music_player import init_pygame

def main():
    init_pygame()
    root = create_gui()
    root.mainloop()

if __name__ == "__main__":
    main()
