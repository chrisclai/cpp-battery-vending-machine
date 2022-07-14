# client.py
# client file

import socket
import AES_Security

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65434  # The port used by the server


def run_Client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as active_socket:
        active_socket.connect((HOST, PORT))
        Receive_Decrypt_Print(active_socket)  # Run the function that will receive and print the JSON data file


def Receive_Decrypt_Print(active_socket):

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

    for i in range(22):
        if i <= 10:
            battery_id1[i] = array_Element[i]  # storing elements 0-10 of "array_Element" in "battery_id1"
        elif i >= 11:
            battery_id2[i-11] = array_Element[i]  # storing elements 11-21 of "array_Element" in "battery_id2"

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

    return data_received


if __name__ == '__main__':
    run_Client()
