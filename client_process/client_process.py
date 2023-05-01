print('Hello world from client')

import socket

PORT = 6666
HOST = "main_container"


def receive_utf_msg(socket_connection):
    length_of_message = int.from_bytes(socket_connection.recv(2), byteorder='big')
    msg = socket_connection.recv(length_of_message).decode("UTF-8")

    return msg


def send_msg_utf(socket_connection, msg):
    socket_connection.send(len(msg).to_bytes(2, byteorder='big'))
    socket_connection.send(bytes(msg, encoding="UTF-8"))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    data = receive_utf_msg(s)
    print(f"Recibido: {data}")

    send_msg_utf(s, "I am a message from client")

    with open("calculos.txt", 'r') as file:
        lines = [line.rstrip() for line in file]

        print(f"Calculos a realizar: {lines}")

        for line in lines:
            print(f"Enviado: {line}")
            send_msg_utf(s, line)
            response = receive_utf_msg(s)
            print(f"Respuesta: {response}")

        s.close()