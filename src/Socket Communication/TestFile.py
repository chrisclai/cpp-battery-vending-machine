# TestFile.py
# This is a test script to test the capability of extracting data from the JSON data dump from the client

import json
from time import sleep

while True:

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

    # printing the results from each array
    print(battery_id1[0])
    print(battery_id1[1])
    print(battery_id1[2])
    print(battery_id1[3])
    print(battery_id1[5])

    sleep(1)  # a delay of 1 second
