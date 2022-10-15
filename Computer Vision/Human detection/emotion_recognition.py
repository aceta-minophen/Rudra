from fer import FER
import cv2


def process_video():
    capture = cv2.VideoCapture(0)
    while True:   
        isTrue, frame = capture.read()
        emo_detector = FER(mtcnn=False)
        #captured_emotions = emo_detector.detect_emotions(frame)
        dominant_emotion, emotion_score = emo_detector.top_emotion(frame)
        cv2.putText(frame,dominant_emotion, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow("Emotion", frame)
        #Press q to exit.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    capture.release()
    cv2.destroyAllWindows
    cv2.waitKey(0)


process_video()

