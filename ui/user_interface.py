import tkinter as tk
import json
from tkinter.font import BOLD

# TKINTER DEFAULT VARIABLES
HEIGHT = 650
WIDTH = 906
REFRESH_RATE = 50
OFFSET= 25
VALUE_OFFSET = 60
UNIT_OFFSET = 60
LABEL_BEGIN_X = 190
LABEL_BEGIN_Y = 150

# BATTERY DATA IMPORTATION
# Opening JSON file
with open('BatteryDataDump.json', 'r') as openfile:

        # Reading from json file
        json_object = json.load(openfile)

        battery_data = [0] * 55  # this array will store the data from the JSON file

        loopCounter = 0

        # The for loop will extract data from the JSON file "BatteryDataDump" and will store the data into the array "battery_data"
        for i in json_object['Battery Data']:
            battery_data[0 + loopCounter] = i['ID']  # this will extract the data from the "Battery Data" section
            battery_data[1 + loopCounter] = i['Capacity']  # this will extract the data from the "Capacity" section
            battery_data[2 + loopCounter] = i['Energy']  # this will extract the data from the "Energy" section
            battery_data[3 + loopCounter] = i['Charge Capacity']  # this will extract the data from the "Charge Capacity" section
            battery_data[4 + loopCounter] = i['Temperature']  # this will extract the data from the "Temperature" section
            battery_data[5 + loopCounter] = i['BMS Health']  # this will extract the data from the "BMS Health" section
            battery_data[6 + loopCounter] = i['Total Voltage']  # this will extract the data from the "Total Voltage" section
            battery_data[7 + loopCounter] = i['Cell 1 Voltage']  # this will extract the data from the "Cell 1 Voltage" section
            battery_data[8 + loopCounter] = i['Cell 2 Voltage']  # this will extract the data from the "Cell 2 Voltage" section
            battery_data[9 + loopCounter] = i['Cell 3 Voltage']  # this will extract the data from the "Cell 3 Voltage" section
            battery_data[10 + loopCounter] = i['Cell 4 Voltage']  # this will extract the data from the "Cell 4 Voltage" section

            # incrementing the loop counter to access the other data
            loopCounter += 11

        # Splitting the data from "battery_data" into 0-10 and 11-21 to be stored in "battery_id1", "battery_id2", etc.
        size = 11
        battery_id1 = [0] * size
        battery_id2 = [0] * size
        battery_id3 = [0] * size
        battery_id4 = [0] * size
        battery_id5 = [0] * size

        for i in range(55):
            if i <= 10:
                battery_id1[i] = battery_data[i]  # storing elements 0-10 of "array_Element" in "battery_id1"
            elif 11 <= i <= 21:
                battery_id2[i - 11] = battery_data[i]  # storing elements 11-21 of "array_Element" in "battery_id2"
            elif 22 <= i <= 32:
                battery_id3[i - 22] = battery_data[i]  # storing elements 22-32 of "array_Element" in "battery_id3"
            elif 33 <= i <= 43:
                battery_id4[i - 33] = battery_data[i]  # storing elements 33-43 of "array_Element" in "battery_id4"
            elif 44 <= i <= 54:
                battery_id5[i - 44] = battery_data[i]  # storing elements 44-54 of "array_Element" in "battery_id5"

# GUI INITIALIZATION
# Create the program window (root)
root = tk.Tk()
root.resizable(False, False)
main_canv = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='midnightblue', highlightthickness=0)
main_canv.pack()
main_canv.focus_set()

# LABEL
title = tk.Label(main_canv, text="CPP Battery Vending Machine", font=('verdana',25,'bold'), justify='center', bg='midnightblue', fg='#149dca')
title.place(relx=0.5,rely=0.05,anchor='center')

subtitle = tk.Label(main_canv, text="ROBOTIS Collaboration Project 2022", font=('courier new',15), justify='center', bg='midnightblue', fg='seashell3')
subtitle.place(relx=0.5,rely=0.11,anchor='center')

instructions = tk.Label(main_canv, text="Use the buttons to remotely control the robot. Sensor data from the BMS can be seen below.", font=('garamond',13), justify='center', bg='midnightblue', fg='springgreen')
instructions.place(relx=0.5,rely=0.15,anchor='center')

battery_title = tk.Label(main_canv, text="Battery Data", font=('courier new',15), justify='center', bg='midnightblue', fg='white')
battery_title.place(relx=0.155,rely=0.2,anchor='center')

total_title = tk.Label(main_canv, text="Total BMS Data", font=('courier new',15), justify='center', bg='midnightblue', fg='white')
total_title.place(relx=0.84,rely=0.2,anchor='center')

# CANVAS
battery_canv_left = tk.Canvas(main_canv, width=255, height=490, highlightthickness=0, bg='royalblue4')   
battery_canv_left.place(x=15, y=150, anchor='nw')

total_canv_right = tk.Canvas(main_canv, width=255, height=490, highlightthickness=0, bg='royalblue4')   
total_canv_right.place(x=635, y=150, anchor='nw')

camera_canv = tk.Canvas(main_canv, width=333, height=300, highlightthickness=0, bg='royalblue4')   
camera_canv.place(x=287, y=150, anchor='nw')

# PLACEHOLDER TEXT FOR CAMERA DISPLAY 
camera_title = tk.Label(main_canv, text="Placeholder for camera display", font=('courier new',10), justify='center', bg='midnightblue', fg='white')
camera_title.place(relx=0.50,rely=0.45,anchor='center')

# BUTTONS
button_accept = tk.Button(main_canv, width = 17, height = 2, highlightthickness=0, bg='royalblue', text = "ACCEPT", font = ('courier new', 10), fg = 'white', activeforeground = "red",activebackground = "light grey", pady=10)
button_accept.place(relx=0.4,rely=0.78,anchor='center')

button_retrieve = tk.Button(main_canv, width = 17, height = 2, highlightthickness=0, bg='royalblue', text = "RETRIEVE", font = ('courier new', 10), fg = 'white', activeforeground = "red",activebackground = "light grey", pady=10)
button_retrieve.place(relx=0.603,rely=0.78,anchor='center')

button_exit = tk.Button(main_canv, command= root.destroy, width = 17, height = 2, highlightthickness=0, bg='royalblue', text = "EXIT", font = ('courier new', 10), fg = 'white', activeforeground = "red",activebackground = "light grey", pady=10)
button_exit.place(relx=0.503,rely=0.9,anchor='center')

button_right = tk.Button(battery_canv_left, command= root.destroy, width = 5, height = 1, highlightthickness=0, bg='royalblue', text = "-->",  fg = 'white', activeforeground = "red",activebackground = "light grey", pady=10)
button_right.place(relx=0.9,rely= 0.94,anchor='center')

button_left = tk.Button(battery_canv_left, command= root.destroy, width = 5, height = 1, highlightthickness=0, bg='royalblue', text = "<--",  fg = 'white', activeforeground = "red",activebackground = "light grey", pady=10)
button_left.place(relx=0.09,rely= 0.94,anchor='center')

# CANVAS LABELS
b1_data = tk.Label(battery_canv_left, 
                    text = battery_id1[0] + "\n" + "\n" + battery_id1[1] + "\n" + "\n" + battery_id1[2] + "\n" + "\n" + battery_id1[3] + "\n" + "\n" + battery_id1[4] + "\n" + "\n" + battery_id1[5] + "\n" + "\n" + battery_id1[6] + "\n" + "\n" + battery_id1[7] + "\n" + "\n" + battery_id1[8] + "\n" + "\n" + battery_id1[9] + "\n" + "\n" + battery_id1[10],
                    font=('courier new', 12, BOLD), justify='center', bg='midnightblue', fg='red')
b1_data.place(relx=0.92,rely=0.45,anchor='center')

b1_data_title = tk.Label(battery_canv_left, 
                    text = "Battery ID" + "\n" + "\n" + "Capacity" + "\n" + "\n" + "Energy" + "\n" + "\n" + "Charge Capacity" + "\n" + "\n" + "Temperature" + "\n" + "\n" + "Battery Health Grade" + "\n" + "\n" + "Total Voltage"+ "\n" + "\n" + "Cell 1 Voltage" + "\n" + "\n" + "Cell 2 Voltage"+ "\n" + "\n" + "Cell 3 Voltage" + "\n" + "\n" + "Cell 4 Voltage",
                    font=('courier new', 12, BOLD), justify='left', bg='midnightblue', fg='red')
b1_data_title.place(relx=0.42,rely=0.45,anchor='center')

# SHOW ACTUAL WINDOW
root.mainloop()