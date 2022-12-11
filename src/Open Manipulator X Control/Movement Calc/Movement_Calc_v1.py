import math

#reference link:
#https://pdfs.semanticscholar.org/56a0/9731772199fe77bcb0dbff3a69f1c623e0c7.pdf

Z_OFFSET = 77                                                   #d1
BICEP_DIST = 130                                                #a2
FOREARM_DIST = 124                                              #a3
WRIST_DIST = 126                                                #a4


def angle_Calc(coor, FOREARM_MODE, CLAW_MODE):                                # coor[] = [Px, Py, Pz]
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
        theta1 = math.atan(coor[1]/coor[0])                     # theta1 = arctan(Py/Px) (11)
        print("theta1 = "+ str(math.degrees(theta1)) + "\n")
        return math.degrees(theta1), theta1

    def elbow_Theta():                                          # theta3 calculation (20)
        cosTheta3 = (math.pow(r2, 2) + math.pow(z2, 2) - (math.pow(BICEP_DIST, 2) + math.pow(FOREARM_DIST, 2)))/(2*BICEP_DIST*FOREARM_DIST)                 # cos_theta3 = [(r2)^2 + (z2)^2 - ((a2)^2 + (a3)^2)] / (2*a2*a3)
        print("cosTheta3 = "+ str(cosTheta3) + "\n")
        theta3 = math.acos(cosTheta3)                           # theta3 = arccos(cos_theta3)
        print("theta3 = "+ str(math.degrees(theta3)) + "\n")
        return math.degrees(theta3), theta3

    def shoulder_Theta(theta3_R):
        
        cosTheta2 = ((BICEP_DIST+FOREARM_DIST*math.cos(theta3_R))*r2 + (FOREARM_DIST*math.sin(theta3_R))*z2)/(math.pow(r2, 2) + math.pow(z2, 2))           # cos_theta2 = [(a2 + a3*cos_theta3)r2 + (a3*sin_theta3)z2] / (r^2 + z^2)
        print("cosTheta2 = "+ str(cosTheta2) + "\n")
        sinTheta2 = ((BICEP_DIST+FOREARM_DIST*math.cos(theta3_R))*z2 - (FOREARM_DIST*math.sin(theta3_R))*r2)/(math.pow(r2, 2) + math.pow(z2, 2))           # sin_theta2 = [(a2 + a3*cos_theta3)z2 - (a3*sin_theta3)r2] / (r^2 + z^2)
        print("sinTheta2 = "+ str(sinTheta2) + "\n")
        theta2 = math.atan(sinTheta2/cosTheta2)
        print("theta2 = "+ str(math.degrees(theta2)) + "\n")
        return math.degrees(theta2), theta2


    baseTheta, baseTheta_R = base_Theta()   
    Theta3, Theta3_R = elbow_Theta()
    if (FOREARM_MODE == 0):                                 # forearm_mode = 0 -> negative theta3 (forearm points down)
        Theta3 = -Theta3                                    # forearm_mode = 1 -> positive theta3 (forearm points up)
        Theta3_R = -Theta3_R
    elbowTheta = Theta3 - 11
    Theta2, Theta2_R = shoulder_Theta(Theta3_R)
    shoulderTheta = Theta2 + 11
    wristTheta = phi - elbowTheta - shoulderTheta
    print("theta4 = "+ str(wristTheta) + "\n")

    return [int(baseTheta), int(shoulderTheta), int(elbowTheta), int(wristTheta)]

if __name__ == "__main__":
    #rest coordinates
    # angle1 = angle_Calc([275, 0, 205], 0, 0)
    angle1 = angle_Calc([205, -70, 215], 1, 0)
    print(angle1)
