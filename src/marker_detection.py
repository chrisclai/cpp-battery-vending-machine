import cv2 as cv
from cv2 import aruco
import numpy as np

# Setting the dictionary for us to read a 4x4 aruco code
marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_1000)

# Setting parameters to create marker
param_markers = aruco.DetectorParameters_create()

# Identifying the camera
camera = cv.VideoCapture(0, cv.CAP_DSHOW)

# Camera Detection of aruco codes!
while True:
    ret, frame = camera.read()
    if not ret:
        break
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    marker_corners, markers_IDs, reject = aruco.detectMarkers(gray_frame, marker_dict, parameters = param_markers)
    print(markers_IDs)
    
    # Marker outline drawing
    if marker_corners:
        for ids, corners in zip(markers_IDs, marker_corners):   
            cv.polylines(frame, [corners.astype(np.int32)], True, (0,255,255), 4, cv.LINE_AA)
            corners = corners.reshape(4,2)
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            cv.putText(frame, f"id: {ids[0]}", top_right, cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
            

# Camera Feed open
    cv.imshow("Camera", frame)
    key = cv.waitKey(1)
    if key == ord('q'):
        break

camera.release()
cv.destroyAllWindows()





