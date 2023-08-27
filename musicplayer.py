import os
import tkinter as tk
from tkinter import ttk, filedialog
import pygame
from PIL import Image, ImageTk

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")

        self.playlist = []
        self.current_track_index = 0
        self.paused_position = 0  # Position where playback was paused
        self.playing = False  # Flag to track playback state

        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat")

        button_width = 12  # Set the desired button width

        frame = ttk.Frame(root)
        frame.pack(expand=True, padx=50, pady=10)

        # Create a label frame to group the items
        label_frame = ttk.LabelFrame(frame, text="Music Player", borderwidth=2, relief="solid")
        label_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Load and display the image
        image = Image.open("music_icon.png")  # Replace with the path to your image
        image = image.resize((100, 100), Image.LANCZOS)  # Use Image.LANCZOS for high-quality resizing
        self.photo = ImageTk.PhotoImage(image=image)
        self.image_label = tk.Label(label_frame, image=self.photo)
        self.image_label.grid(row=0, columnspan=3, pady=10)

        self.previous_button = ttk.Button(label_frame, text="Previous", command=self.previous_track, width=button_width)
        self.previous_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.play_button = ttk.Button(label_frame, text="Play", command=self.toggle_play, width=button_width)
        self.play_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.next_button = ttk.Button(label_frame, text="Next", command=self.next_track, width=button_width)
        self.next_button.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        self.stop_button = ttk.Button(label_frame, text="Pause", command=self.toggle_play, width=button_width)
        self.stop_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.load_button = ttk.Button(label_frame, text="Load Music", command=self.load_music, width=button_width)
        self.load_button.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        # Configure column weight to center-align
        label_frame.columnconfigure((0, 1, 2), weight=1)

        # Initialize the mixer module
        pygame.mixer.init()

        # Frame for loaded songs listbox
        loaded_songs_frame = ttk.Frame(frame)
        loaded_songs_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")

        # Listbox to display loaded files
        self.playlist_listbox = tk.Listbox(loaded_songs_frame, selectmode=tk.SINGLE, height=6)
        self.playlist_listbox.pack(fill=tk.BOTH, expand=True)
        self.update_playlist_listbox()

    def toggle_play(self):
        if not self.playlist:
            return

        if not self.playing:
            if self.paused_position:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.load(self.playlist[self.current_track_index])
                pygame.mixer.music.play()
            self.playing = True
        else:
            pygame.mixer.music.pause()
            self.paused_position = pygame.mixer.music.get_pos()  # Save the position
            self.playing = False
        self.update_playlist_listbox()

    def previous_track(self):
        if self.current_track_index > 0:
            self.current_track_index -= 1
            self.play_music()

    def next_track(self):
        if self.current_track_index < len(self.playlist) - 1:
            self.current_track_index += 1
            self.play_music()
            self.update_playlist_listbox()

    def play_music(self):
        if self.playlist:
            pygame.mixer.music.load(self.playlist[self.current_track_index])
            pygame.mixer.music.play()
            self.playing = True
            self.update_playlist_listbox()

    def load_music(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
        self.playlist = list(file_paths)
        if self.playlist:
            self.current_track_index = 0
        self.update_playlist_listbox()

    def update_playlist_listbox(self):
        self.playlist_listbox.delete(0, tk.END)
        
        for idx, track in enumerate(self.playlist):
            file_name = os.path.basename(track)  # Get the file name from the path
            self.playlist_listbox.insert(tk.END, file_name)
            
        # Update the appearance of all items
        for i in range(len(self.playlist)):
            if i == self.current_track_index:
                self.playlist_listbox.itemconfig(i, {'bg': 'light blue', 'selectbackground': 'light blue'})
            else:
                self.playlist_listbox.itemconfig(i, {'bg': 'white', 'selectbackground': 'white'})





root = tk.Tk()
app = MusicPlayer(root)
root.mainloop()

# Clean up when done
pygame.quit()
