print('Hello world from main')

import numexpr
import socket
import _thread
import threading

PORT = 6666


def receive_utf_msg(socket_connection):
    length_of_message = int.from_bytes(socket_connection.recv(2), byteorder='big')
    msg = socket_connection.recv(length_of_message).decode("UTF-8")

    return msg


def send_msg_utf(socket_connection, msg):
    socket_connection.send(len(msg).to_bytes(2, byteorder='big'))
    socket_connection.send(bytes(msg, encoding="UTF-8"))


def client_logic(socket_connection):
    with socket_connection:  # With the open connection
        thread_id = threading.current_thread().ident
        print(f"Thread ID {thread_id}: Connected by {addr}")

        send_msg_utf(socket_connection, "I am a message from main")
        data = receive_utf_msg(socket_connection)

        print(data)




print('Inicializando socket')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        _thread.start_new_thread(client_logic, (conn,))
