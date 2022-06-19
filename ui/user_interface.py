from random import Random
import tkinter as tk


# TKINTER DEFAULT VARIABLES
HEIGHT = 650
WIDTH = 900
REFRESH_RATE = 50
OFFSET= 25
VALUE_OFFSET = 60
UNIT_OFFSET = 60
LABEL_BEGIN_X = 190
LABEL_BEGIN_Y = 150

# INITIALIZATION
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
battery_canv_left = tk.Canvas(main_canv, width=275, height=490, highlightthickness=0, bg='royalblue4')   
battery_canv_left.place(x=10, y=150, anchor='nw')

total_canv_right = tk.Canvas(main_canv, width=275, height=490, highlightthickness=0, bg='royalblue4')   
total_canv_right.place(x=615, y=150, anchor='nw')

camera_canv = tk.Canvas(main_canv, width=323, height=300, highlightthickness=0, bg='royalblue4')   
camera_canv.place(x=288, y=150, anchor='nw')

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

# SHOW ACTUAL WINDOW
root.mainloop()