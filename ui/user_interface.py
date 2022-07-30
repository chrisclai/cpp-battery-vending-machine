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


# CANVAS LABELS
battery_data_titles = tk.Label(battery_canv_left, 
                    text = "Battery ID" + "\n" + "\n" + "Capacity" + "\n" + "\n" + "Energy" + "\n" + "\n" + "Charge Capacity" + "\n" + "\n" + "Temperature" + "\n" + "\n" + "Battery Health Grade" + "\n" + "\n" + "Total Voltage"+ "\n" + "\n" + "Cell 1 Voltage" + "\n" + "\n" + "Cell 2 Voltage"+ "\n" + "\n" + "Cell 3 Voltage" + "\n" + "\n" + "Cell 4 Voltage",
                    font=('courier new', 12, BOLD), justify='left', bg='midnightblue', fg='red')
battery_data_titles.place(relx=0.42,rely=0.45,anchor='center')

#########################
b5_data = tk.Label(battery_canv_left, 
                   text = battery_id5[0] + "\n" + "\n" + battery_id5[1] + "\n" + "\n" + battery_id5[2] + "\n" + "\n" + battery_id5[3] + "\n" + "\n" + battery_id5[4] + "\n" + "\n" + battery_id5[5] + "\n" + "\n" + battery_id5[6] + "\n" + "\n" + battery_id5[7] + "\n" + "\n" + battery_id5[8] + "\n" + "\n" + battery_id5[9] + "\n" + "\n" + battery_id5[10],
                   font=('courier new', 12, BOLD), justify='center', bg='midnightblue', fg='red')
b5_data.place(relx=0.92,rely=0.45,anchor='center')
#########################

b4_data = tk.Label(battery_canv_left, 
                    text = battery_id4[0] + "\n" + "\n" + battery_id4[1] + "\n" + "\n" + battery_id4[2] + "\n" + "\n" + battery_id4[3] + "\n" + "\n" + battery_id4[4] + "\n" + "\n" + battery_id4[5] + "\n" + "\n" + battery_id4[6] + "\n" + "\n" + battery_id4[7] + "\n" + "\n" + battery_id4[8] + "\n" + "\n" + battery_id4[9] + "\n" + "\n" + battery_id4[10],
                    font=('courier new', 12, BOLD), justify='center', bg='midnightblue', fg='red')
b4_data.place(relx=0.92,rely=0.45,anchor='center')
#########################

b3_data = tk.Label(battery_canv_left, 
                    text = battery_id3[0] + "\n" + "\n" + battery_id3[1] + "\n" + "\n" + battery_id3[2] + "\n" + "\n" + battery_id3[3] + "\n" + "\n" + battery_id3[4] + "\n" + "\n" + battery_id3[5] + "\n" + "\n" + battery_id3[6] + "\n" + "\n" + battery_id3[7] + "\n" + "\n" + battery_id3[8] + "\n" + "\n" + battery_id3[9] + "\n" + "\n" + battery_id3[10],
                    font=('courier new', 12, BOLD), justify='center', bg='midnightblue', fg='red')
b3_data.place(relx=0.92,rely=0.45,anchor='center')


#########################
b2_data = tk.Label(battery_canv_left, 
                    text = battery_id2[0] + "\n" + "\n" + battery_id2[1] + "\n" + "\n" + battery_id2[2] + "\n" + "\n" + battery_id2[3] + "\n" + "\n" + battery_id2[4] + "\n" + "\n" + battery_id2[5] + "\n" + "\n" + battery_id2[6] + "\n" + "\n" + battery_id2[7] + "\n" + "\n" + battery_id2[8] + "\n" + "\n" + battery_id2[9] + "\n" + "\n" + battery_id2[10],
                    font=('courier new', 12, BOLD), justify='center', bg='midnightblue', fg='red')
b2_data.place(relx=0.92,rely=0.45,anchor='center')

#########################
b1_data = tk.Label(battery_canv_left, 
                    text = battery_id1[0] + "\n" + "\n" + battery_id1[1] + "\n" + "\n" + battery_id1[2] + "\n" + "\n" + battery_id1[3] + "\n" + "\n" + battery_id1[4] + "\n" + "\n" + battery_id1[5] + "\n" + "\n" + battery_id1[6] + "\n" + "\n" + battery_id1[7] + "\n" + "\n" + battery_id1[8] + "\n" + "\n" + battery_id1[9] + "\n" + "\n" + battery_id1[10],
                    font=('courier new', 12, BOLD), justify='center', bg='midnightblue', fg='red')
b1_data.place(relx=0.92,rely=0.45,anchor='center')

#########################

total_BMS_titles = tk.Label(total_canv_right, 
                    text = "Capacity" + "\n" + "\n" + "Energy" + "\n" + "\n" + "Charge Capacity" + "\n" + "\n" + "Average Temp." + "\n" + "\n" + "Total Voltage"+ "\n" + "\n" + "Cell 1 Voltage" + "\n" + "\n" + "Cell 2 Voltage"+ "\n" + "\n" + "Cell 3 Voltage" + "\n" + "\n" + "Cell 4 Voltage",
                    font=('courier new', 12, BOLD), justify='left', bg='midnightblue', fg='orange')
total_BMS_titles.place(relx= 0.35,rely=0.37,anchor='center')

# TOTAL BMS DATA CALCULATIONS
t_capacity_list = [float(battery_id1[1]), float(battery_id2[1]), float(battery_id3[1]), float(battery_id4[1]), float(battery_id5[1])]
t_energy_list = [float(battery_id1[2]), float(battery_id2[2]), float(battery_id3[2]), float(battery_id4[2]), float(battery_id5[2])]
t_charge_capacity_list = [float(battery_id1[3]), float(battery_id2[3]), float(battery_id3[3]), float(battery_id4[3]), float(battery_id5[3])]
t_avg_temp_list = [float(battery_id1[4]), float(battery_id2[4]), float(battery_id3[4]), float(battery_id4[4]), float(battery_id5[4])]
t_voltage_list = [float(battery_id1[6]), float(battery_id2[6]), float(battery_id3[6]), float(battery_id4[6]), float(battery_id5[6])]
t_cell_1_voltage_list = [float(battery_id1[7]), float(battery_id2[7]), float(battery_id3[7]), float(battery_id4[7]), float(battery_id5[7])]
t_cell_2_voltage_list = [float(battery_id1[8]), float(battery_id2[8]), float(battery_id3[8]), float(battery_id4[8]), float(battery_id5[8])]
t_cell_3_voltage_list = [float(battery_id1[9]), float(battery_id2[9]), float(battery_id3[9]), float(battery_id4[9]), float(battery_id5[9])]
t_cell_4_voltage_list = [float(battery_id1[10]), float(battery_id2[10]), float(battery_id3[10]), float(battery_id4[10]), float(battery_id5[10])]

battery_totals = tk.Label(total_canv_right,
                text = sum(t_capacity_list)
                    + "\n" + sum(t_energy_list)
                    + "\n" + sum(t_charge_capacity_list)
                    + "\n" + sum(t_avg_temp_list)/len(t_avg_temp_list)
                    + "\n" + sum(t_voltage_list)
                    + "\n" + sum(t_cell_1_voltage_list)
                    + "\n" + sum(t_cell_2_voltage_list)
                    + "\n" + sum(t_cell_3_voltage_list)
                    + "\n" + sum(t_cell_4_voltage_list)
                    , font=('courier new', 12, BOLD), justify='center', bg='midnightblue', fg='red')
battery_totals.place(relx=0.85,rely=0.078,anchor='center')


# PLACEHOLDER TEXT FOR CAMERA DISPLAY 
camera_title = tk.Label(main_canv, text="Placeholder for camera display", font=('courier new',10), justify='center', bg='midnightblue', fg='white')
camera_title.place(relx=0.50,rely=0.45,anchor='center')


# TOGGLE ARROW FUNCTION

# THIS IS AN ATTEMPT TO MAKE THE ARROWS WORK
clickCounter = 0
def toggle_right():
    clickCounter = clickCounter + 1
    if clickCounter == 1:
       b1_data = tk.Label(battery_canv_left, 
                    text = battery_id1[0] + "\n" + "\n" + battery_id1[1] + "\n" + "\n" + battery_id1[2] + "\n" + "\n" + battery_id1[3] + "\n" + "\n" + battery_id1[4] + "\n" + "\n" + battery_id1[5] + "\n" + "\n" + battery_id1[6] + "\n" + "\n" + battery_id1[7] + "\n" + "\n" + battery_id1[8] + "\n" + "\n" + battery_id1[9] + "\n" + "\n" + battery_id1[10],
                    font=('courier new', 12, BOLD), justify='center', bg='midnightblue', fg='red')
       b1_data.place(relx=0.92,rely=0.45,anchor='center') 
    elif clickCounter == 2:
        b2_data = tk.Label(battery_canv_left, 
                    text = battery_id2[0] + "\n" + "\n" + battery_id2[1] + "\n" + "\n" + battery_id2[2] + "\n" + "\n" + battery_id2[3] + "\n" + "\n" + battery_id2[4] + "\n" + "\n" + battery_id2[5] + "\n" + "\n" + battery_id2[6] + "\n" + "\n" + battery_id2[7] + "\n" + "\n" + battery_id2[8] + "\n" + "\n" + battery_id2[9] + "\n" + "\n" + battery_id2[10],
                    font=('courier new', 12, BOLD), justify='center', bg='midnightblue', fg='red')
        b2_data.place(relx=0.92,rely=0.45,anchor='center')
    elif clickCounter == 3:
        b3_data = tk.Label(battery_canv_left, 
                    text = battery_id3[0] + "\n" + "\n" + battery_id3[1] + "\n" + "\n" + battery_id3[2] + "\n" + "\n" + battery_id3[3] + "\n" + "\n" + battery_id3[4] + "\n" + "\n" + battery_id3[5] + "\n" + "\n" + battery_id3[6] + "\n" + "\n" + battery_id3[7] + "\n" + "\n" + battery_id3[8] + "\n" + "\n" + battery_id3[9] + "\n" + "\n" + battery_id3[10],
                    font=('courier new', 12, BOLD), justify='center', bg='midnightblue', fg='red')
        b3_data.place(relx=0.92,rely=0.45,anchor='center')
    elif clickCounter == 4:
        b4_data = tk.Label(battery_canv_left, 
                    text = battery_id4[0] + "\n" + "\n" + battery_id4[1] + "\n" + "\n" + battery_id4[2] + "\n" + "\n" + battery_id4[3] + "\n" + "\n" + battery_id4[4] + "\n" + "\n" + battery_id4[5] + "\n" + "\n" + battery_id4[6] + "\n" + "\n" + battery_id4[7] + "\n" + "\n" + battery_id4[8] + "\n" + "\n" + battery_id4[9] + "\n" + "\n" + battery_id4[10],
                    font=('courier new', 12, BOLD), justify='center', bg='midnightblue', fg='red')
        b4_data.place(relx=0.92,rely=0.45,anchor='center')
    elif clickCounter == 5:
        b5_data = tk.Label(battery_canv_left, 
                   text = battery_id5[0] + "\n" + "\n" + battery_id5[1] + "\n" + "\n" + battery_id5[2] + "\n" + "\n" + battery_id5[3] + "\n" + "\n" + battery_id5[4] + "\n" + "\n" + battery_id5[5] + "\n" + "\n" + battery_id5[6] + "\n" + "\n" + battery_id5[7] + "\n" + "\n" + battery_id5[8] + "\n" + "\n" + battery_id5[9] + "\n" + "\n" + battery_id5[10],
                   font=('courier new', 12, BOLD), justify='center', bg='midnightblue', fg='red')
        b5_data.place(relx=0.92,rely=0.45,anchor='center')
        clickCounter == 0


# BUTTONS
button_accept = tk.Button(main_canv, width = 17, height = 2, highlightthickness=0, bg='royalblue', text = "ACCEPT", font = ('courier new', 10), fg = 'white', activeforeground = "red",activebackground = "light grey", pady=10)
button_accept.place(relx=0.4,rely=0.78,anchor='center')

button_retrieve = tk.Button(main_canv, width = 17, height = 2, highlightthickness=0, bg='royalblue', text = "RETRIEVE", font = ('courier new', 10), fg = 'white', activeforeground = "red",activebackground = "light grey", pady=10)
button_retrieve.place(relx=0.603,rely=0.78,anchor='center')

button_exit = tk.Button(main_canv, command= root.destroy, width = 17, height = 2, highlightthickness=0, bg='royalblue', text = "EXIT", font = ('courier new', 10), fg = 'white', activeforeground = "red",activebackground = "light grey", pady=10)
button_exit.place(relx=0.503,rely=0.9,anchor='center')

while 1:
    button_right = tk.Button(battery_canv_left, command = toggle_right(), width = 5, height = 1, highlightthickness=0, bg='royalblue', text = "-->",  fg = 'white', activeforeground = "red",activebackground = "light grey", pady=10)
    button_right.place(relx=0.9,rely= 0.94,anchor='center')

    # Placeholder command for button_left
    button_left = tk.Button(battery_canv_left, command= root.destroy, width = 5, height = 1, highlightthickness=0, bg='royalblue', text = "<--",  fg = 'white', activeforeground = "red",activebackground = "light grey", pady=10)
    button_left.place(relx=0.09,rely= 0.94,anchor='center')


# SHOW ACTUAL WINDOW
root.mainloop()
