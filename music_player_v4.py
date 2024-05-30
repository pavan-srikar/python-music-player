import pygame
from tkinter import Tk, Button, Listbox, filedialog, END, ACTIVE, Label, Frame
from tkinter.ttk import Progressbar
import time
from os.path import basename

# Initialize Pygame
pygame.init()

# Create the Tkinter window
root = Tk()
root.title("Music Player")

# Global variables
is_paused = False
start_time = 0
paused_time = 0
current_song_duration = 0

# Function to add songs to the playlist
def add_song():
    song_path = filedialog.askopenfilename(initialdir="/home/pavan/Music", title="Choose a Song", filetypes=(("MP3 Files", "*.mp3"),))
    if song_path:
        song_name = basename(song_path)
        playlist.insert(END, song_name)
        playlist_paths.append(song_path)

# Function to play or pause the song
def toggle_play_pause():
    global is_paused, start_time, paused_time, current_song_duration
    if is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
        start_time = time.time() - paused_time
        play_pause_button.config(text="||")
        update_duration_bar(current_song_duration)
    else:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            is_paused = True
            paused_time = time.time() - start_time
            play_pause_button.config(text=">")
        else:
            if playlist.curselection():
                song_index = playlist.curselection()[0]
                song_path = playlist_paths[song_index]
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play(loops=0)
                start_time = time.time()
                current_song_duration = pygame.mixer.Sound(song_path).get_length()
                play_pause_button.config(text="||")
                update_duration_bar(current_song_duration)
            else:
                print("No song selected.")


# Function to stop the music
def stop_song():
    global is_paused
    pygame.mixer.music.stop()
    is_paused = False
    duration_bar['value'] = 0
    time_label.config(text="0:00 / 0:00")
    play_pause_button.config(text=">")

# Function to update the duration bar
def update_duration_bar(song_duration):
    while pygame.mixer.music.get_busy() or is_paused:
        if not is_paused:
            elapsed_time = time.time() - start_time
            progress = (elapsed_time / song_duration) * 100
            duration_bar['value'] = progress

            # Update time display
            current_time = time.strftime("%M:%S", time.gmtime(elapsed_time))
            total_time = time.strftime("%M:%S", time.gmtime(song_duration))
            time_label.config(text=f"{current_time} / {total_time}")

            root.update()
            time.sleep(1)
        else:
            root.update()
            time.sleep(1)

# Function to seek the song position based on the progress bar click
def seek_song(event):
    global start_time
    click_x = event.x
    song_position = (click_x / duration_bar.winfo_width()) * current_song_duration
    pygame.mixer.music.set_pos(song_position)
    start_time = time.time() - song_position

# Create a main frame
main_frame = Frame(root)
main_frame.pack(pady=20)

# Create a frame for the song list and controls
song_list_frame = Frame(main_frame)
song_list_frame.grid(row=0, column=0, padx=10)

# Create a listbox to display the playlist
playlist = Listbox(song_list_frame, bg="black", fg="white", width=50, selectbackground="gray", selectforeground="black")
playlist.pack(pady=20)

# List to store the full paths of the songs
playlist_paths = []

# Create a label to display current and total duration
time_label = Label(song_list_frame, text="0:00 / 0:00")
time_label.pack()

# Create a duration bar
duration_bar = Progressbar(song_list_frame, orient="horizontal", length=400, mode="determinate")
duration_bar.pack(pady=10)

# Bind the progress bar click event
duration_bar.bind("<Button-1>", seek_song)

# Create buttons for adding songs, playing/pausing, and stopping
button_frame = Frame(song_list_frame)
button_frame.pack(pady=10)

add_button = Button(button_frame, text="Add Song", command=add_song)
add_button.grid(row=0, column=0, padx=5)

play_pause_button = Button(button_frame, text=">", command=toggle_play_pause)
play_pause_button.grid(row=0, column=1, padx=5)

stop_button = Button(button_frame, text="Stop", command=stop_song)
stop_button.grid(row=0, column=2, padx=5)

# Initialize the mixer
pygame.mixer.init()

root.mainloop()
