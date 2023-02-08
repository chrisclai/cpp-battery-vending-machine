import math
import motorctrl_v1 as motor
import Movement_Calc_v2 as calculation

BASE_ID = 1
BICEP_ID = 2
FOREARM_ID = 3
WRIST_ID = 4
CLAW_ID = 0

PORT_NUM = 'COM3'
BAUDRATE = 1000000

MOVEARM_MODE = 1

ALL_IDs = [BASE_ID, BICEP_ID, FOREARM_ID, WRIST_ID, CLAW_ID]
MOVE_IDs = [BASE_ID, BICEP_ID, FOREARM_ID, WRIST_ID]

if __name__ == "__main__":
    motor.portInitialization(PORT_NUM, ALL_IDs)
    while (MOVEARM_MODE):
        x = int(input("Enter the goal X coordinate for the arm: "))
        y = int(input("Enter the goal Y coordinate for the arm: "))
        z = int(input("Enter the goal Z coordinate for the arm: "))
        print("""
        [0] CLAW PARALLEL TO GROUND
        [1] CLAW PERPENDICULAR TO GROUND
        [2] CLAW 45 DEGREE TO GROUND
        """)
        forearm_mode = int(input("Enter '0', '1', or '2' for forearm mode: "))

        claw_angle =  int(input("Enter the mode for the claw [0] to open and [1] to close: "))


        if (claw_angle == 0):
            motor.motorRunWithInputs([90], [0])
        else:
            motor.motorRunWithInputs([180], [0])

        coor = [x,y,z]
        angles = calculation.angle_Calc(coor, forearm_mode)
        print(angles)
        
        motor.dxlSetVelo([30,18,30,30,30], ALL_IDs)
        motor.simMotorRun(angles, MOVE_IDs)


        # motor.motorRunWithInputs([180], [0])
        # motor.motorRunWithInputs([225], [0])

        mode = input("Enter 'Y' to continue arm movement. Else, press any key: ")
        if (mode != 'Y'):
            MOVEARM_MODE = 0
            motor.portTermination()