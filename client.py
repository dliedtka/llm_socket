import sys
import socket 


if __name__ == "__main__":
    ip = sys.argv[1]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = ip
    port = 12345       
    client_socket.connect((host, port))

    message = input("Prompt: ")
    client_socket.send(message.encode('utf-8'))

    response = client_socket.recv(16384).decode('utf-8')
    print(response)

    client_socket.close()
    