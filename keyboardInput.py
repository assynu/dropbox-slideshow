def Listener():
    import os
    import console
    
    from pynput.keyboard import Key, Listener

    def on_release(key):
        if key == Key.esc:
            console.Log("Exiting...")
            os._exit(0)

    while True:
        with Listener(on_release=on_release) as listener:
            listener.join()