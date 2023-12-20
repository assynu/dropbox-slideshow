def Start():
    import dropbox
    import cv2
    import os
    import numpy as np
    import console

    # Configurable parameters
    access_token = 'sl.BrrKbCA9pviKx2I3qkzQ6K-FGWPvz1CUFHwUk5-ZH9WgHppTx3fKgRp159ZYJVSrE9mRzLeOOUQ0LqE4BcY-00ZHSDYoZNhLeN6X3AEf0WOhhpIO_5GVK8HtNdo4t_YI5tgZMq8YykSfdSM_UsYE'
    dropbox_folder = '/Slideshow'
    local_folder = 'Media'
    display_time = 5  # time in seconds to display each image
    transition_time = 5  # time in seconds for transition

    # Initialize Dropbox client
    dbx = dropbox.Dropbox(
        app_key='5nc9p3co7c67q48',
        app_secret='07uqju6grj4qhdu',
        oauth2_refresh_token='88WOBOYVU34AAAAAAAAAAREA8JfuVnSWkkijHCZfyiG44V0c3lZwpy-6uSn-shuy'
    )
    
    cv2.namedWindow('Slideshow', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Slideshow', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    # Get screen resolution
    import ctypes
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    
    while True:
        # Get list of files in the Dropbox folder
        files = dbx.files_list_folder(dropbox_folder).entries
        
        files.sort(key=lambda x: x.name)

        img = None
        for file in files:
            # Download each file
            local_path = f'{local_folder}/{file.name}'

            console.Log(f'Downloading \"{file.name}\"..')

            dbx.files_download_to_file(local_path, file.path_lower)
            
            # Display the image or video
            if file.name.endswith('.mp4'):
                # Display video
                cap = cv2.VideoCapture(local_path)
                fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frames per second
                delay = int(1000 / fps)  # Calculate the delay for a single frame
                frame_count = 0  # Initialize frame count

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Resize the frame
                    frame = cv2.resize(frame, (screen_width, screen_height))

                    # Add fade-in effect for the first 30 frames of the video
                    if img is not None and frame_count < 30:
                        alpha = frame_count / 30
                        frame = cv2.addWeighted(frame, alpha, img, 1 - alpha, 0)
                    cv2.imshow('Slideshow', frame)

                    if cv2.waitKey(delay) & 0xFF == ord('q'):  # Use the calculated delay here
                        break
                    frame_count += 1
                cap.release()

                # Display image
                next_img = cv2.imread(local_path)

                # Get the display size
                display_size = (screen_width, screen_height)

                # Check if the image size is not the same as the display size
                if next_img is not None and next_img.shape[:2] != display_size:
                    # Resize the image
                    next_img = cv2.resize(next_img, display_size)

                if img is not None and next_img is not None:
                    # Transition from img to next_img
                    for alpha in range(30, -1, -1):
                        beta = 1 - alpha / 30

                        # Ensure both images have the same size
                        if img.shape[:2] != next_img.shape[:2]:
                            img = cv2.resize(img, (next_img.shape[1], next_img.shape[0]))

                        dst = cv2.addWeighted(img, alpha / 30, next_img, beta, 0)
                        cv2.imshow('Slideshow', dst)
                        cv2.waitKey(delay)
            else:
                # Display image
                next_img = cv2.imread(local_path)

                # Get the display size
                display_size = (screen_width, screen_height)

                # Check if the image size is not the same as the display size
                if next_img.shape[:2] != display_size:
                    # Resize the image
                    next_img = cv2.resize(next_img, display_size)

                if img is not None:
                    # Transition from img to next_img
                    for i in np.linspace(0, 1, transition_time * 100):
                        alpha = i
                        beta = 1.0 - alpha
                        dst = cv2.addWeighted(next_img, alpha, img, beta, 0.0)
                        cv2.imshow('Slideshow', dst)
                        cv2.waitKey(1)
                img = next_img
                cv2.imshow('Slideshow', img)
                cv2.waitKey(display_time * 1000)
            
            # Delete the local file
            os.remove(local_path)

    cv2.destroyAllWindows()