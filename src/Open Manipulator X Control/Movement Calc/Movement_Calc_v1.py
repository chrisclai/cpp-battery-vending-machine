import math

#reference link:
#https://pdfs.semanticscholar.org/56a0/9731772199fe77bcb0dbff3a69f1c623e0c7.pdf

Z_OFFSET = 76.5                                                 #d1
BICEP_DIST = 128                                                #a2
FOREARM_DIST = 124                                              #a3
WRIST_DIST = 126                                                #a4


def angle_Calc(coor, CLAW_MODE):                                #coor[] = [Px, Py, Pz]
    if (CLAW_MODE == 0):
        phi = 0                                                 #claw parallel to the ground
    elif (CLAW_MODE == 1):
        phi = 90                                                #claw vertical to the ground
    else:
        phi = 45

    z3 = coor[2] - Z_OFFSET                                     #z3
    z2 = z3 - WRIST_DIST*math.cos(math.radians(phi))            #z2
    
    Pr = math.sqrt(math.pow(coor[0],2)+math.pow(coor[1],2))     #r3
    r2 = Pr - WRIST_DIST*math.sin(math.radians(phi))            #r2
    
    def base_Theta():
        baseTheta = math.degrees(math.atan(coor[1]/coor[0]))   #theta1 = arctan(Py/Px)
        return baseTheta
    def elbow_Theta():