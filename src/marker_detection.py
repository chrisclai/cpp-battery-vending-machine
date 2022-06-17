import cv2 as cv
from cv2 import aruco
import numpy as np
import pandas as pd
import json


with open ('data.json') as json_file:
    data = json.load(json_file)
df = pd.json_normalize(data,record_path=['Battery Data'])

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
            topLeft, topRight, bottomRight, bottomLeft = corners
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            if ids == 1:
                cv.putText(frame, f"ID: {ids[0]}", (topRight[0], topLeft[1] - 100), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),1, cv.LINE_AA)
                cv.putText(frame, f"Capacity: {data['Battery Data'][0]['Capacity']}", (topRight[0], topLeft[1] - 80), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
                cv.putText(frame, f"Energy: {data['Battery Data'][0]['Energy']}", (topRight[0], topLeft[1] - 60), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
                cv.putText(frame, f"Charge Capacity: {data['Battery Data'][0]['Charge Capacity']}", (topRight[0], topLeft[1] - 40), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
                cv.putText(frame, f"Temperature: {data['Battery Data'][0]['Temperature']}", (topRight[0], topLeft[1] - 20), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
                cv.putText(frame, f"BMS Health: {data['Battery Data'][0]['BMS Health']}", (topRight[0], topLeft[1] - (-5)), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
                cv.putText(frame, f"Total Voltage: {data['Battery Data'][0]['Total Voltage']}", (topRight[0], topLeft[1] - (-20)), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
            if ids == 2:
                cv.putText(frame, f"ID: {ids[0]}", (topRight[0], topLeft[1] - 100), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),1, cv.LINE_AA)
                cv.putText(frame, f"Capacity: {data['Battery Data'][1]['Capacity']}", (topRight[0], topLeft[1] - 80), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
                cv.putText(frame, f"Energy: {data['Battery Data'][1]['Energy']}", (topRight[0], topLeft[1] - 60), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
                cv.putText(frame, f"Charge Capacity: {data['Battery Data'][1]['Charge Capacity']}", (topRight[0], topLeft[1] - 40), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
                cv.putText(frame, f"Temperature: {data['Battery Data'][1]['Temperature']}", (topRight[0], topLeft[1] - 20), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
                cv.putText(frame, f"BMS Health: {data['Battery Data'][1]['BMS Health']}", (topRight[0], topLeft[1] - (-5)), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
                cv.putText(frame, f"Total Voltage: {data['Battery Data'][1]['Total Voltage']}", (topRight[0], topLeft[1] - (-20)), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
            '''if ids == 3:
                cv.putText(frame, f"ID: {ids[0]}", (topRight[0], topLeft[1] - 100), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),1, cv.LINE_AA)
                cv.putText(frame, f"Capacity(%): {df.iloc[2, df.columns.get_loc('Capacity (%)')]}", (topRight[0], topLeft[1] - 80), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
                cv.putText(frame, f"Energy(Wh): {df.iloc[2, df.columns.get_loc('Energy (Wh)')]}", (topRight[0], topLeft[1] - 60), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
                cv.putText(frame, f"Charge Capacity(%): {df.iloc[2, df.columns.get_loc('Charge Capacity (mAh)')]}", (topRight[0], topLeft[1] - 40), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
                cv.putText(frame, f"Temperature: {df.iloc[2, df.columns.get_loc('Temperature (C)')]}", (topRight[0], topLeft[1] - 20), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
                cv.putText(frame, f"BMS Health: {df.iloc[2, df.columns.get_loc('BMS Health (%)')]}", (topRight[0], topLeft[1] - (-5)), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)
                cv.putText(frame, f"Total Voltage: {df.iloc[2, df.columns.get_loc('Total Voltage (V)')]}", (topRight[0], topLeft[1] - (-20)), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2, cv.LINE_AA)'''
            
# Camera Feed open
    cv.imshow("Camera", frame)
    key = cv.waitKey(1)
    if key == ord('q'):
        break

camera.release()
cv.destroyAllWindows()





