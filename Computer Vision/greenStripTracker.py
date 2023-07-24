import cv2
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
