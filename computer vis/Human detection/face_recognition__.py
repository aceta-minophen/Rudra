import cv2
import face_recognition
from fer import FER
import numpy as np
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import spoon_fork_detection

cred = credentials.Certificate(
    'rudra-x-firebase-adminsdk-e2s77-2a7119b4c9.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rudra-x-default-rtdb.firebaseio.com/'
})

# Reading from DB
ref = db.reference('Computer Vision/')
#print(ref.get())

# haar_cascade = cv2.CascadeClassifier('haar_face.xml')
# capture = cv2.VideoCapture(0)
# while True:
#     isTrue, frame = capture.read()
#     faces_rect1 = haar_cascade.detectMultiScale(
#         frame, scaleFactor=1.5, minNeighbors=3)
#     for(x, y, w, h) in faces_rect1:
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), thickness=2)
#     cv2.imshow('Detected Faces', frame)
#     if cv2.waitKey(20) & 0xFF == ord('d'):
#         break
# capture.release()
# cv2.destroyAllWindows
# cv2.waitKey(0)
KNOWN_FACES_DIR = os.path.join(os.getcwd(), 'faces')
MAX_FRAMES = 60

def encode_faces():
    # Each subfolder's name becomes our label (name)
    known_faces = []
    known_names = []
    for name in os.listdir(KNOWN_FACES_DIR):
        # Next we load every file of faces of known person
        # Load an image
        image = face_recognition.load_image_file(os.path.join(f'{KNOWN_FACES_DIR}', f'{name}'))

        # Get 128-dimension face encoding
        # Always returns a list of found faces, for this purpose we take first face only (assuming one face per image as you can't be twice on one image)
        encoding = face_recognition.face_encodings(image)[0]

        # Append encodings and name
        known_faces.append(encoding)
        known_names.append(name[:-4])
    return known_faces, known_names



def process_video():
    video_capture = cv2.VideoCapture(0)
    known_face_encodings, known_face_names = encode_faces()
    emo_detector = FER(mtcnn=False)
    # Initialize some variables

    process_this_frame = True

    while video_capture.isOpened():
        # Grab a single frame of video
        ret, frame = video_capture.read()
        if process_this_frame:
            image_np = np.asarray(frame)  
            frame, action = spoon_fork_detection.final_detection(image_np, frame)
            act_recog = db.reference('Computer Vision/Action Recognition')
            if action == 'eat':
                for key, value in act_recog.get().items():
                    if key == "Eating Food"                 :
                        if(value["Detected"] == False):
                            act_recog.child(key).update({"Detected": True})
            elif action == 'drink':
               for key, value in act_recog.get().items():  
                if key == "Drinking Water" :                  
                    if(value["Detected"] == False):
                        act_recog.child(key).update({"Detected": True})
            else:
                for key, value in act_recog.get().items():                    
                    if(value["Detected"] == True):
                        act_recog.child(key).update({"Detected": False})

           

            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            
             # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]
                
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                   
                face_names.append(name)
            if 'Tom Holland' not in face_names:
                ref.update({'Face Recognition/User': {'Name': 'Tom Holland', 'Recognized': False}})
                ref.update({'Expression Detection': {'Happy': False, 'Upset': False, 'Anxiety': False}})
        
        process_this_frame = not process_this_frame        
            
            # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            
            if name == 'Tom Holland':
                ref.update({'Face Recognition/User': {'Name': name, 'Recognized': True}})
                #captured_emotions = emo_detector.detect_emotions(frame)
                dominant_emotion, emotion_score = emo_detector.top_emotion(frame)
                if dominant_emotion == 'happy':
                    ref.update({'Expression Detection': {'Happy': True, 'Upset': False, 'Anxiety': False}})
                elif dominant_emotion == 'sad' or dominant_emotion == 'angry':
                    ref.update({'Expression Detection': {'Happy': False, 'Upset': True, 'Anxiety': False}})

                elif dominant_emotion == 'fear':
                    ref.update({'Expression Detection': {'Happy': False, 'Upset': False, 'Anxiety': True}})
                else:
                    ref.update({'Expression Detection': {'Happy': False, 'Upset': False, 'Anxiety': False}})
                cv2.putText(frame, dominant_emotion, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        
            else:
                ref.update({'Face Recognition/User': {'Name': 'Tom Holland', 'Recognized': False}})
                ref.update({'Expression Detection': {'Happy': False, 'Upset': False, 'Anxiety': False}})

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)
               
        
        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
   
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


process_video()