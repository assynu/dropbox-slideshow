import threading
import console
import keyboardInput
import slideshow

def main():
    console.clear()

    console.log("Initializing...")

    slideshowThread = threading.Thread(target=slideshow.Start)
    keyboardLietenrThread = threading.Thread(target=keyboardInput.Listener)

    slideshowThread.start()
    keyboardLietenrThread.start()

    slideshowThread.join()
    keyboardLietenrThread.join()

if __name__ == '__main__':
    main()
