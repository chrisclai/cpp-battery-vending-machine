import numpy as np
import cv2
import imutils
import time

# Define webcam used
webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Check for compatibility. If not, force search webcam
ret, frame = webcam.read()
print(frame)
try:
    if frame == None:
        webcam = cv2.VideoCapture(-1)
except:
    print("Task Failed Successfully. Move on.")

# Import face-recgonition software
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

while(True):
    start = time.time()
    # Grabbing frame from webcam
    ret, frame = webcam.read()

    # Frame width and height + fps
    width = int(webcam.get(3))
    height = int(webcam.get(4))

    cv2.putText(frame, "Frame Max (x,y): ({},{})".format(width, height), (width - 230, 465), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Defining box dimensions
    centerx = 0.0
    centery = 0.0
    object_detect = ""

    # Create a box around the face, if detected
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        frame = cv2.rectangle(frame, (x,y), (x + w, y + h), (0, 255, 0), 3)
        centerx = x + 0.5 * float(w)
        centery = y + 0.5 * float(h)

    # Text to display dimensions
    cv2.putText(frame, "x: {}, y: {}".format(centerx, centery), (width - 230, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Text to display object type
    if not centerx and not centery:
        object_detect = "None"
    else:
        object_detect = "Face"
    
    cv2.putText(frame, "Object: {}".format(object_detect), (width - 230, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    stop = time.time()

    seconds = stop - start

    # Calculate frames per second
    fps = 1 / seconds

    # fps display
    cv2.putText(frame,"FPS: " + str(round(fps,2)), (50,50) ,cv2.FONT_HERSHEY_SIMPLEX, 0.75,(50,150,50),2)

    # Show frame in seperate box
    cv2.imshow('video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Safely close all windows
webcam.release()
cv2.destroyAllWindows()