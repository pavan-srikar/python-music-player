import pygame
from tkinter import Tk, Button, Listbox, filedialog, END, ACTIVE, Label
from tkinter.ttk import Progressbar
import time

# Initialize Pygame
pygame.init()

# Create the Tkinter window
root = Tk()
root.title("Music Player")

# Create a listbox to display the playlist
playlist = Listbox(root, bg="black", fg="white", width=50, selectbackground="gray", selectforeground="black")
playlist.pack(pady=20)

# Create a label to display current and total duration
time_label = Label(root, text="0:00 / 0:00")
time_label.pack()

# Create a duration bar
duration_bar = Progressbar(root, orient="horizontal", length=200, mode="determinate")
duration_bar.pack(pady=10)

# Global variables
is_paused = False
start_time = 0
paused_time = 0

# Function to add songs to the playlist
def add_song():
    song = filedialog.askopenfilename(initialdir="/home/pavan/Music", title="Choose a Song", filetypes=(("MP3 Files", "*.mp3"),))
    playlist.insert(END, song)

# Function to play selected song
def play_song():
    global is_paused, start_time, paused_time
    if is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
        start_time = time.time() - paused_time
    else:
        song = playlist.get(ACTIVE)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        start_time = time.time()
        song_duration = pygame.mixer.Sound(song).get_length()
        update_duration_bar(song_duration)

# Function to pause the music
def pause_song():
    global is_paused, paused_time
    if not is_paused:
        pygame.mixer.music.pause()
        is_paused = True
        paused_time = time.time() - start_time

# Function to stop the music
def stop_song():
    global is_paused
    pygame.mixer.music.stop()
    is_paused = False
    duration_bar['value'] = 0
    time_label.config(text="0:00 / 0:00")

# Function to update the duration bar
def update_duration_bar(song_duration):
    while pygame.mixer.music.get_busy() and not is_paused:
        elapsed_time = time.time() - start_time
        progress = (elapsed_time / song_duration) * 100
        duration_bar['value'] = progress

        # Update time display
        current_time = time.strftime("%M:%S", time.gmtime(elapsed_time))
        total_time = time.strftime("%M:%S", time.gmtime(song_duration))
        time_label.config(text=f"{current_time} / {total_time}")

        root.update()
        time.sleep(1)

# Create buttons for adding songs, playing, pausing, and stopping
add_button = Button(root, text="Add Song", command=add_song)
add_button.pack(pady=10)
play_button = Button(root, text="Play", command=play_song)
play_button.pack(pady=10)
pause_button = Button(root, text="Pause", command=pause_song)
pause_button.pack(pady=10)
stop_button = Button(root, text="Stop", command=stop_song)
stop_button.pack(pady=10)

# Initialize the mixer
pygame.mixer.init()

root.mainloop()
