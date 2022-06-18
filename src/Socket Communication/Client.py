# Client

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65434  # The port used by the server


def run_Client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        run_printData(s)  # Run the function that will receive and print the JSON data file


def run_printData(s):
    # Making an array of size 22 to handle the data from the JSON file
    # The JSON file has 11 data points for ID battery 1 and
    # another 11 data points for ID battery 2.
    # NOTE: The array indexing starts from 0. Therefore, the data will be contained in index 0 to 21, which makes
    # 21 elements in total. The extra array element at index 22 is needed for the for loop or else it will throw an indexing error.
    data = [0] * 22

    # the for loop will insert the data into the array that is being received from the server from the JSON data file
    for x in range(22):
        data[x] = s.recv(4)
        convertThisData = data[x]
        data[x] = convertThisData.decode()  # converting from byte to int

    # Printing the data received from the server
    # Battery ID 1
    print("Received: ID -> #", data[0])
    print("Received: Capacity -> ", data[1], "%")
    print("Received: Energy ->", data[2], "wH")
    print("Received: Charge Capacity ->", data[3], "mAh")
    print("Received: Temperature ->", data[4], "C")
    print("Received: BMS Health ->", data[5], "%")
    print("Received: Total Voltage ->", data[6], "V")
    print("Received: Cell 1 Voltage ->", data[7], "V")
    print("Received: Cell 2 Voltage ->", data[8], "V")
    print("Received: Cell 3 Voltage ->", data[9], "V")
    print("Received: Cell 4 Voltage->", data[10], "V")

    # Battery ID 2
    print("Received: ID -> #", data[11])
    print("Received: Capacity -> ", data[12], "%")
    print("Received: Energy ->", data[13], "wH")
    print("Received: Charge Capacity ->", data[14], "mAh")
    print("Received: Temperature ->", data[15], "C")
    print("Received: BMS Health ->", data[16], "%")
    print("Received: Total Voltage ->", data[17], "V")
    print("Received: Cell 1 Voltage ->", data[18], "V")
    print("Received: Cell 2 Voltage ->", data[19], "V")
    print("Received: Cell 3 Voltage ->", data[20], "V")
    print("Received: Cell 4 Voltage->", data[21], "V")


if __name__ == '__main__':
    run_Client()
