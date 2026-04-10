import socket
import json
import cliente

from cliente.interface.broadcast_receiver import BroadcastReceiver

class Interface:
    def __init__(self):
        self.connection = socket.socket()
        self.connection.connect((cliente.SERVER_ADDRESS,cliente.PORT))

    def receive_str(self,connect, n_bytes: int) -> str:
        data = connect.recv(n_bytes)
        return data.decode()

    def send_str(self,connect, value: str) -> None:
        connect.send(value.encode())

    def send_int(self,connect:socket.socket, value: int, n_bytes: int) -> None:
        connect.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def receive_int(self,connect: socket.socket, n_bytes: int) -> int:
        data = connect.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def send_object(self,connection, obj):
        data = json.dumps(obj).encode('utf-8')
        size = len(data)
        self.send_int(connection, size, cliente.INT_SIZE)
        connection.send(data)

    def receive_object(self,connection):
        size = self.receive_int(connection, cliente.INT_SIZE)
        data = connection.recv(size)
        return json.loads(data.decode('utf-8'))

    def execute(self):
        receiver = BroadcastReceiver(self.connection)
        receiver.start()

        print("Preciso que introduza dois valores:")
        x:int = int(input("x="))
        y:int = int(input("y="))

        res = ""
        while res != ".":
            print("Qual é o cálculo que quer efetuar? x + - / ('.' para fim)")
            res = input()

            if res == "+":
                self.send_str(self.connection, cliente.ADD_OP)
                self.send_int(self.connection, x, cliente.INT_SIZE)
                self.send_int(self.connection, y, cliente.INT_SIZE)

            elif res == "-":
                self.send_str(self.connection, cliente.SUB_OP)
                self.send_int(self.connection, x, cliente.INT_SIZE)
                self.send_int(self.connection, y, cliente.INT_SIZE)
                
            elif res == "/":
                self.send_str(self.connection, cliente.DIV_OP)
                self.send_int(self.connection, x, cliente.INT_SIZE)
                self.send_int(self.connection, y, cliente.INT_SIZE)

        self.send_str(self.connection, cliente.END_OP)
                