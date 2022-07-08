import cv2 as cv
haar_cascade = cv.CascadeClassifier('haar_face.xml')
capture = cv.VideoCapture(0)
while True:
    isTrue, frame = capture.read()
    faces_rect1 = haar_cascade.detectMultiScale(
        frame, scaleFactor=1.5, minNeighbors=3)
    for(x, y, w, h) in faces_rect1:
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), thickness=2)
    cv.imshow('Detected Faces', frame)
    if cv.waitKey(20) & 0xFF == ord('d'):
        break
capture.release()
cv.destroyAllWindows

cv.waitKey(0)
