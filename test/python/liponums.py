# This file contains a function that is to be imported
# into a script to produce 16 random numbers in a list
# corresponding to 4 discharging lipo batteries.
# Use at your own risk (contains time library)

import time
import random

class Lipo:
    # Instantiates a lipo battery simulation class.
    # numLipo represents the number of lipo batteries that you would like to simulate
    def __init__(self, numLipo):
        self.numLipo = numLipo
        self.lipoData = [0] * numLipo * 4 # 4S lipo contains 4 cells each
        self.randHigh = 4.20
        self.randLow = 3.90
        self.counter = 0

    # Method to retrieve smart (algorithm induced) random list of lipo batteries. 
    # Deprecates over time (depending on calls, contains a minute delay)
    # Resets if the number gets too low
    def getlipodata(self):
        self.counter += 1

        if self.counter == 100:
            self.randHigh -= 0.1
            self.randLow -= 0.1
            # get rid of floating point error
            self.randHigh = round(self.randHigh, 1)
            self.randLow = round(self.randLow, 1)
            # reset counter
            self.counter = 0

        if self.randLow <= 2.5:
            self.randHigh = 4.2
            self.randLow = 3.9
        
        for x in range(0, len(self.lipoData)):
            self.lipoData[x] = random.randrange(int(self.randLow*100), int(self.randHigh*100), 1)/100.0

        time.sleep(0.1) # 100ms delay to simulate microcontroller delay, may use multithreading

    # Method to print out information about internal counting variables for debugging purposes
    def debuglipo(self):
        print(f"Counter: {self.counter} \t randHigh: {self.randHigh} \t\t randLow: {self.randLow}")

# Use cases
lipoarray = Lipo(4) # 4 lipo batteries

while True:
    lipoarray.getlipodata()
    lipoarray.debuglipo()
    print(lipoarray.lipoData) # <-- contains your lipo data in a list
