import cv2
import sys

s=0
if len(sys.argv) >1:
    s= sys.argv[1]

source = cv2.VideoCapture(s+cv2.CAP_DSHOW)

win_name = 'Camera'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

#reading the modal
net = cv2.dnn.readNetFromCaffe("deploy.prototxt", 
                               "res10_300x300_ssd_iter_140000_fp16.caffemodel")

#modal parameters
in_width = 300                        #size
in_height = 300                       #size
mean = [104, 117, 123]                #mean values of colour chains of images in training model
conf_threshold = 0.7                  #this value will detect sensitivity of your detections

while cv2.waitKey(1)!=27:             #while not esc(key)
    has_frame, frame = source.read()  #reading one frame at a time from video feed
    if not has_frame:
        break
    frame = cv2.flip(frame,1)         #flipping the frame horizontally as per our convinience 
    frame_height = frame.shape[0]     #retreiving size of the video frame
    frame_width = frame.shape[1]      #retreiving size of the video frame

    # create a 4D blob from a frame
    blob = cv2.dnn.blobFromImage(frame, 1.0, (in_width, in_height), mean ,swapRB = False, crop= False)  
    # preprocessing of the image in above line(image frame from video stream, scale factor(may change), (input width, height of image), mean value(will be subtractedd from all the images), swapRB(RB=RedBlue) false because opencv and caffe has same convention, resizing of image is false) 

    #run a model
    net.setInput(blob)                    #prepares blob for inference
    detections = net.forward()            #performs inference on above line

    for i in range(detections.shape[2]):  #looping over all the detections
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:   
            # bounding box coordinates
            x_left_bottom = int(detections[0, 0, i, 3] * frame_width)
            y_left_bottom = int(detections[0, 0, i, 4] * frame_height)
            x_right_top = int(detections[0, 0, i, 5] * frame_width)
            y_right_top = int(detections[0, 0, i, 6] * frame_height)

            #creating a rectangle around the detections in the frame
            cv2.rectangle(frame, (x_left_bottom, y_left_bottom), (x_right_top, y_right_top), (0, 255, 0))
            #add text indicating confidence
            label = "Confidence: %.4f" % confidence 
            label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

            cv2.rectangle(frame, (x_left_bottom, y_left_bottom - label_size[1]), (x_left_bottom + label_size[0], y_left_bottom + base_line), (255, 255, 255), cv2.FILLED)
            
            cv2.putText(frame, label, (x_left_bottom, y_left_bottom), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    t, _= net.getPerfProfile()                                                #returns time required to perform inference
    label = 'Inference time: %.2f ms' % (t*1000.0 / cv2.getTickFrequency())   #converting time to milliseconds
    cv2.putText(frame, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
    cv2.imshow(win_name, frame)                                               #displaying the output 
    cv2.destroyWindow(win_name)