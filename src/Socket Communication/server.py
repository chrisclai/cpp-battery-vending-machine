# server.py
# server file

import socket
import extractJSONFile
import AES_Security

HOST = "127.0.0.1"  # Standard loop back interface address (local host)
PORT = 65434  # Port to listen on (non-privileged port are > 1023)


def run_Server():
    # creating a socket object with socket.socket()
    # the socket type is socket.SOCKET_STREAM -> which is referring to the default TCP protocolsecurity
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as active_Socket:
        active_Socket.bind((HOST, PORT))  # associate the socket with a specific network interface and port number
        active_Socket.listen()
        connection, addr = active_Socket.accept()

        with connection:
            print(f"Connected by {addr}")

            while True:
                byte_Data = extractJSONFile.retrieve_Data().decode('UTF-8')  # calling a method from a different script to get the data from the JSON file and decoding it into a string
                myKey = "EncrYption KEy!!"  # Using this variable for the encryption key to pass on to the security script
                encrypted_byte_Data = AES_Security.AESCipher(myKey).encrypt(byte_Data)  # calling the script "security" to encrypt "byte_Data"

                print("Encrypted data ready for the server to send: ", encrypted_byte_Data)
                connection.send(encrypted_byte_Data.encode('UTF-8'))  # sending the encrypted text as well as encoding it into byte format since sockets can only transfer as byte format

                # break out of while loop and close the server
                loopBreak = 1

                if loopBreak == 1:
                    break


if __name__ == '__main__':
    run_Server()
