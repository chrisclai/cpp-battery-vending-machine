# Server

import socket
import extractJSONFile

HOST = "127.0.0.1"  # Standard loop back interface address (local host)
PORT = 65434  # Port to listen on (non-privileged port are > 1023)


def run_Server():
    # creating a socket object with socket.socket()
    # the socket type is socket.SOCKET_STREAM -> which is referring to the default TCP protocol
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))  # associate the socket with a specific network interface and port number
        s.listen()
        conn, addr = s.accept()

        with conn:
            print(f"Connected by {addr}")

            loopBreak = 0
            while True:
                byte_Data = extractJSONFile.retrieve_Data()  # calling a function from a different script to get the data from the JSON file

                for i in range(22):
                    conn.send(byte_Data[i])  # sending the data from the JSON file to the client
                    loopBreak = 1

                # break out of while loop and close the server
                if loopBreak == 1:
                    break


if __name__ == '__main__':
    run_Server()
    extractJSONFile.retrieve_Data()
