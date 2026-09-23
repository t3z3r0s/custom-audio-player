from tkinter import filedialog
import vlc


class AudioPlayer:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        





        self.player.event_manager().event_attach(
            vlc.EventType.MediaPlayerEndReached,
            self.songFinished
        )



        
    def selectFiles(self):
        self.tracks = filedialog.askopenfilenames()

        if self.tracks:
            media = self.instance.media_new(self.tracks[0])
            self.player.set_media(media)

            return True

        return False



    def togglePlay(self):
        if self.player.get_media() is None:
            self.selectFiles()
            return "no track"

        elif self.player.is_playing():
            self.player.pause()
            return "paused"

        else:
            self.player.play()
            self.songFinished = False
            return "resumed"

    
    self.songFinished = False

    def songFinished(self, event):
        self.songFinished = True


    def nextTrack(self):
        pass

    def prevTrack(self):
        pass


    def get_song_length(self, formatted=False):
        length_ms = self.player.get_length()

        if length_ms == -1:
            return None

        seconds = length_ms / 1000

        if formatted:
            minutes = seconds // 60
            seconds %= 60
            return f"{minutes}:{seconds:02d}"

        return seconds


    def get_current_song_time(self):
        return self.player.get_time() / 1000
             


    def fast_forward(self):
        current_time = self.player.get_time()
        self.player.set_time(current_time + 1000)

    def rewind(self):
        current_time = self.player.get_time()
        self.player.set_time(current_time - 1000)

    def cleanup(self):
        self.player.stop()
        self.player.release()
        self.instance.release()
