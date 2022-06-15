# Server

import socket
import json

HOST = "127.0.0.1"  # Standard loopback interface address (local host)
PORT = 65434  # Port to listen on (non-privileged port are > 1023)


# creating a socket object with socket.socket()
# the socket type is socket.SOCKET_STREAM -> which is referring to the default TCP protocol
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # associate the socket with a specific network interface and port number
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:

            # Opening JSON file
            with open('data.json') as json_file:
                data = json.load(json_file)

                # The for-loop contains the information from the JSON file
                # to extract information from the JSON file and to pass it through the client-server
                # the string information must be converted into bytes in order for the socket to accept it
                for i in data['Battery Data']:
                    passData1 = i['ID']  # this will extract the data from the "Battery Data" section
                    encode1 = passData1.encode()
                    byte_ID = bytearray(encode1)  # the data from the JSON file is convert to a bytearray
                    conn.send(byte_ID)  # the byte version of the JSON data is sent through the socket

                    passData2 = i['Capacity']  # this will extract the data from the "Capacity" section
                    encode2 = passData2.encode()
                    byte_Capacity = bytearray(encode2)
                    conn.send(byte_Capacity)

                    passData3 = i['Energy']  # this will extract the data from the "Energy" section
                    encode3 = passData3.encode()
                    byte_Energy = bytearray(encode3)
                    conn.send(byte_Energy)

                    passData4 = i['Charge Capacity']  # this will extract the data from the "Charge Capacity" section
                    encode4 = passData4.encode()
                    byte_ChargeCapacity = bytearray(encode4)
                    conn.send(byte_ChargeCapacity)

                    passData5 = i['Temperature']  # this will extract the data from the "Temperature" section
                    encode5 = passData5.encode()
                    byte_Temperature = bytearray(encode5)
                    conn.send(byte_Temperature)

                    passData6 = i['BMS Health']  # this will extract the data from the "BMS Health" section
                    encode6 = passData6.encode()
                    byte_BMSHealth = bytearray(encode6)
                    conn.send(byte_BMSHealth)

                    passData7 = i['Total Voltage']  # this will extract the data from the "Total Voltage" section
                    encode7 = passData7.encode()
                    byte_TotalVoltage = bytearray(encode7)
                    conn.send(byte_TotalVoltage)

                    passData8 = i['Cell 1 Voltage']  # this will extract the data from the "Cell 1 Voltage" section
                    encode8 = passData8.encode()
                    byte_Cell1Volt = bytearray(encode8)
                    conn.send(byte_Cell1Volt)

                    passData9 = i['Cell 2 Voltage']  # this will extract the data from the "Cell 2 Voltage" section
                    encode9 = passData9.encode()
                    byte_Cell2Volt = bytearray(encode9)
                    conn.send(byte_Cell2Volt)

                    passData10 = i['Cell 3 Voltage']  # this will extract the data from the "Cell 3 Voltage" section
                    encode10 = passData10.encode()
                    byte_Cell3Volt = bytearray(encode10)
                    conn.send(byte_Cell3Volt)

                    passData11 = i['Cell 4 Voltage']  # this will extract the data from the "Cell 4 Voltage" section
                    encode11 = passData11.encode()
                    byte_Cell4Volt = bytearray(encode11)
                    conn.send(byte_Cell4Volt)

