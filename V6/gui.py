# gui.py

from tkinter import Tk, Button, Listbox, Label, Frame
from tkinter.ttk import Progressbar
from music_player import add_song, toggle_play_pause, stop_song, next_song, prev_song, seek_song
from logger import log

def create_gui():
    root = Tk()
    root.title("Music Player")

    # Create a main frame
    main_frame = Frame(root)
    main_frame.pack(pady=20)

    # Create a frame for the song list and controls
    song_list_frame = Frame(main_frame)
    song_list_frame.grid(row=0, column=0, padx=10)

    # Create a listbox to display the playlist
    playlist = Listbox(song_list_frame, bg="black", fg="white", width=50, selectbackground="gray", selectforeground="black")
    playlist.pack(pady=20)

    # Create a label to display current and total duration
    time_label = Label(song_list_frame, text="0:00 / 0:00")
    time_label.pack()

    # Create a duration bar
    duration_bar = Progressbar(song_list_frame, orient="horizontal", length=400, mode="determinate")
    duration_bar.pack(pady=10)

    # Bind the progress bar click event
    duration_bar.bind("<Button-1>", lambda event: seek_song(event, duration_bar))

    # Create buttons for adding songs, playing/pausing, stopping, next and previous songs
    button_frame = Frame(song_list_frame)
    button_frame.pack(pady=10)

    add_button = Button(button_frame, text="Add Song", command=lambda: add_song(playlist))
    add_button.grid(row=0, column=0, padx=5)

    prev_button = Button(button_frame, text="《", command=lambda: prev_song(playlist, lambda: toggle_play_pause(playlist, play_pause_button, duration_bar, time_label)))
    prev_button.grid(row=0, column=1, padx=5)

    play_pause_button = Button(button_frame, text="⏵︎", command=lambda: toggle_play_pause(playlist, play_pause_button, duration_bar, time_label))
    play_pause_button.grid(row=0, column=2, padx=5)

    next_button = Button(button_frame, text="》", command=lambda: next_song(playlist, lambda: toggle_play_pause(playlist, play_pause_button, duration_bar, time_label)))
    next_button.grid(row=0, column=3, padx=5)

    stop_button = Button(button_frame, text="⏹︎", command=lambda: stop_song(play_pause_button, duration_bar, time_label))
    stop_button.grid(row=0, column=4, padx=5)

    # Button with "uxbypavan"
    my_button = Button(button_frame, text="uxbypavan", command=open_portfolio)
    my_button.grid(row=0, column=5, padx=5)

    return root

def open_portfolio():
    import webbrowser
    webbrowser.open("https://uxbypavan.framer.ai")
    log("Opened portfolio")
