# music_player.py

import pygame
import time
from tkinter import END
from os.path import basename
from logger import log

# Global variables
is_paused = False
start_time = 0
paused_time = 0
current_song_duration = 0
playlist_paths = []

def init_pygame():
    pygame.init()
    pygame.mixer.init()

def add_song(playlist):
    from tkinter import filedialog
    from os.path import basename

    song_path = filedialog.askopenfilename(initialdir="/home/pavan/Music", title="Choose a Song", filetypes=(("MP3 Files", "*.mp3"),))
    if song_path:
        song_name = basename(song_path)
        playlist.insert(END, song_name)
        playlist_paths.append(song_path)
        log(f"Added song: {song_name}")

def toggle_play_pause(playlist, play_pause_button, duration_bar, time_label):
    global is_paused, start_time, paused_time, current_song_duration
    if is_paused:
        pygame.mixer.music.unpause()
        is_paused = False
        start_time = time.time() - paused_time
        play_pause_button.config(text="⏸︎")
        update_duration_bar(duration_bar, time_label, current_song_duration)
        log("Resumed song")
    else:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            is_paused = True
            paused_time = time.time() - start_time
            play_pause_button.config(text="⏵︎")
            log("Paused song")
        else:
            if playlist.curselection():
                song_index = playlist.curselection()[0]
                song_path = playlist_paths[song_index]
                pygame.mixer.music.load(song_path)
                pygame.mixer.music.play(loops=0)
                start_time = time.time()
                current_song_duration = pygame.mixer.Sound(song_path).get_length()
                play_pause_button.config(text="⏸︎")
                update_duration_bar(duration_bar, time_label, current_song_duration)
                log(f"Playing song: {basename(song_path)}")
            else:
                log("No song selected.")

def stop_song(play_pause_button, duration_bar, time_label):
    global is_paused
    pygame.mixer.music.stop()
    is_paused = False
    duration_bar['value'] = 0
    time_label.config(text="0:00 / 0:00")
    play_pause_button.config(text="⏵︎")
    log("Stopped song")

def next_song(playlist, toggle_play_pause):
    current_index = playlist.curselection()[0]
    next_index = (current_index + 1) % playlist.size()
    playlist.selection_clear(0, END)
    playlist.selection_set(next_index)
    playlist.activate(next_index)
    toggle_play_pause()
    log("Playing next song")

def prev_song(playlist, toggle_play_pause):
    current_index = playlist.curselection()[0]
    prev_index = (current_index - 1) % playlist.size()
    playlist.selection_clear(0, END)
    playlist.selection_set(prev_index)
    playlist.activate(prev_index)
    toggle_play_pause()
    log("Playing previous song")

def update_duration_bar(duration_bar, time_label, song_duration):
    global is_paused, start_time
    while pygame.mixer.music.get_busy() or is_paused:
        if not is_paused:
            elapsed_time = time.time() - start_time
            progress = (elapsed_time / song_duration) * 100
            duration_bar['value'] = progress

            # Update time display
            current_time = time.strftime("%M:%S", time.gmtime(elapsed_time))
            total_time = time.strftime("%M:%S", time.gmtime(song_duration))
            time_label.config(text=f"{current_time} / {total_time}")

            duration_bar.update()
            time.sleep(1)
        else:
            duration_bar.update()
            time.sleep(1)

def seek_song(event, duration_bar):
    global start_time, current_song_duration
    click_x = event.x
    song_position = (click_x / duration_bar.winfo_width()) * current_song_duration
    pygame.mixer.music.set_pos(song_position)
    start_time = time.time() - song_position
    log(f"Seeked song to position: {song_position:.2f} seconds")
