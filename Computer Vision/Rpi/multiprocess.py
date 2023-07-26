import cv2
import multiprocessing

# Function to access the camera and start capturing frames
def access_camera(queue):
    camera = cv2.VideoCapture(0)  # 0 represents the default camera, change if you have multiple cameras

    if not camera.isOpened():
        print("Error: Could not access the camera.")
        return

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Put the frame into the queue for processing
        queue.put(frame)

        # Display the original frame in a window named "Processed Frame"
        cv2.imshow("Processed Frame", frame)

        # Exit the loop when the user presses 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows when done
    camera.release()
    cv2.destroyAllWindows()

# Function to perform some processing on the camera image
def process_image(queue):
    while True:
        frame = queue.get()

        # Process the frame (e.g., apply a different filter or transformation)
        processed_frame = cv2.flip(frame, 1)  # Flip the frame horizontally

        # Display the processed frame in a window named "Processed Frame"
        cv2.imshow("Processed Frame", processed_frame)

        # Exit the loop when the user presses 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Close the OpenCV window for this function when done
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Create a multiprocessing queue to pass frames between processes
    queue = multiprocessing.Queue()

    # Create and start the processes for accessing the camera and processing images
    camera_process = multiprocessing.Process(target=access_camera, args=(queue,))
    process_process = multiprocessing.Process(target=process_image, args=(queue,))

    camera_process.start()
    process_process.start()

    # Wait for all processes to finish (this will block the main process until all processes complete)
    camera_process.join()
    process_process.join()
