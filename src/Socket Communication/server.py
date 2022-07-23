# server.py
# server file

import socket
from _thread import *
from time import sleep

# These are calling on user made python scripts
import extractJSONFile
import AES_Security

HOST = "127.0.0.1"  # Standard loop back interface address (local host)
PORT = 65434  # Port to listen on (non-privileged port are > 1023)


# Creating the server
def run_Server(HOST, PORT):
    # creating a socket object with socket.socket()
    # the socket type is socket.SOCKET_STREAM -> which is referring to the default TCP protocol security
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as active_Socket:
        try:
            active_Socket.bind((HOST, PORT))  # associate the socket with a specific network interface and port number
        except socket.error as e:
            print(str(e))

        print(f'Server is listening on port {PORT}...')
        active_Socket.listen()

        while True:
            accept_connections(active_Socket)


# Establishes a connection and creates a new thread for each client request
def accept_connections(active_socket):
    client, address = active_socket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(client_handler, (client, ))


# Handles the client -> will fetch data, encrypt the data, and then send it to the client
def client_handler(connection):

    with connection:
        print(f"Connected by {connection}")

        while True:
            byte_Data = extractJSONFile.retrieve_Data().decode('UTF-8')  # calling a method from a different script to get the data from the JSON file and decoding it into a string
            myKey = "EncrYption KEy!!"  # Using this variable for the encryption key to pass on to the security script
            encrypted_byte_Data = AES_Security.AESCipher(myKey).encrypt(byte_Data)  # calling the script "security" to encrypt "byte_Data"

            print("Encrypted data ready for the server to send: ", encrypted_byte_Data)
            connection.send(encrypted_byte_Data.encode('UTF-8'))  # sending the encrypted text as well as encoding it into byte format since sockets can only transfer as byte format

            sleep(1)  # in order for the server to be in sync with the client while sending data continuously, a time delay of 1 second is added

            # break out of while loop and close the server
            loopBreak = 0
            if loopBreak == 1:
                break


if __name__ == '__main__':
    run_Server(HOST, PORT)
