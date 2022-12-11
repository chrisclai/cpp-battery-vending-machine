import math
from tkinter import E, S

#reference link:
#https://pdfs.semanticscholar.org/56a0/9731772199fe77bcb0dbff3a69f1c623e0c7.pdf

Z_OFFSET = 77                                                   # d1
BICEP_DIST = 130                                                # a2
FOREARM_DIST = 124                                              # a3
WRIST_DIST = 126                                                # a4

BASE_OFFSET = 225                                               # Offset between the theoretical theta1 and actual base angle value
SHOUDLER_OFFSET = 90                                            # Offset between the theoretical theta2 and actual base angle value 
ELBOW_OFFSET = 225                                              # Offset between the theoretical theta3 and actual base angle value 
WRIST_OFFSET = 180                                              # Offset between the theoretical theta4 and actual base angle value 

ELBOW_W_OFFSET = 10                                             # Offset for the elbow motor to account for the weight pulling the forearm down
OUT_OF_RANGE_F = 0

BASE_H_LIMIT = 135                                              # Upper Physical Limit of the Base Motor Theoretical Value
BASE_L_LIMIT = -135                                             # Lower Physical Limit of the Base Motor Theoretical Valuev
SHOULDER_H_LIMIT = 180                                          # Upper Physical Limit of the Shoulder Motor Theoretical Value
SHOULDER_L_LIMIT = 0                                            # Lower Physical Limit of the Shoulder Motor Theoretical Value
ELBOW_H_LIMIT = 0                                               # Upper Physical Limit of the Elbow Motor Theoretical Value
ELBOW_L_LIMIT = -180                                            # Lower Physical Limit of the Elbow Motor Theoretical Value
WRIST_H_LIMIT = 90                                              # Upper Physical Limit of the Wrist Motor Theoretical Value
WRIST_L_LIMIT = -90                                             # Lower Physical Limit of the Wrist Motor Theoretical Value

def angle_Calc(coor, CLAW_MODE):                                # coor[] = [Px, Py, Pz]
    if (CLAW_MODE == 0):
        phi = 0                                                 # claw parallel to the ground
    elif (CLAW_MODE == 1):
        phi = 90                                                # claw vertical to the ground
    else:
        phi = 45

    z3 = coor[2] - Z_OFFSET                                     # z3 = Pr - d1
    print("z3 = "+ str(z3) + "\n")
    z2 = z3 - WRIST_DIST*math.sin(math.radians(phi))            # z2 = z3 - a3*sin(phi)
    print("z2 = "+ str(z2) + "\n")
    
    Pr = math.sqrt(math.pow(coor[0],2)+math.pow(coor[1],2))     # r3 = Pr
    print("r3 = "+ str(Pr) + "\n")
    r2 = Pr - WRIST_DIST*math.cos(math.radians(phi))            # r2 = r3 - a4*cos(phi)
    print("r2 = "+ str(r2) + "\n")
    
    def base_Theta():      
        if (coor[0] == 0):                                      # if the base theta is 90 or -90 degree
            if (coor[1] > 0):
                theta1 = 90
            else:    theta1 = -90
        elif (coor[0] < 0):                                     # if base theta is greater than 90 or less than -90
            if (coor[1] > 0):
                theta1 = math.atan(coor[1]/coor[0]) + 180
            else:    theta1 = math.atan(coor[1]/coor[0]) - 180  
        else:                                                   # if base theta is within [-90,90]
            theta1 = math.atan(coor[1]/coor[0])                     # theta1 = arctan(Py/Px) (11)

        return math.degrees(theta1), theta1

    def elbow_Theta():                                          # theta3 calculation (20)
        cosTheta3 = (math.pow(r2, 2) + math.pow(z2, 2) - (math.pow(BICEP_DIST, 2) + math.pow(FOREARM_DIST, 2)))/(2*BICEP_DIST*FOREARM_DIST)                 # cos_theta3 = [(r2)^2 + (z2)^2 - ((a2)^2 + (a3)^2)] / (2*a2*a3)
        print("cosTheta3 = "+ str(cosTheta3) + "\n")
        theta3 = math.acos(cosTheta3)                           # theta3 = arccos(cos_theta3)
        print("theta3 = "+ str(-math.degrees(theta3)) + "\n")
        return -math.degrees(theta3), -theta3                   # Elbow motor motion is only physically posibble with negative theta3 value [-180, 0]

    def shoulder_Theta(theta3_R):
        
        cosTheta2 = ((BICEP_DIST+FOREARM_DIST*math.cos(theta3_R))*r2 + (FOREARM_DIST*math.sin(theta3_R))*z2)/(math.pow(r2, 2) + math.pow(z2, 2))           # cos_theta2 = [(a2 + a3*cos_theta3)r2 + (a3*sin_theta3)z2] / (r^2 + z^2)
        print("cosTheta2 = "+ str(cosTheta2) + "\n")
        sinTheta2 = ((BICEP_DIST+FOREARM_DIST*math.cos(theta3_R))*z2 - (FOREARM_DIST*math.sin(theta3_R))*r2)/(math.pow(r2, 2) + math.pow(z2, 2))           # sin_theta2 = [(a2 + a3*cos_theta3)z2 - (a3*sin_theta3)r2] / (r^2 + z^2)
        print("sinTheta2 = "+ str(sinTheta2) + "\n")
        theta2 = math.atan(sinTheta2/cosTheta2)
        if (theta2 <0):                                          # add offset when theta2 is negative (arm pointing to the ground)
            theta2 = theta2 + math.pi   
        print("theta2 = "+ str(math.degrees(theta2)) + "\n")
        return math.degrees(theta2), theta2


    baseTheta, baseTheta_R = base_Theta()   
    Theta3, Theta3_R = elbow_Theta()
    elbowTheta = Theta3 - 11                                     # (-90< elbowTheta <0) -> Forearm up # (-180< Theta3 <-90) -> Forearm down
    Theta2, Theta2_R = shoulder_Theta(Theta3_R)
    shoulderTheta = Theta2 + 11
    wristTheta = phi - elbowTheta - shoulderTheta
    print("theta4 = "+ str(wristTheta) + "\n")

    if ((baseTheta < BASE_L_LIMIT) or (baseTheta > BASE_H_LIMIT)):                                          
        print("Base angle calculated (%s) is out of physical range [-135, 135]" % (baseTheta))              # setting physical range limit for baseTheta [-135, 135]
        OUT_OF_RANGE_F = 1
    elif ((shoulderTheta < SHOULDER_L_LIMIT) or (shoulderTheta > SHOULDER_H_LIMIT)):
        print("Shoulder angle calculated (%s) is out of physical range [0, 180]" % (shoulderTheta))         # setting physical range limit for shoulderTheta [0, 180]
        OUT_OF_RANGE_F = 1
    elif ((elbowTheta > ELBOW_H_LIMIT) or (elbowTheta < ELBOW_L_LIMIT)):
        print("Elbow angle calculated (%s) is out of physical range [-180, 0]" % (elbowTheta))              # setting physical range limit for elbowTheta [-180, 0]
        OUT_OF_RANGE_F = 1   
    elif ((wristTheta > WRIST_H_LIMIT) or (wristTheta < WRIST_L_LIMIT)):
        print("Wrist angle calculated (%s) is out of physical range [-90, 90]" % (wristTheta))              # setting physical range limit for wristTheta [-90, 90]
        OUT_OF_RANGE_F = 1
    else:
        OUT_OF_RANGE_F = 0
    
    print("[%s, %s, %s, %s]" % (int(baseTheta), int(shoulderTheta), int(elbowTheta), int(wristTheta)))

    if (OUT_OF_RANGE_F):
        return 0
    else:
        return [int(baseTheta+BASE_OFFSET), int(shoulderTheta+SHOUDLER_OFFSET), int(elbowTheta+ELBOW_OFFSET+ELBOW_W_OFFSET), int(wristTheta+WRIST_OFFSET)]


# if __name__ == "__main__":
    #angle for the rest position of the arm
    #angle1 = angle_Calc([275, 0, 205], 0)

    #Test coordinate #1: first quadrant, smaller x, higher z
    #angle1 = angle_Calc([205, -70, 215], 2)

    #Test coordinate #2: second quadrant, larger x, lower z
    #angle1 = angle_Calc([295, 70, 195], 0)

    #Test coordinate #3: half x from rest, half z from rest, y=0
    #angle1 = angle_Calc([140, 0, 150], 0)

    #Test coordinate #3: half x from rest, higher z from rest, y=0 ******* Check with the real arm to see if this configuration is physically posibble with the parallel claw
    # angle1 = angle_Calc([140, 0, 220], 0)
    # print(angle1)
