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


#********* DYNAMIXEL Model definition *********   
PROTOCOL_VERSION = 2 #Dynamixel SDK has two operating modes: Protocol 1 or 2. This code uses 2
BAUDRATE = 1000000

    #List of all the addresses from the Control Table that is used for operation
ADDR_PRESENT_POSITION = 132 #Address of the positions of the motors
ADDR_PROFILE_VELOCITY = 112 #Address of the velocity of the motors
ADDR_GOAL_POSITION = 116 #Address of goal position
ADDR_MOVING = 122 #Address of value that states if motor is moving or not
ADDR_MOVING_STATUS = 123
DXL_MOVING_STATUS_THRESHOLD = 10    # Dynamixel moving status threshold
LEN_GOAL_POSITION = 4 #Byte Length of goal position
LEN_PRESENT_POSITION = 4 #Byte length of present positiond
ADDR_TORQUE_ENABLE = 64
TORQUE_ENABLE = 1

#******MOTOR DRIVE FUNCTIONS*******
#this is where we will put hardware team functions

#Initializes and enables all the motors
#Input is portname, baudrate, and Dynamixel motor IDs
#Portname is the serial port assigned to the U2D2. Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
#To check portname, please refer to either the Dynamixel Wizard or "Serial Ports" in Device Manager
#Baurate is the rate of information transfer via serial ports. Linux is 57600 and Windows is 1000000
#Dynamixel motor IDs can be found by using the Dynamixel Wizard.
#There is no output from this function
def portInitialization(portname, dxlIDs):

    global DEVICENAME
    DEVICENAME = portname  # All the motors share the same port when connected in series  
    global portHandler
    portHandler = PortHandler(DEVICENAME) # Initialize PortHandler instance and PacketHandler instance
    global packetHandler
    packetHandler = PacketHandler(PROTOCOL_VERSION)

    if portHandler.openPort(): #Enables communication between computer and motors
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        getch()
        quit()

    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE): #Sets rate of information transfer
        print("Succeeded to change the baudrate")
    else:
        print("Failed to change the baudrate")
        getch()
        quit()


    global DXL_ID # Set the motor ID for each dynamixel. ID 0,1,2 is base/bicep/forearm motors
    DXL_ID = dxlIDs
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
    print("-------------------------------------")
    

def dxlPresAngle(dxlIDs):
    idNum = len(dxlIDs)
    dxl_present_position = [0] * idNum
    dxl_present_angle = [0] * idNum

    print("DXL IDs being read: ", dxlIDs)
    for id in range(idNum): #Reads the current position of the motor
        dxl_present_position[id] = ReadMotorData(dxlIDs[id], ADDR_PRESENT_POSITION)
    print("Present positions are: ", dxl_present_position)

    for id in range(idNum): #Converts the position into angles
        dxl_present_angle[id] = _map(dxl_present_position[id], 0, 4095, 0, 360)
    print("Present angles are: ", dxl_present_angle)
    print("-------------------------------------")
    return (dxl_present_angle)


def dxlSetVelo(vel_array, dxlIDs):
    if (len(vel_array) == len(dxlIDs)):
        idNum = len(dxlIDs)
        for id in range(idNum):
                    WriteMotorData(dxlIDs[id], ADDR_PROFILE_VELOCITY, vel_array[id])
    else:
        print("ERROR: Number of velocity inputs not matching with number of DXL ID inputs!")
    print("-------------------------------------")
    dxlGetVelo(dxlIDs)


def dxlGetVelo(dxlIDs):
    idNum = len(dxlIDs)
    dxl_present_velocity = [0] * idNum

    print("DXL IDs being read: ", dxlIDs)
    for id in range(idNum):
        dxl_present_velocity[id] = ReadMotorData(dxlIDs[id], ADDR_PROFILE_VELOCITY)
    print("Velocities are ", dxl_present_velocity)
    print("-------------------------------------")
    return (dxl_present_velocity)


def motorRunWithInputs(angle_inputs, dxlIDs):
    idNum = len(dxlIDs)

    #Format is [base, bicep, forearm, wrist, claw]
    if (len(angle_inputs) == idNum):
        dxl_goal_angle = angle_inputs
        dxl_goal_inputs = [0] * idNum
        dxl_end_position = [0] * idNum
        dxl_end_angle = [0] * idNum
        movementStatus = [0] * idNum

        print("Motors are rotating. DXL ID: ", dxlIDs)
        # ------------------Start to execute motor rotation------------------------
        while 1:
            #Convert angle inputs into step units for movement
            for id in range(idNum):
                dxl_goal_inputs[id] = _map(dxl_goal_angle[id], 0, 360, 0, 4095)
            print("Goal angles are ", dxl_goal_angle)

            #Write goal position for all motors (base, bicep, forearm, wrist, claw)
            for id in range(idNum):
                WriteMotorData(dxlIDs[id], ADDR_GOAL_POSITION, dxl_goal_inputs[id])

                #Read position for each motor and set status of motor
                dxl_end_position[id], movementStatus[id] = motor_check(dxlIDs[id], dxl_goal_inputs[id]) #Read position for the motor
                dxl_end_angle[id] = _map(dxl_end_position[id], 0, 4095, 0, 360)
            #print("Angle for Dynamixel:%03d is %03d" % (DXL_ID[device_index], dxl_end_angle[device_index]))

            for id in range(idNum):
                print("Angle for Dynamixels %03d after execution is %03d ----------------------------" % (dxlIDs[id], dxl_end_angle[id]))
            # ------------------------------------------------------------------------------------------------------------------------------------------------------

            #Motor movement completes and motor movement status to be sent out
            # ------------------------------------------------------------------------------------------------------------------------------------------------------
            print("-------------------------------------")
            return movementStatus
    else:
        print("ERROR: Number of angle inputs not matching with number of DXL ID inputs")


def simMotorRun(angle_inputs, dxlIDs):
    idNum = len(dxlIDs)
    movementStatus = [1] * idNum

    #Format is [base, bicep, forearm, wrist, claw]
    if (len(angle_inputs) == idNum):
        dxl_goal_angle = angle_inputs
        dxl_goal_inputs = [0] * idNum
        dxl_end_position = [0] * idNum
        dxl_end_angle = [0] * idNum
        movementStatus = [0] * idNum

        print("Motors are simultaneously rotating. DXL ID: ", dxlIDs)
        # ------------------Start to execute motor rotation------------------------
        while 1:
            #Convert angle inputs into step units for movement
            for id in range(idNum):
                dxl_goal_inputs[id] = _map(dxl_goal_angle[id], 0, 360, 0, 4095)
            print("Goal angles are ", dxl_goal_angle)

            simWrite(dxl_goal_inputs, dxlIDs)
            dxl_end_position, movementStatus = simPosCheck(dxl_goal_inputs, dxlIDs)
            for id in range(idNum):
                dxl_end_angle[id] = _map(dxl_end_position[id], 0, 4095, 0, 360)
            
            for id in range(idNum):
                print("Angle for Dynamixel:%03d is %03d ----------------------------" % (dxlIDs[id], dxl_end_angle[id]))
            # ------------------------------------------------------------------------------------------------------------------------------------------------------
            print("-------------------------------------")
            return movementStatus
    else:
        print("ERROR: Number of angle inputs not matching with number of DXL ID inputs")
        return movementStatus


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
def ReadMotorData(motorID, data_address):
    data_value, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(
        portHandler, motorID, data_address)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    return data_value

#Writes data to one motor at a given address. Dynamixel XM430-W350-R has most data in 4 bytes
#Input is (ID of motor to be read, address where data resides, data you want to write)
#There is no output
def WriteMotorData(motorID, data_address, data_inputs):
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
    portHandler, motorID, data_address, data_inputs)
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

#The functions take in an array of X angle inputs and an array of X dynamixel IDs. Running the functions will drive the X dynamixels to the desired angle inputs simultaneously
def simWrite(dxl_goal_inputs, dxlIDs):
    idNum = len(dxlIDs)
    #Intializate simultaneous motor movement
    global motor_sync_write
    motor_sync_write = GroupSyncWrite(portHandler, packetHandler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)
    global motor_sync_read
    motor_sync_read = GroupSyncRead(portHandler, packetHandler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
    #print("Motor_Sync_Write is ", motor_sync_write)
    #print("Motor_Sync_Read is ", motor_sync_read)

    #Create parameter storage for present positions
    for id in range(idNum):
        dxl_addparam_result = motor_sync_read.addParam(dxlIDs[id])
        if dxl_addparam_result != True:
            print("[ID:%03d] groupSyncRead addparam failed" % dxlIDs[id])
        #print("DXL_ADDPARAM_RESULT is " ,dxl_addparam_result)

    param_goal_position = [0] * idNum
    #Allocate goal position values into 4-byte array for bicep and forearm motors. Dynamixel motors use either 2-bytes or 4-bytes
    for id in range(idNum): 
        param_goal_position[id] = [DXL_LOBYTE(DXL_LOWORD(dxl_goal_inputs[id])), DXL_HIBYTE(DXL_LOWORD(dxl_goal_inputs[id])),DXL_LOBYTE(DXL_HIWORD(dxl_goal_inputs[id])), DXL_HIBYTE(DXL_HIWORD(dxl_goal_inputs[id]))]
    #print("param_goal_bicep_position is ", param_goal_position[1])
    #print("param_goal_bicep_position is ", param_goal_position[2])

    for id in range(idNum): 
    #Add goal position input values of bicep and forearm motors to Syncwrite parameter storage
        dxl_addparam_result = motor_sync_write.addParam(dxlIDs[id], param_goal_position[id])
        if dxl_addparam_result != True:
            print("[ID:%03d] groupSyncWrite addparam failed" % dxlIDs[id])
        #print("groupSyncWrite for [ID:%03d] works" % (DXL_ID[device_index]))
   
    #Syncwrite goal position to bicep and forearm motors
    dxl_comm_result = motor_sync_write.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

    #Clear syncwrite parameter storage
    motor_sync_write.clearParam()

def simPosCheck(dxl_goal_inputs, dxlIDs):
    idNum = len(dxlIDs)
    def simReadData():
        dxl_present_position = [0] * idNum
        # Syncread present position
        dxl_comm_result = motor_sync_read.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

        # Check if groupsyncread data of Dynamixel is available
        for motorID in dxlIDs:
            dxl_getdata_result = motor_sync_read.isAvailable(motorID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
            if dxl_getdata_result != True:
                print("[ID:%03d] groupSyncRead getdata failed" % motorID)

        # Get Dynamixel present position value
        for id in range(idNum):
            dxl_present_position[id] = motor_sync_read.getData(dxlIDs[id], ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
            #print("ID:%03d, position = %03d" % (dxlIDs[motorIndex], dxl_present_position[motorIndex]))

        return dxl_present_position
    
    print("Simultaneous position checking. DXL IDs being read: ", dxlIDs)
    repetition_status = [0] * idNum
    movement_status = [0] * idNum

    present_position = simReadData()
    kicker = 0
    while (kicker == 0):
        new_position = simReadData()
        #Kicker method to prevent the infinite looping of the motor
        for id in range(idNum):
            if (abs(new_position[id] - present_position[id]) < 2) and movement_status[id] == 0:
                repetition_status[id] += 1
            else:
                repetition_status[id] = 0
            if repetition_status[id] >= 10:
                kicker = 1
        
        present_position = new_position

        movement_complete_count = 0
        for id in range(idNum):
            if (abs(dxl_goal_inputs[id]- present_position[id]) < DXL_MOVING_STATUS_THRESHOLD):
                movement_complete_count += 1
                movement_status[id] = 1
        
        if (movement_complete_count == idNum):
            kicker = 1
    
    return present_position, movement_status



# if __name__ == "__main__":
#     #portInitialization(portname, baudrate, baseID, bicepID, forearmID):
#     portInitialization('COM4', [1,2,3,4])

#     # portInitialization('/dev/ttyUSB0', 1000000, 1, 3)

#     dxlSetVelo([30,30,30,30],  [1,2,3,4])

#     #rest position, [275, 0, 205],  claw parallel, 
#     motorRunWithInputs([225, 179, 145, 179],[1,2,3,4])

#     # motorRunWithInputs([270], [4])
#     # time.sleep(2)

#     motorRunWithInputs([225], [3])
#     time.sleep(2)

    
#     motorRunWithInputs([90], [2])
#     time.sleep(2)

#     motorRunWithInputs([270], [2])
#     time.sleep(2)
