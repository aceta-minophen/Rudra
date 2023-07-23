import cv2
import numpy as np

# Function to calibrate the color range for rectangle tracking
def calibrate_color_range(frame):
    def nothing(x):
        pass

    # Create a window for trackbars
    cv2.namedWindow('Calibration')

    # Set default HSV color range values
    h_min, h_max, s_min, s_max, v_min, v_max = 0, 10, 120, 255, 70, 255

    # Create trackbars to adjust HSV color range
    cv2.createTrackbar('H min', 'Calibration', h_min, 180, nothing)
    cv2.createTrackbar('H max', 'Calibration', h_max, 180, nothing)
    cv2.createTrackbar('S min', 'Calibration', s_min, 255, nothing)
    cv2.createTrackbar('S max', 'Calibration', s_max, 255, nothing)
    cv2.createTrackbar('V min', 'Calibration', v_min, 255, nothing)
    cv2.createTrackbar('V max', 'Calibration', v_max, 255, nothing)

    while True:
        # Get current trackbar positions
        h_min = cv2.getTrackbarPos('H min', 'Calibration')
        h_max = cv2.getTrackbarPos('H max', 'Calibration')
        s_min = cv2.getTrackbarPos('S min', 'Calibration')
        s_max = cv2.getTrackbarPos('S max', 'Calibration')
        v_min = cv2.getTrackbarPos('V min', 'Calibration')
        v_max = cv2.getTrackbarPos('V max', 'Calibration')

        # Create HSV color range from the trackbar values
        lower_color = np.array([h_min, s_min, v_min])
        upper_color = np.array([h_max, s_max, v_max])

        # Convert the frame from BGR to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create a binary mask for the selected color range
        mask = cv2.inRange(hsv_frame, lower_color, upper_color)

        # Show the mask in the calibration window
        cv2.imshow('Calibration', mask)

        # Press 'ESC' key to exit calibration
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Destroy the calibration window
    cv2.destroyAllWindows()

    # Return the selected HSV color range
    return lower_color, upper_color

# Function to find and track the colored rectangle based on the calibrated color range
def find_colored_rectangle(frame, lower_color, upper_color):
    # Convert the frame from BGR to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a binary mask for the selected color range
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the best match rectangle (presumed to be the colored rectangle)
    best_match_contour = None
    best_match_score = float('inf')

    # Hu Moments of a perfect rectangle
    perfect_rectangle = np.array([[0, 0], [0, 1], [1, 1], [1, 0]], dtype=np.float32)
    perfect_rectangle_moments = cv2.matchShapes(perfect_rectangle, perfect_rectangle, cv2.CONTOURS_MATCH_I3, 0)

    for contour in contours:
        # Filter contours based on their area and aspect ratio
        area = cv2.contourArea(contour)
        if area > 1000:
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            if len(approx) == 4:  # Check if the contour is a quadrilateral
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w) / h
                if 0.7 < aspect_ratio < 1.3:
                    # Calculate Hu Moments and compare with the Hu Moments of a perfect rectangle
                    moments = cv2.matchShapes(approx, perfect_rectangle, cv2.CONTOURS_MATCH_I3, 0)
                    if moments < best_match_score:
                        best_match_score = moments
                        best_match_contour = approx

    # Draw the rectangle on the frame if a valid contour is found
    if best_match_contour is not None:
        x, y, w, h = cv2.boundingRect(best_match_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, "Colored Rectangle", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # Print the coordinates of the center of the rectangle
        center_x = x + w // 2
        center_y = y + h // 2
        print("Colored Rectangle Center Coordinates: (x={}, y={})".format(center_x, center_y))

# Main function to capture video from the camera and process it
def main():
    # Open the camera
    cap = cv2.VideoCapture(0)

    # Calibrate the color range for the colored rectangle
    _, frame = cap.read()
    lower_color, upper_color = calibrate_color_range(frame)

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if ret:
            # Find and track the colored rectangle
            find_colored_rectangle(frame, lower_color, upper_color)

            # Show the frame with the colored rectangle
            cv2.imshow("Colored Rectangle Tracker", frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
