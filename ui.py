import customtkinter as ctk
import tkinter as tk    
import random   
import json 
import os
import settings
from player import AudioPlayer

class MediaPlayerUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("multimedia player")
        self.geometry("270x115+400+400")
        self.configure(fg_color="#333333")
        self.resizable(False, False)
        self.overrideredirect(True)
        self.grab_set()

        self.MainUI = mainUI(self)
        self.settingsUI = settings.SettingsUI(self)

        self.topbar = ctk.CTkFrame(
            self,
            height=12,
            width=270,
            fg_color="#444444",
            corner_radius=0
        )
        self.topbar.place(x=0, y=0, anchor="nw")

        self.closeWindowButton = ctk.CTkButton(
            self.topbar,
            text="x",
            height=7,
            width=7,
            fg_color="#424242",
            hover_color="#424242",
            font=("Courier", -12, "bold"),
            text_color="#FFFFFF",
            corner_radius=0,
            command=self.destroy
        )
        self.closeWindowButton.place(x=270, y=-3, anchor="ne")

        self.minimiseWindowButton = ctk.CTkButton(
            self.topbar,
            text="-",
            height=7,
            width=7,
            fg_color="#424242",
            hover_color="#424242",
            text_color="#FFFFFF",
            font=("Courier", -12, "bold"),
            command=self.minimiseWindow
        )
        self.minimiseWindowButton.place(x=260, y=-2, anchor="ne")

        self.appNameText = ctk.CTkLabel(
            self.topbar,
            text="multimedia system",
            height=7,
            fg_color="#424242",
            text_color="#FFFFFF",
            font=("Courier", -12, "bold"),
            corner_radius=0,
        )
        self.appNameText.place(x=135, y=8, anchor="c")

        self.settingsButton = ctk.CTkButton(
            self.topbar,
            text="#",
            height=7,
            width=10,
            fg_color="#424242",
            hover_color="#424242",
            text_color="#FFFFFF",
            corner_radius=0,
            font=("Courier", -12, "bold"),
            command=self.callSettingsWindow
        )
        self.settingsButton.place(x=0, y=-2, anchor="nw")

        self.bind("<Map>", self.restore)

        self.topbar.bind("<Button-1>", self.startDrag)
        self.topbar.bind("<B1-Motion>", self.dragWindow)

        self.appNameText.bind("<Button-1>", self.startDrag)
        self.appNameText.bind("<B1-Motion>", self.dragWindow)

    def minimiseWindow(self, event=None):
        self.overrideredirect(False)
        self.withdraw()

    def restore(self, event=None):
        self.deiconify()
        self.overrideredirect(True)

    def startDrag(self, event):
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root
        self.window_start_x = self.winfo_x()
        self.window_start_y = self.winfo_y()

    def dragWindow(self, event):
        dx = event.x_root - self.drag_start_x
        dy = event.y_root - self.drag_start_y

        self.geometry(
            f"+{self.window_start_x + dx}+"
            f"{self.window_start_y + dy}"
        )

    def callSettingsWindow(self):
        self.settingsUI.openSettingsUI()


class mainUI(ctk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)

        self.mainCanvas = tk.Canvas(
            root,
            bg="#3b3b3b",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            height=99,
            width=266
        )
        self.mainCanvas.place(x=2, y=14, anchor="nw")

        self.tk.call("lower", self.mainCanvas._w)

        self.audioplayer = AudioPlayer()

        self.rewinding = False
        self.fastForwarding = False
        self.seeking = False

        self.loadFileInfoBar()
        self.loadMediaControlButtons()

    def loadFileInfoBar(self):
        self.fileInfoBar = ctk.CTkFrame(
            self.mainCanvas,
            fg_color="#000000",
            height=35,
            width=172,
            corner_radius=4
        )
        self.fileInfoBar.place(x=89, y=0, anchor="nw")

        self.timeBar = ctk.CTkFrame(
            self.mainCanvas,
            fg_color="#000000",
            height=45,
            width=80,
            corner_radius=4
        )
        self.timeBar.place(x=5, y=0, anchor="nw")

    def loadMediaControlButtons(self):

        getSongLength = self.audioplayer.get_song_length()

        self.seekBar = ctk.CTkSlider(
            self.mainCanvas,
            from_=0,
            to=100,
            width=266,
            height=6,
            progress_color="#174A7C",
            fg_color="#B0B0B0",
            button_color="#252525",
            button_hover_color="#333333",
            button_length=10
        )
        self.seekBar.set(0)

        self.seekBar.place(x=0, y=55, anchor="nw")

        self.buttonHolder = ctk.CTkFrame(
            self.mainCanvas,
            fg_color="#252525",
            height=30,
            width=256,
            corner_radius=4
        )
        self.buttonHolder.place(x=5, y=67, anchor="nw")

        # Previous
        self.previousTrackButton = ctk.CTkButton(
            self.buttonHolder,
            text="⏮",
            font=("Courier", -20, "bold"),
            height=15,
            width=20,
            fg_color="#252525",
            hover_color="#252525",
            corner_radius=4,
            command=self.audioplayer.prevTrack
        )
        self.previousTrackButton.place(x=15, y=20, anchor="c")

        # Rewind
        self.rewindButton = ctk.CTkButton(
            self.buttonHolder,
            text="⏪",
            font=("Courier", -20, "bold"),
            height=15,
            width=20,
            fg_color="#252525",
            hover_color="#252525",
            corner_radius=4,
        )
        self.rewindButton.place(x=40, y=20, anchor="c")

        # Play / Pause
        self.playPauseTrackButton = ctk.CTkButton(
            self.buttonHolder,
            text="▶",
            font=("Courier", -20, "bold"),
            height=15,
            width=20,
            fg_color="#252525",
            hover_color="#252525",
            corner_radius=4,
            command=self.togglePlayButton
        )
        self.playPauseTrackButton.place(x=65, y=17, anchor="c")

        # Fast forward
        self.fastForwardButton = ctk.CTkButton(
            self.buttonHolder,
            text="⏩",
            font=("Courier", -20, "bold"),
            height=15,
            width=20,
            fg_color="#252525",
            hover_color="#252525",
            corner_radius=4,
        )
        self.fastForwardButton.place(x=90, y=20, anchor="c")

        # Next
        self.nextTrackButton = ctk.CTkButton(
            self.buttonHolder,
            text="⏭",
            font=("Courier", -20, "bold"),
            height=15,
            width=20,
            fg_color="#252525",
            hover_color="#252525",
            corner_radius=4,
            command=self.audioplayer.nextTrack
        )
        self.nextTrackButton.place(x=115, y=20, anchor="c")


        self.chooseSongButton = ctk.CTkButton(self.mainCanvas,text="playlists")







        # Hold-to-rewind
        self.rewindButton.bind("<ButtonPress-1>",self.onRewindForwardPress, add="+")
        self.rewindButton.bind("<ButtonRelease-1>",self.onRewindForwardRelease, add="+")

        # Hold-to-fast-forward
        self.fastForwardButton.bind("<ButtonPress-1>",self.onRewindForwardPress, add="+")
        self.fastForwardButton.bind("<ButtonRelease-1>",self.onRewindForwardRelease, add="+")

        self.seekBar.bind("<ButtonPress-1>", self.seekBarPressed)
        self.seekBar.bind("<ButtonRelease-1>", self.seekBarReleased)

        self.bind("<space>", self.togglePlayButton)


     
        
    def updateSeekBar(self):
        if not self.seeking:
            current_time = self.audioplayer.get_current_song_time()

            if current_time is not None:
                self.seekBar.set(current_time)

        self.mainCanvas.after(250, self.updateSeekBar)




    def seekBarPressed(self, event):
        self.seeking = True


    def seekBarReleased(self, event):
        self.seeking = False

        value = self.seekBar.get()
        self.audioplayer.player.set_time(int(value * 1000))



    def onRewindForwardPress(self, event):
        if event.widget == self.rewindButton:
            self.rewinding = True
            self.doRewind()
            print("rewinding")

        elif event.widget == self.fastForwardButton:
            self.fastForwarding = True
            self.doFastForward()
            print("fast forwarding")

    def onRewindForwardRelease(self, event):
        if event.widget == self.rewindButton:
            self.rewinding = False
            print("not rewinding")

        elif event.widget == self.fastForwardButton:
            self.fastForwarding = False
            print("not fast forwarding")

    def doRewind(self):
        if self.rewinding:
            self.audioplayer.rewind()
            self.after(100, self.doRewind)

    def doFastForward(self):
        if self.fastForwarding:
            self.audioplayer.fast_forward()
            self.after(100, self.doFastForward)

    def togglePlayButton(self):
        state = self.audioplayer.togglePlay()

        if state == "paused":
            self.playPauseTrackButton.configure(text="▶",font=("Courier", -20, "bold"))
            self.playPauseTrackButton.place(x=65, y=18, anchor="c")


        elif self.audioplayer.songFinished:
            self.playPauseTrackButton.configure(text="⏸",font=("Courier", -24, "bold"))
            self.playPauseTrackButton.place(x=65, y=22, anchor="c")

            self.updateSeekBar()

        elif state == "no track":
            print("No track loaded")

        elif state == "song_ended":
            self.playPauseTrackButton.configure(text="↻",font=("Courier", -24, "bold"))
            self.playPauseTrackButton.place(x=65, y=22, anchor="c")

