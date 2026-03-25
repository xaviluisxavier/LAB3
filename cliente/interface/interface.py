import socket
import json
import cliente

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
        while True:
            print("Qual é o cálculo que quer efetuar? x + - / (escreva 'sair' para parar)")
            res:str = input()
            
            if res.lower() == 'sair':
                self.send_str(self.connection, cliente.END_OP)
                break
                
            print("Preciso que introduza dois valores:")
            x:int = int(input("x="))
            y:int = int(input("y="))

            if res =="+":
                self.send_str(self.connection,cliente.ADD_OP)
                self.send_int(self.connection,x, cliente.INT_SIZE)
                self.send_int(self.connection,y, cliente.INT_SIZE)
                res_val = self.receive_int(self.connection,cliente.INT_SIZE)
                print("O resultado da soma é:", res_val)
            elif res =="-":
                self.send_str(self.connection,cliente.SUB_OP)
                self.send_int(self.connection,x, cliente.INT_SIZE)
                self.send_int(self.connection,y, cliente.INT_SIZE)
                res_val = self.receive_int(self.connection,cliente.INT_SIZE)
                print("O resultado da subtracao é:", res_val)
            
            elif res =="/":
                self.send_str(self.connection, cliente.DIV_OP)
                self.send_int(self.connection, x, cliente.INT_SIZE)
                self.send_int(self.connection, y, cliente.INT_SIZE)
                resultado = self.receive_int(self.connection, cliente.INT_SIZE)
                
                if resultado == -1 and y == 0:
                    print("Erro: Não é possível dividir por zero!")
                else:
                    print("O resultado da divisão (inteira) é:", resultado)
                