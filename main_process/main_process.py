print('Hello world from main')

import numexpr
import socket
import _thread
import threading
import pymongo

PORT = 6666


def receive_utf_msg(socket_connection):
    length_of_message = int.from_bytes(socket_connection.recv(2), byteorder='big')
    msg = socket_connection.recv(length_of_message).decode("UTF-8")

    return msg

def send_msg_utf(socket_connection, msg):
    socket_connection.send(len(msg).to_bytes(2, byteorder='big'))
    socket_connection.send(bytes(msg, encoding="UTF-8"))


mongoClient = pymongo.MongoClient('mongoDB', 27017)
mongoDB = mongoClient['calculos']
calculosCol = mongoDB['calculos']


def client_logic(socket_connection):
    with socket_connection:  # With the open connection
        thread_id = threading.current_thread().ident
        print(f"Thread ID {thread_id}: Connected by {addr}")

        send_msg_utf(socket_connection, "I am a message from main")
        data = receive_utf_msg(socket_connection)

        print(f"Thread {thread_id}: Recibido: {data}")

        while True:
            calculo_rec = receive_utf_msg(socket_connection)

            if len(calculo_rec) == 0:
                break

            print(f"Thread {thread_id}: Recibido: {calculo_rec}")

            dbResponse = calculosCol.find_one({"calculo":{ '$eq': calculo_rec }})

            if dbResponse:
                print(f'Thread {thread_id}: Respondiendo desde DB:{calculo_rec}')
                send_msg_utf(socket_connection, dbResponse['response'])
            else:
                calculo = str(numexpr.evaluate(calculo_rec.replace('^', '**')))
                calculosCol.insert_one({"calculo":calculo_rec, "response":calculo})
                print(f'Thread {thread_id}: Respondiendo:{calculo}')

                send_msg_utf(socket_connection, calculo)





print('Inicializando socket')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        _thread.start_new_thread(client_logic, (conn,))
