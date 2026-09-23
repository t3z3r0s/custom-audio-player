import ui

print("MAIN.PY STARTED")

if __name__ == "__main__":
    mediaplayer = ui.MediaPlayerUI()

    try:
        mediaplayer.mainloop()
    except KeyboardInterrupt:
        print("keyboard interrupt")
