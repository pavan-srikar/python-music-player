import os
import pygame
from tkinter import Tk, Button, Listbox, filedialog, END, ACTIVE

# Initialize Pygame
pygame.init()

# Create the Tkinter window
root = Tk()
root.title("Music Player")

# Create a listbox to display the playlist
playlist = Listbox(root, bg="black", fg="white", width=50, selectbackground="gray", selectforeground="black")
playlist.pack(pady=20)

# Function to add songs to the playlist
def add_song():
    song = filedialog.askopenfilename(initialdir="/home/pavan/Music", title="Choose a Song", filetypes=(("MP3 Files", "*.mp3"),))
    playlist.insert(END, song)

# Function to play selected song
def play_song():
    song = playlist.get(ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

# Function to stop the music
def stop_song():
    pygame.mixer.music.stop()

# Create buttons for adding songs, playing, and stopping
add_button = Button(root, text="Add Song", command=add_song)
add_button.pack(pady=10)
play_button = Button(root, text="Play", command=play_song)
play_button.pack(pady=10)
stop_button = Button(root, text="Stop", command=stop_song)
stop_button.pack(pady=10)

# Initialize the mixer
pygame.mixer.init()

root.mainloop()
