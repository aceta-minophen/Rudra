import cv2
import threading

# Global variable to store the camera object
camera = None

# Function to access the camera and start capturing frames
def access_camera():
    global camera
    camera = cv2.VideoCapture(0)  # 0 represents the default camera, change if you have multiple cameras

    if not camera.isOpened():
        print("Error: Could not access the camera.")
        return

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Process the frame here if needed (e.g., apply filters or manipulations)
        processed_frame = frame.copy()

        # Display the processed frame in a window named "Processed Frame"
        cv2.imshow("Processed Frame", processed_frame)

        # Exit the loop when the user presses 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows when done
    camera.release()
    cv2.destroyAllWindows()

# Function 1 to perform some processing on the camera image
def process_image1():
    global camera
    while True:
        if camera is not None:
            # Capture a frame from the camera
            ret, frame = camera.read()
            if not ret:
                break

            # Process the frame (e.g., apply a different filter)
            processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Display the processed frame in a window named "Processed Frame 1"
            cv2.imshow("Processed Frame 1", processed_frame)

        # Exit the loop when the user presses 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close the OpenCV window for this function when done
    cv2.destroyAllWindows()

# Function 2 to perform some other processing on the camera image
def process_image2():
    global camera
    while True:
        if camera is not None:
            # Capture a frame from the camera
            ret, frame = camera.read()
            if not ret:
                break

            # Process the frame (e.g., apply a different filter or transformation)
            processed_frame = cv2.flip(frame, 1)  # Flip the frame horizontally

            # Display the processed frame in a window named "Processed Frame 2"
            cv2.imshow("Processed Frame 2", processed_frame)

        # Exit the loop when the user presses 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close the OpenCV window for this function when done
    cv2.destroyAllWindows()

# Create and start the threads for accessing the camera and processing images
camera_thread = threading.Thread(target=access_camera)
process_thread1 = threading.Thread(target=process_image1)
process_thread2 = threading.Thread(target=process_image2)

camera_thread.start()
process_thread1.start()
process_thread2.start()

# Wait for all threads to finish (this will block the main thread until all threads complete)
camera_thread.join()
process_thread1.join()
process_thread2.join()
