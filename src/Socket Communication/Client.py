# client.py
# client file

import socket
import AES_Security

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65434  # The port used by the server


# For the client to make a connection with the server -> server.py
def run_Client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as active_socket:
        print('Waiting for connection')
        try:
            active_socket.connect((HOST, PORT))
            Receive_Decrypt_Print(active_socket)  # Run the function that will receive and print the JSON data file
        except socket.error as e:
            print(str(e))


# To receive, decrypt, and print the data that the server is sending
def Receive_Decrypt_Print(active_socket):

    # run in a loop so that the program can continue to print the data that is being extracted
    while True:

        # receiving the encrypted data coming from the server and storing it in "data_received"
        data_received = active_socket.recv(2048)
        print("Encrypted data received from the server: ", data_received)

        # decrypting the data that was received from the server
        myKey = "EncrYption KEy!!"
        decrypted_Text = AES_Security.AESCipher(myKey).decrypt(data_received)
        print("Decrypted text result: ", decrypted_Text)

        # "decrypted_Text" outputs as one long string
        # So, the data will need to be split. As it is split it is automatically put into an array and store in "array_Element"
        array_Element = decrypted_Text.split(" ")

        # Splitting the data from "array_Element" into 0-10 and 11-21 to be stored in "battery_id1" and "battery_id2"
        size = 11
        battery_id1 = [0] * size
        battery_id2 = [0] * size
        battery_id3 = [0] * size
        battery_id4 = [0] * size
        battery_id5 = [0] * size

        for i in range(55):
            if i <= 10:
                battery_id1[i] = array_Element[i]  # storing elements 0-10 of "array_Element" in "battery_id1"
            elif 11 <= i <= 21:
                battery_id2[i-11] = array_Element[i]  # storing elements 11-21 of "array_Element" in "battery_id2"
            elif 22 <= i <= 32:
                battery_id3[i-22] = array_Element[i]  # storing elements 22-32 of "array_Element" in "battery_id3"
            elif 33 <= i <= 43:
                battery_id4[i-33] = array_Element[i]  # storing elements 33-43 of "array_Element" in "battery_id4"
            elif 44 <= i <= 54:
                battery_id5[i-44] = array_Element[i]  # storing elements 44-54 of "array_Element" in "battery_id5"

        # Printing the data to the terminal
        # Battery ID 1
        print("~~~~~~~~~~~~PRINTING BATTERY ID 1~~~~~~~~~~~~")
        print("Received: ID -> #", battery_id1[0])
        print("Received: Capacity -> ", battery_id1[1], "%")
        print("Received: Energy ->", battery_id1[2], "wH")
        print("Received: Charge Capacity ->", battery_id1[3], "mAh")
        print("Received: Temperature ->", battery_id1[4], "C")
        print("Received: BMS Health ->", battery_id1[5], "%")
        print("Received: Total Voltage ->", battery_id1[6], "V")
        print("Received: Cell 1 Voltage ->", battery_id1[7], "V")
        print("Received: Cell 2 Voltage ->", battery_id1[8], "V")
        print("Received: Cell 3 Voltage ->", battery_id1[9], "V")
        print("Received: Cell 4 Voltage->", battery_id1[10], "V")

        # Battery ID 2
        print("~~~~~~~~~~~~PRINTING BATTERY ID 2~~~~~~~~~~~~")
        print("Received: ID -> #", battery_id2[0])
        print("Received: Capacity -> ", battery_id2[1], "%")
        print("Received: Energy ->", battery_id2[2], "wH")
        print("Received: Charge Capacity ->", battery_id2[3], "mAh")
        print("Received: Temperature ->", battery_id2[4], "C")
        print("Received: BMS Health ->", battery_id2[5], "%")
        print("Received: Total Voltage ->", battery_id2[6], "V")
        print("Received: Cell 1 Voltage ->", battery_id2[7], "V")
        print("Received: Cell 2 Voltage ->", battery_id2[8], "V")
        print("Received: Cell 3 Voltage ->", battery_id2[9], "V")
        print("Received: Cell 4 Voltage->", battery_id2[10], "V")

        # Battery ID 3
        print("~~~~~~~~~~~~PRINTING BATTERY ID 3~~~~~~~~~~~~")
        print("Received: ID -> #", battery_id3[0])
        print("Received: Capacity -> ", battery_id3[1], "%")
        print("Received: Energy ->", battery_id3[2], "wH")
        print("Received: Charge Capacity ->", battery_id3[3], "mAh")
        print("Received: Temperature ->", battery_id3[4], "C")
        print("Received: BMS Health ->", battery_id3[5], "%")
        print("Received: Total Voltage ->", battery_id3[6], "V")
        print("Received: Cell 1 Voltage ->", battery_id3[7], "V")
        print("Received: Cell 2 Voltage ->", battery_id3[8], "V")
        print("Received: Cell 3 Voltage ->", battery_id3[9], "V")
        print("Received: Cell 4 Voltage->", battery_id3[10], "V")

        # Battery ID 4
        print("~~~~~~~~~~~~PRINTING BATTERY ID 4~~~~~~~~~~~~")
        print("Received: ID -> #", battery_id4[0])
        print("Received: Capacity -> ", battery_id4[1], "%")
        print("Received: Energy ->", battery_id4[2], "wH")
        print("Received: Charge Capacity ->", battery_id4[3], "mAh")
        print("Received: Temperature ->", battery_id4[4], "C")
        print("Received: BMS Health ->", battery_id4[5], "%")
        print("Received: Total Voltage ->", battery_id4[6], "V")
        print("Received: Cell 1 Voltage ->", battery_id4[7], "V")
        print("Received: Cell 2 Voltage ->", battery_id4[8], "V")
        print("Received: Cell 3 Voltage ->", battery_id4[9], "V")
        print("Received: Cell 4 Voltage->", battery_id4[10], "V")

        # Battery ID 5
        print("~~~~~~~~~~~~PRINTING BATTERY ID 5~~~~~~~~~~~~")
        print("Received: ID -> #", battery_id5[0])
        print("Received: Capacity -> ", battery_id5[1], "%")
        print("Received: Energy ->", battery_id5[2], "wH")
        print("Received: Charge Capacity ->", battery_id5[3], "mAh")
        print("Received: Temperature ->", battery_id5[4], "C")
        print("Received: BMS Health ->", battery_id5[5], "%")
        print("Received: Total Voltage ->", battery_id5[6], "V")
        print("Received: Cell 1 Voltage ->", battery_id5[7], "V")
        print("Received: Cell 2 Voltage ->", battery_id5[8], "V")
        print("Received: Cell 3 Voltage ->", battery_id5[9], "V")
        print("Received: Cell 4 Voltage->", battery_id5[10], "V")


if __name__ == '__main__':
    run_Client()
