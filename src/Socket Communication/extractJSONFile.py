import json


def retrieve_Data():
    dataArray = [0] * 22  # this array will store the data from the JSON file

    print("CONNECTED TO ~~~ getDataFile")

    # Opening JSON file
    with open('data.json') as json_file:
        data = json.load(json_file)

        # The for-loop contains the information from the JSON file
        # to extract information from the JSON file and to pass it through the client-server
        # the string information must be converted into bytes in order for the socket to accept it
        loopCounter = 0
        for i in data['Battery Data']:

            passData1 = i['ID']  # this will extract the data from the "Battery Data" section
            byte_ID = bytearray(passData1, 'UTF-8')  # the data from the JSON file is converted to a bytearray
            dataArray[0 + loopCounter] = byte_ID  # storing the data into an array

            passData2 = i['Capacity']  # this will extract the data from the "Capacity" section
            byte_Capacity = bytearray(passData2, 'UTF-8')
            dataArray[1 + loopCounter] = byte_Capacity

            passData3 = i['Energy']  # this will extract the data from the "Energy" section
            byte_Energy = bytearray(passData3, 'UTF-8')
            dataArray[2 + loopCounter] = byte_Energy

            passData4 = i['Charge Capacity']  # this will extract the data from the "Charge Capacity" section
            byte_ChargeCapacity = bytearray(passData4, 'UTF-8')
            dataArray[3 + loopCounter] = byte_ChargeCapacity

            passData5 = i['Temperature']  # this will extract the data from the "Temperature" section
            byte_Temperature = bytearray(passData5, 'UTF-8')
            dataArray[4 + loopCounter] = byte_Temperature

            passData6 = i['BMS Health']  # this will extract the data from the "BMS Health" section
            byte_BMSHealth = bytearray(passData6, 'UTF-8')
            dataArray[5 + loopCounter] = byte_BMSHealth

            passData7 = i['Total Voltage']  # this will extract the data from the "Total Voltage" section
            byte_TotalVoltage = bytearray(passData7, 'UTF-8')
            dataArray[6 + loopCounter] = byte_TotalVoltage

            passData8 = i['Cell 1 Voltage']  # this will extract the data from the "Cell 1 Voltage" section
            byte_Cell1Volt = bytearray(passData8, 'UTF-8')
            dataArray[7 + loopCounter] = byte_Cell1Volt

            passData9 = i['Cell 2 Voltage']  # this will extract the data from the "Cell 2 Voltage" section
            byte_Cell2Volt = bytearray(passData9, 'UTF-8')
            dataArray[8 + loopCounter] = byte_Cell2Volt

            passData10 = i['Cell 3 Voltage']  # this will extract the data from the "Cell 3 Voltage" section
            byte_Cell3Volt = bytearray(passData10, 'UTF-8')
            dataArray[9 + loopCounter] = byte_Cell3Volt

            passData11 = i['Cell 4 Voltage']  # this will extract the data from the "Cell 4 Voltage" section
            byte_Cell4Volt = bytearray(passData11, 'UTF-8')
            dataArray[10 + loopCounter] = byte_Cell4Volt

            #  incrementing the loop counter to access the other data
            loopCounter += 11

    return dataArray


if __name__ == '__main__':
    retrieve_Data()
