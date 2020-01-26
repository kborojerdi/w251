"""This is for capturing video

Calling method: python video_capture.py
"""

import numpy as np
import cv2
import paho.mqtt.publish as publish
import binascii

#load the XML classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture(1)

# Check if camera opened successfully
if (cap.isOpened()== False): 
    print("Error opening video stream or file")

# Read until video is completed
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # We don't use the color information, so might as well save space
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # face detection and other logic goes here
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        face = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
	# your logic goes here; for instance
	# cut out face from the frame.. 
        cv2.imshow('face', face)
	rc,png = cv2.imencode('.png', face)
	msg = png.tobytes()
        publish.single("test", payload=msg, qos=0, retain=False, hostname="169.62.93.58")
        # print(binascii.hexlify(msg))
        print(len(msg))

        # msg_back = np.frombuffer(msg, dtype=np.uint8)
        # image = cv2.imdecode(msg_back, flags=0)

        # cv2.imshow('image',image)
        # cv2.imwrite("/data/w251/HW3/face.png", image)

    if ret == True:

        # Display the resulting frame
        cv2.imshow('Frame',frame)

        # Press Q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release the capture
cap.release()

# Close all the frames
cv2.destroyAllWindows()
