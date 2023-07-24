import cv2
import numpy as np

# Function to turn the robot left
def turn_left():
    # Add your code here to control the robot to turn left
    print("Turning left...")

# Function to turn the robot right
def turn_right():
    # Add your code here to control the robot to turn right
    print("Turning right...")

# Function to move the robot forward
def move_forward():
    # Add your code here to control the robot to move forward
    print("Moving forward...")

# Function to move the robot backward
def move_backward():
    # Add your code here to control the robot to move backward
    print("Moving backward...")

def detect_red_circles(image):
    # Convert the image from BGR to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the red color (in HSV)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Create a binary mask for the red color
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Apply GaussianBlur to the mask to reduce noise
    mask = cv2.GaussianBlur(mask, (9, 9), 2)

    # Detect circles using the Hough Transform
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=5, maxRadius=30)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            # Draw the circle on the original image
            cv2.circle(image, (x, y), r, (0, 255, 0), 4)

            # Determine the change in radius size from the previous iteration
            global prev_radius
            delta_radius = r - prev_radius
            prev_radius = r

            if delta_radius < -1:  # If the radius is getting smaller
                move_forward()
            elif delta_radius > 1:  # If the radius is getting bigger
                move_backward()

            # Determine the center of the frame
            frame_height, frame_width, _ = image.shape
            center_x = frame_width // 2

            # Determine the relative position of the circle with respect to the center of the frame
            if x < center_x - 50:  # If the circle is on the left side of the frame
                turn_left()
            elif x > center_x + 50:  # If the circle is on the right side of the frame
                turn_right()
            else:
                print("The circle is centered.")  # The circle is roughly centered, continue moving straight

    return image

def main():
    global prev_radius
    prev_radius = 0  # Variable to store the previous radius of the red circle

    # Initialize the camera (assuming it's the default camera, change the index if needed)
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Skip if the frame is not read properly
        if not ret:
            continue

        # Detect red circles and perform robot movements
        result_frame = detect_red_circles(frame)

        # Display the resulting frame
        cv2.imshow('Red Circle Detection', result_frame)

        # Exit the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()



""" import cv2
import numpy as np

def detect_red_circles(image):
    # Convert the image from BGR to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the red color (in HSV)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Create a binary mask for the red color
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Apply GaussianBlur to the mask to reduce noise
    mask = cv2.GaussianBlur(mask, (9, 9), 2)

    # Detect circles using the Hough Transform
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=5, maxRadius=30)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            # Draw the circle on the original image
            cv2.circle(image, (x, y), r, (0, 255, 0), 4)

    return image

def main():
    # Initialize the camera (assuming it's the default camera, change the index if needed)
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Skip if the frame is not read properly
        if not ret:
            continue

        # Detect red circles
        result_frame = detect_red_circles(frame)

        # Display the resulting frame
        cv2.imshow('Red Circle Detection', result_frame)

        # Exit the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
 """