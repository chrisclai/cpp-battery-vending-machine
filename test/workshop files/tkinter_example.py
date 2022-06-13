from random import Random
import tkinter as tk
import math

# TKINTER DEFAULT VARIABLES
HEIGHT = 1080
WIDTH = 480
REFRESH_RATE = 50
OFFSET= 25
VALUE_OFFSET = 60
UNIT_OFFSET = 60
LABEL_BEGIN_X = 190
LABEL_BEGIN_Y = 150

# GLOBAL VARIABLES
global currentKey
currentKey = ''

# INITIALIZATION
# Create the program window (root)
root = tk.Tk()
root.resizable(False, False)
main_canv = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='black', highlightthickness=0)
main_canv.pack()
main_canv.focus_set()

# CANVAS
control_canv = tk.Canvas(main_canv, width=360, height=900, highlightthickness=0, bg='black')   
control_canv.place(x=60, y=120, anchor='nw')

# KEYBOARD FUNCTIONS
def keyup(k):
    global currentKey
    print('up', k.char)
    currentKey = ''

def keydown(k):
    global currentKey
    if currentKey == k.char:
        pass
    else:
        print('down', k.char)
        currentKey = k.char
        sendCommand(currentKey)

def sendCommand(currentKey):
    if currentKey == 'w':
        print('UP')
    elif currentKey == 'a':
        print('LEFT')
    elif currentKey == 's':
        print('DOWN')
    elif currentKey == 'd':
        print('RIGHT')
    else:
        print("Not a valid key!")

# BIND
main_canv.bind("<KeyPress>", keydown)
main_canv.bind("<KeyRelease>", keyup)

# CLASS LABEL
class tkLabelUnit:
    def __init__(self, master=root, str='text', val=0.01, unit='m', list=0, offsetX=0):
        self.label = tk.Label(master, text=str, bg='black', fg='mint cream', font=('garamond',11,), justify='right')
        self.label.place(x=LABEL_BEGIN_X+offsetX, y=LABEL_BEGIN_Y+list*OFFSET, anchor='ne')

        self.value = tk.Label(master, text=val, bg='black', fg='mint cream', font=('garamond',11,), justify='right')
        self.value.place(x=LABEL_BEGIN_X+VALUE_OFFSET+offsetX,y=LABEL_BEGIN_Y+list*OFFSET, anchor='ne')

        self.unit = tk.Label(master, text=unit, bg='black', fg='mint cream', font=('garamond',11,),justify='left')
        self.unit.place(x=LABEL_BEGIN_X+UNIT_OFFSET+offsetX,y=LABEL_BEGIN_Y+list*OFFSET, anchor='nw')

# LABEL
title = tk.Label(main_canv, text="tkinter example", font=('courier new',24,'bold italic'), justify='center', bg='black', fg='#149dca')
title.place(relx=0.5,rely=0.075,anchor='center')

subtitle = tk.Label(main_canv, text="data array & user input", font=('courier new',20,'bold'), justify='center', bg='black', fg='#ca4114')
subtitle.place(relx=0.5,rely=0.11,anchor='center')

instructions = tk.Label(main_canv, text="Click on the GUI, then use the WASD keys\nto remotely control the robot. Sensor\ndata from the robot can be seen below.", font=('garamond',16,'italic'), justify='center', bg='black', fg='#FFFF81')
instructions.place(relx=0.5,rely=0.185,anchor='center')

# UNIT LABELS
IMU_System = tkLabelUnit(master=control_canv, str='System: ', val='Error', unit='', list=0)
IMU_Gyrometer = tkLabelUnit(master=control_canv, str='Gyrometer: ', val='Error', unit='', list=1)
IMU_Accelerometer = tkLabelUnit(master=control_canv, str='Accelerometer: ', val='Error', unit='', list=2)
IMU_Magnometer = tkLabelUnit(master=control_canv, str='Magnometer: ', val='Error', unit='', list=3)

empty1 = tkLabelUnit(master=control_canv, str='', val='', unit='', list=4)

IMU_Orientation_X = tkLabelUnit(master=control_canv, str='X Orientation: ', val='Error', unit='°', list=5)
IMU_Orientation_Y = tkLabelUnit(master=control_canv, str='Y Orientation: ', val='Error', unit='°', list=6)
IMU_Orientation_Z = tkLabelUnit(master=control_canv, str='Z Orientation: ', val='Error', unit='°', list=7)

empty2 = tkLabelUnit(master=control_canv, str='', val='', unit='', list=8)

IMU_Gyro_X = tkLabelUnit(master=control_canv, str='Gyroscope X:', val="Error", unit='rad/s', list=9)
IMU_Gyro_Y = tkLabelUnit(master=control_canv, str='Gyroscope Y:', val="Error", unit='rad/s', list=10)
IMU_Gyro_Z = tkLabelUnit(master=control_canv, str='Gyroscope Z:', val="Error", unit='rad/s', list=11)

empty3 = tkLabelUnit(master=control_canv, str='', val='', unit='', list=12)

IMU_AccelerometerAcc_X = tkLabelUnit(master=control_canv, str='Accelerometer Acc. X:', val="Error", unit='m/s^2', list=13)
IMU_AccelerometerAcc_Y = tkLabelUnit(master=control_canv, str='Accelerometer Acc. Y:', val="Error", unit='m/s^2', list=14)
IMU_AccelerometerAcc_Z = tkLabelUnit(master=control_canv, str='Accelerometer Acc. Z:', val="Error", unit='m/s^2', list=15)

empty4 = tkLabelUnit(master=control_canv, str='', val='', unit='', list=16)

IMU_Magnetic_Magnitude = tkLabelUnit(master=control_canv, str='Magnetic Magnitude: ', val="Error", unit='uT', list=17)
IMU_AccelerometerAcc_Magnitude = tkLabelUnit(master=control_canv, str='Acceleration Magnitude: ', val="Error", unit='m/s^2', list=18)

empty5 = tkLabelUnit(master=control_canv, str='', val='', unit='', list=19)

IMU_BoardTemperature = tkLabelUnit(master=control_canv, str='Board Temperature: ', val='Error', unit='°C', list=20)

empty6 = tkLabelUnit(master=control_canv, str='', val='', unit='', list=21)

Battery_Voltage = tkLabelUnit(master=control_canv, str='Battery Voltage:', val='Error', unit='V', list=22)
Battery_Current = tkLabelUnit(master=control_canv, str='Battery Current:', val='Error', unit='mA', list=23)
Battery_Capacity = tkLabelUnit(master=control_canv, str='Battery Capacity:', val='Error', unit='%', list=24)

# UPDATE FUNCTION
# Will recursively loop to update the data every 50ms
def updateData():
    # Change this database to extract data
    nums = [0] * 25

    # IMU Calibration
    IMU_System.value['text'] = nums[0]
    IMU_Gyrometer.value['text'] = nums[1]
    IMU_Accelerometer.value['text'] = nums[2]
    IMU_Magnometer.value['text'] = nums[3]

    # IMU Orientation
    IMU_Orientation_X.value['text'] = float(nums[4])
    IMU_Orientation_Y.value['text'] = float(nums[5])
    IMU_Orientation_Z.value['text'] = float(nums[6])

    # IMU Angular Velocity
    IMU_Gyro_X.value['text'] = float(nums[7])
    IMU_Gyro_Y.value['text'] = float(nums[8])
    IMU_Gyro_Z.value['text'] = float(nums[9])

    # IMU Acceleration
    IMU_AccelerometerAcc_X.value['text'] = float(nums[10])
    IMU_AccelerometerAcc_Y.value['text'] = float(nums[20])
    IMU_AccelerometerAcc_Z.value['text'] = float(nums[21])

    # Magnitude of Magnetic Fields and Acceleration
    IMU_Magnetic_Magnitude.value['text'] = round(math.sqrt((float(nums[13]) ** 2) + (float(nums[14]) ** 2) + (float(nums[15]) ** 2)), 3)
    IMU_AccelerometerAcc_Magnitude.value['text'] = round(math.sqrt((float(nums[19]) ** 2) + (float(nums[20]) ** 2) + (float(nums[21]) ** 2)), 3)

    # IMU Board Temperature
    IMU_BoardTemperature.value['text'] = float(nums[22])

    # Battery Detection
    Battery_Voltage.value['text'] = nums[24]
    Battery_Current.value['text'] = nums[23]
    Battery_Capacity.value['text'] = round(float(nums[24])/9.0 * 100, 2)

    root.after(REFRESH_RATE, updateData)

# UPDATE / REFRESH
# This is start calling the update function which is recursive.
# The recursion is essentially the update / represh.
root.after(REFRESH_RATE, updateData)

# CREATE THE ACTUAL WINDOW
root.mainloop()