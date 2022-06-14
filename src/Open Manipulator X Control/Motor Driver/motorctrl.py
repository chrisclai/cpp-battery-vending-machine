#ALL IMPORTS
from dynamixel_sdk import *  # Uses Dynamixel SDK library
import os

if os.name == 'nt':
    import msvcrt

    def getch():
        return msvcrt.getch().decode()
else:
    import sys
    import tty
    import termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


#******MOTOR DRIVE FUNCTIONS*******
#this is where we will put hardware team functions

#Initializes and enables all the motors
#Input is portname, baudrate, and Dynamixel motor IDs
#Portname is the serial port assigned to the U2D2. Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
#To check portname, please refer to either the Dynamixel Wizard or "Serial Ports" in Device Manager
#Baudrate is the rate of information transfer via serial ports. Linux is 57600 and Windows is 1000000
#Dynamixel motor IDs can be found by using the Dynamixel Wizard.
#There is no output from this function
def portInitialization(portname, baudrate, baseID, bicepID, forearmID, wristID, clawID):
    global DEVICENAME
    DEVICENAME = portname  # All the motors share the same port when connected in series
    global PROTOCOL_VERSION #Dynamixel SDK has two operating modes: Protocol 1 or 2. This code uses 2
    PROTOCOL_VERSION = 2 # Initialize PortHandler instance and PacketHandler instance
    global portHandler
    portHandler = PortHandler(DEVICENAME)
    global packetHandler
    packetHandler = PacketHandler(PROTOCOL_VERSION)
    device_index = 0

    #List of all the addresses from the Control Table that is used for operation
    global ADDR_PRESENT_POSITION
    ADDR_PRESENT_POSITION = 132 #Address of the positions of the motors
    global ADDR_PROFILE_VELOCITY
    ADDR_PROFILE_VELOCITY = 112 #Address of the velocity of the motors
    global ADDR_GOAL_POSITION
    ADDR_GOAL_POSITION = 116 #Address of goal position
    global ADDR_MOVING
    ADDR_MOVING = 122 #Address of value that states if motor is moving or not
    global ADDR_MOVING_STATUS
    ADDR_MOVING_STATUS = 123
    global DXL_MOVING_STATUS_THRESHOLD
    DXL_MOVING_STATUS_THRESHOLD = 10    # Dynamixel moving status threshold
    global LEN_GOAL_POSITION
    LEN_GOAL_POSITION = 4 #Byte Length of goal position
    global LEN_PRESENT_POSITION
    LEN_PRESENT_POSITION = 4 #Byte length of present position

    if portHandler.openPort(): #Enables communication between computer and motors
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        getch()
        quit()

    global BAUDRATE
    BAUDRATE = baudrate
    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE): #Sets rate of information transfer
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        getch()
        quit()

    global ADDR_TORQUE_ENABLE # Set memory address for Torque Enable
    ADDR_TORQUE_ENABLE = 64
    TORQUE_ENABLE = 1

    global DXL_ID # Set the motor ID for each dynamixel. ID 0,1,2 is base/bicep/forearm motors
    DXL_ID = [baseID, bicepID, forearmID, wristID, clawID]
    global motorNum
    motorNum = len(DXL_ID)

    for motorID in DXL_ID: # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
            portHandler, motorID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel", motorID,
                  "has been successfully connected")
    

def dxlPresAngle():
    dxl_present_position = [0] * motorNum
    dxl_present_angle = [0] * motorNum

    for motorIndex in range(motorNum): #Reads the current position of the motor
        dxl_present_position[motorIndex] = ReadMotorData(motorIndex, ADDR_PRESENT_POSITION)
    print("Positions are ", dxl_present_position)

    for motorIndex in range(motorNum): #Converts the position into angles
        dxl_present_angle[motorIndex] = _map(dxl_present_position[motorIndex], 0, 4095, 0, 360)
    print("Angles are ", dxl_present_angle)

    return (dxl_present_angle)


def dxlSetVelo(vel_array):
    for motorIndex in range(motorNum):
        WriteMotorData(motorIndex, ADDR_PROFILE_VELOCITY, vel_array[motorIndex])
    dxlGetVelo()


def dxlGetVelo():
    dxl_present_velocity = [0] * motorNum

    for motorIndex in range(motorNum):
        dxl_present_velocity[motorIndex] = ReadMotorData(motorIndex, ADDR_PROFILE_VELOCITY)
    print("Velocities are ", dxl_present_velocity)
    return (dxl_present_velocity)


def motorRunWithInputs(angle_inputs):

    #Format is [base, bicep, forearm, wrist, claw]
    dxl_goal_angle = angle_inputs
    dxl_goal_inputs = [0] * motorNum
    dxl_end_position = [0] * motorNum
    dxl_end_angle = [0] * motorNum
    movementStatus = [0] * motorNum

    # ------------------Start to execute motor rotation------------------------
    while 1:
        #Convert angle inputs into step units for movement
        for motorIndex in range(motorNum): 
            dxl_goal_inputs[motorIndex] = _map(
                dxl_goal_angle[motorIndex], 0, 360, 0, 4095)
        print("Goal angles are ", dxl_goal_angle)

        #Write goal position for all motors (base, bicep, forearm, wrist, claw)
        for motorIndex in range(motorNum):
            WriteMotorData(motorIndex, ADDR_GOAL_POSITION, dxl_goal_inputs[motorIndex])

            #Read position for each motor and set status of motor
            dxl_end_position[motorIndex], movementStatus[motorIndex] = motor_check(motorIndex, dxl_goal_inputs[motorIndex]) #Read position for the motor
            dxl_end_angle[motorIndex] = _map(dxl_end_position[motorIndex], 0, 4095, 0, 360)
        #print("Angle for Dynamixel:%03d is %03d" % (DXL_ID[device_index], dxl_end_angle[device_index]))

        for motorIndex in range(motorNum):
            print("Angle for Dynamixels %03d after execution is %03d ----------------------------" % (DXL_ID[motorIndex], dxl_end_angle[motorIndex]))
        # ------------------------------------------------------------------------------------------------------------------------------------------------------

        #Motor movement completes and motor movement status to be sent out
        # ------------------------------------------------------------------------------------------------------------------------------------------------------
        return movementStatus

#The functions take in an array of X angle inputs and an array of X dynamixel IDs. Running the functions will drive the X dynamixels to the desired angle inputs simultaneously
def Sim2MotorsRun(angle_inputs, dxlIDs):
    #Intializate simultaneous motor movement
    global motor_sync_write
    motor_sync_write = GroupSyncWrite(portHandler, packetHandler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
    global motor_sync_read
    motor_sync_read = GroupSyncRead(portHandler, packetHandler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
    #print("Motor_Sync_Write is ", motor_sync_write)
    #print("Motor_Sync_Read is ", motor_sync_read)
    dxl_goal_angle = angle_inputs
    dxl_goal_inputs = [0] * len(angle_inputs)
    param_goal_position = [0] * len(angle_inputs)

    #Convert angle inputs into step units for movement
    for motorIndex in range(len(angle_inputs)): 
        dxl_goal_inputs[motorIndex] = _map(dxl_goal_angle[motorIndex], 0, 360, 0, 4095)
        print("Goal angles are ", dxl_goal_angle)

    #Create parameter storage for present positions
    for motorID in dxlIDs:  #Create parameter storage for bicep and forearm motors' present position value
        dxl_addparam_result = motor_sync_read.addParam(motorID)
        if dxl_addparam_result != True:
            print("[ID:%03d] groupSyncRead addparam failed" % motorID)
        #print("DXL_ADDPARAM_RESULT is " ,dxl_addparam_result)

    #Allocate goal position values into 4-byte array for bicep and forearm motors. Dynamixel motors use either 2-bytes or 4-bytes
    for motorIndex in range(len(angle_inputs)): 
        param_goal_position[motorIndex] = [DXL_LOBYTE(DXL_LOWORD(dxl_goal_inputs[motorIndex])), DXL_HIBYTE(DXL_LOWORD(dxl_goal_inputs[motorIndex])),DXL_LOBYTE(DXL_HIWORD(dxl_goal_inputs[motorIndex])), DXL_HIBYTE(DXL_HIWORD(dxl_goal_inputs[motorIndex]))]
    #print("param_goal_bicep_position is ", param_goal_position[1])
    #print("param_goal_bicep_position is ", param_goal_position[2])
        #Add goal position input values of bicep and forearm motors to Syncwrite parameter storage
        dxl_addparam_result = motor_sync_write.addParam(dxlIDs[motorIndex], param_goal_position[motorIndex])
        if dxl_addparam_result != True:
            print("[ID:%03d] groupSyncWrite addparam failed" % dxlIDs[motorIndex])
        #print("groupSyncWrite for [ID:%03d] works" % (DXL_ID[device_index]))
   
    #Syncwrite goal position to bicep and forearm motors
    dxl_comm_result = motor_sync_write.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

    #Clear syncwrite parameter storage
    motor_sync_write.clearParam()

def Sim2MotorsRead(dxlIDs, pos_data_address, len_data_adress):
        dxl_present_position = [0] * len(dxlIDs)
        # Syncread present position
        dxl_comm_result = motor_sync_read.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

        # Check if groupsyncread data of Dynamixel Bicep is available
        for motorID in dxlIDs:
            dxl_getdata_result = motor_sync_read.isAvailable(motorID, pos_data_address, len_data_adress)
            if dxl_getdata_result != True:
                print("[ID:%03d] groupSyncRead getdata failed" % motorID)

        # Get Dynamixel#1 present position value
        for motorIndex in dxlIDs:
            dxl_present_position[motorIndex] = motor_sync_read.getData(dxlIDs[motorIndex], pos_data_address, len_data_adress)
            #print("ID:%03d, position = %03d" % (dxlIDs[motorIndex], dxl_present_position[motorIndex]))

        return dxl_present_position[motorIndex] 

def portTermination():
    TORQUE_DISABLE = 0
    # Disable Dynamixel Torque
    for motorID in DXL_ID:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
            portHandler, motorID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel", motorID,
                  "has been successfully disconnected")

    # Close port
    portHandler.closePort()


#List of all the sub functions used that the main functions call upon
# ------------------------------------------------------------------------------------------------------------------------------------------------------

#Equation used to convert from angle degrees to positional units and vice versa
#To go from angles to step positions, order of values is 0, 360, 0, 4095
#To go from step positions to degrees, order of values is 0, 4095, 0, 360
#Inputs are angles or units you want to convert.
#Outputs are the converted values of angles or units
def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

#Reads the data of one motor in a given address. Dynamixel XM430-W350-R has most data in 4 bytes
#Input is (ID of motor to be read, address where data resides)
#Output is the data value that was read
def ReadMotorData(motorIndex, data_address):
    data_value, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(
        portHandler, DXL_ID[motorIndex], data_address)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    return data_value

#Writes data to one motor at a given address. Dynamixel XM430-W350-R has most data in 4 bytes
#Input is (ID of motor to be read, address where data resides, data you want to write)
#There is no output
def WriteMotorData(motorIndex, data_address, data_inputs):
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
    portHandler, DXL_ID[motorIndex], data_address, data_inputs)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

#Checks the position of a motor.
#Input is the ID of the motor and the goal position that motor should move to
#Output is the present position of the motor and its status. If the status = 1, successful movement. If status = 0, failed movement
def motor_check(motorIndex, goal_position):
    motor_repetition_status = 0
    motor_status = 0
    
    motor_present_position = ReadMotorData(motorIndex, ADDR_PRESENT_POSITION)
    while 1:
        #Read moving status of motor. If status = 1, motor is still moving. If status = 0, motor stopped moving
        motor_new_position = ReadMotorData(motorIndex, ADDR_PRESENT_POSITION)

        #print("[ID:%03d] PresPos:%03d  NewPos:%03d" %
              #(DXL_ID[device_index], motor_present_position, motor_new_position))

        if (abs(motor_new_position - motor_present_position) < 2):
            motor_repetition_status += 1
        else:
            motor_repetition_status = 0
        if motor_repetition_status >= 10:
            break

        motor_present_position = motor_new_position
        #print("ID:%03d, motor_repetition_status: %03d" % (DXL_ID[device_index], motor_repetition_status))


        #Checks the present position of the motor and compares it to the goal position
        motor_check_value = abs(goal_position - motor_present_position)
        if (motor_check_value > DXL_MOVING_STATUS_THRESHOLD):
            motor_status = 0
            #print("ID:%03d, motor_check_value:%03d and motor status:%03d " % (DXL_ID[device_index],motor_check_value, motor_status))
        else:
            motor_status = 1
            #print("ID:%03d, motor_check_value:%03d and motor status:%03d " % (DXL_ID[device_index],motor_check_value, motor_status))
            break   

    return (motor_present_position, motor_status)

##Old Test Cases
#portInitialization(portname, baudrate, baseID, bicepID, forearmID):
"""portInitialization('COM3', 1000000, 1, 2, 3, 4, 5)

dxlSetVelo([0,0,0,0,0])
#dxl_current_velocity = dxlGetVelo()
#print(dxl_current_velocity)

angles_before = dxlPresAngle()
print(angles_before)

motorRunWithInputs([200,300,100,100,200])

angles_after = dxlPresAngle()
print(angles_after)


angles_before = dxlPresAngle()
print(angles_before)

motorRunWithInputs([0,0,0])

angles_after = dxlPresAngle()
print(angles_after)

angles_before = dxlPresAngle()
print(angles_before)

motorRunWithInputs([100,200,300,90,90])

angles_after = dxlPresAngle()
print(angles_after)

angles_before = dxlPresAngle()
print(angles_before)

motorRunWithInputs([50,150,250,120,300])

angles_after = dxlPresAngle()
print(angles_after)

portTermination()"""