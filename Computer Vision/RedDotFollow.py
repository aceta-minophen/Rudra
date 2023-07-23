import cv2
import numpy as np

# Variables to store the previous position of the red circle
prev_x = 0
prev_y = 0

# Flag to indicate the last movement direction (0 for left, 1 for right)
last_direction = 0

# Function to turn the robot left
def turn_left():
    global last_direction
    # Add your code here to control the robot to turn left
    print("Turning left...")
    last_direction = 0

# Function to turn the robot right
def turn_right():
    global last_direction
    # Add your code here to control the robot to turn right
    print("Turning right...")
    last_direction = 1

# Function to move the robot forward
def move_forward():
    # Add your code here to control the robot to move forward
    print("Moving forward...")

# Function to move the robot backward
def move_backward():
    # Add your code here to control the robot to move backward
    print("Moving backward...")

# Function to find and track the red circle
def find_red_circle(frame):
    global prev_x, prev_y, prev_radius  # Declare prev_radius as a global variable
    # Convert the frame from BGR to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds of the red color in HSV
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    # Create a binary mask for the red color
    red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)

    # Find contours in the mask
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour (presumed to be the red circle)
    max_contour = None
    max_contour_area = 0

    for contour in contours:
        # Filter contours based on their area and circularity
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)

        if perimeter > 0:  # Skip contours with small or zero perimeter
            circularity = 4 * np.pi * area / (perimeter * perimeter)

            if 1000 < area < 50000 and 0.7 < circularity < 1.3:
                if area > max_contour_area:
                    max_contour_area = area
                    max_contour = contour

    # Draw the circle on the frame if a valid contour is found
    if max_contour is not None:
        # Get the rotated bounding box for the contour
        rect = cv2.minAreaRect(max_contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # Draw the rotated bounding box on the frame
        cv2.drawContours(frame, [box], 0, (0, 255, 255), 2)

        # Find the minimum enclosing circle for the contour
        ((x, y), radius) = cv2.minEnclosingCircle(max_contour)
        if radius > 5:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.putText(frame, "Red Circle", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            print("Red Circle Coordinates: x={}, y={}, radius={}".format(int(x), int(y), int(radius)))

            # Determine the center of the frame
            frame_height, frame_width, _ = frame.shape
            center_x = frame_width // 2

            # Determine the relative position of the circle with respect to the center of the frame
            if x < center_x - 50:  # If the circle is on the left side of the frame
                turn_left()
            elif x > center_x + 50:  # If the circle is on the right side of the frame
                turn_right()
            else:
                print("The circle is centered.")  # The circle is roughly centered, continue moving straight
                if last_direction == 0:
                    turn_left()
                elif last_direction == 1:
                    turn_right()

            # Calculate the change in position of the circle
            delta_x = x - prev_x
            delta_y = y - prev_y

            # Update the previous position with the current position for the next iteration
            prev_x = x
            prev_y = y

            # Determine if the circle is going away or coming towards the camera based on the change in radius
            if radius < prev_radius:  # If the radius is getting smaller
                move_forward()
            elif radius > prev_radius:  # If the radius is getting bigger
                move_backward()

            # Update the previous radius for the next iteration
            prev_radius = radius

        else:
            # Circle not detected, continue turning in the last-seen direction
            if last_direction == 0:
                turn_left()
            elif last_direction == 1:
                turn_right()

# Main function to capture video from the camera and process it
def main():
    global prev_radius
    prev_radius = 0  # Variable to store the previous radius of the red circle

    # Open the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if ret:
            # Find and track the red circle
            find_red_circle(frame)

            # Show the frame with the red circle
            cv2.imshow("Red Circle Tracker", frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
