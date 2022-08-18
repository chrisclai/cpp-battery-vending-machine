# extractJSONFile.py
# This is an extraction file to retrieve data from the JSON file

import json


def retrieve_Data():
    dataArray = [0] * 16  # this array will store the data from the JSON file

    print("CONNECTED TO ~~~ extractJSONFile.py")

    # Opening JSON file
    with open('GetBMSDataDump.json') as json_file:
        data = json.load(json_file)

        # The for-loop contains the information from the JSON file
        # to extract information from the JSON file and to pass it through the client-server
        # the string information must be converted into bytes in order for the socket to accept it
        loopCounter = 0
        for i in data['Battery Data']:

            # passData1 = i['ID']  # this will extract the data from the "Battery Data" section
            # byte_ID = bytearray(passData1, 'UTF-8')  # the data from the JSON file is converted to a bytearray
            # dataArray[0 + loopCounter] = byte_ID  # storing the data into an array
            #
            # passData2 = i['Capacity']  # this will extract the data from the "Capacity" section
            # byte_Capacity = bytearray(passData2, 'UTF-8')
            # dataArray[1 + loopCounter] = byte_Capacity
            #
            # passData3 = i['Energy']  # this will extract the data from the "Energy" section
            # byte_Energy = bytearray(passData3, 'UTF-8')
            # dataArray[2 + loopCounter] = byte_Energy
            #
            # passData4 = i['Charge Capacity']  # this will extract the data from the "Charge Capacity" section
            # byte_ChargeCapacity = bytearray(passData4, 'UTF-8')
            # dataArray[3 + loopCounter] = byte_ChargeCapacity
            #
            # passData5 = i['Temperature']  # this will extract the data from the "Temperature" section
            # byte_Temperature = bytearray(passData5, 'UTF-8')
            # dataArray[4 + loopCounter] = byte_Temperature
            #
            # passData6 = i['BMS Health']  # this will extract the data from the "BMS Health" section
            # byte_BMSHealth = bytearray(passData6, 'UTF-8')
            # dataArray[5 + loopCounter] = byte_BMSHealth
            #
            # passData7 = i['Total Voltage']  # this will extract the data from the "Total Voltage" section
            # byte_TotalVoltage = bytearray(passData7, 'UTF-8')
            # dataArray[6 + loopCounter] = byte_TotalVoltage

            passData1 = i['Cell 1 Voltage']  # this will extract the data from the "Cell 1 Voltage" section
            byte_Cell1Volt = bytearray(passData1, 'UTF-8')
            dataArray[0 + loopCounter] = byte_Cell1Volt

            passData2 = i['Cell 2 Voltage']  # this will extract the data from the "Cell 2 Voltage" section
            byte_Cell2Volt = bytearray(passData2, 'UTF-8')
            dataArray[1 + loopCounter] = byte_Cell2Volt

            passData3 = i['Cell 3 Voltage']  # this will extract the data from the "Cell 3 Voltage" section
            byte_Cell3Volt = bytearray(passData3, 'UTF-8')
            dataArray[2 + loopCounter] = byte_Cell3Volt

            passData4 = i['Cell 4 Voltage']  # this will extract the data from the "Cell 4 Voltage" section
            byte_Cell4Volt = bytearray(passData4, 'UTF-8')
            dataArray[3 + loopCounter] = byte_Cell4Volt

            #  incrementing the loop counter to access the other data
            loopCounter += 4

    # this portion of the code will get the byte array "dataArray" and will decode it into a string format
    temp_dataArray_storage = [0] * 16
    message = dataArray

    for x in range(16):
        convertThisData = message[x]
        temp_dataArray_storage[x] = convertThisData.decode()  # decodes it as a string and store as an array in "temp_dataArray_storage"

    thisConcatMsg = ' '.join(temp_dataArray_storage)  # this will take the array elements and will join it as a string with a space between each element
    byte_thisConcatMsg = thisConcatMsg.encode('utf-8')  # this takes "thisConcatMsg" and format it into a byte format

    return byte_thisConcatMsg


if __name__ == '__main__':
    print(retrieve_Data())
