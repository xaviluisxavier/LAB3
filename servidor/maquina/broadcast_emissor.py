import servidor
import threading
import time
import json
from typing import Dict
from servidor.maquina.lista_clientes import ListaClientes
from dados.dados import Dados

class ThreadBroadcast(threading.Thread):
    def __init__(self, lista_clientes: ListaClientes, dados: Dados, intervalo: int = 10):
        super().__init__(daemon=True)
        self.lista_clientes = lista_clientes
        self.dados = dados
        self.intervalo = intervalo
        self.running = True

    def send_int(self,connection, value: int, n_bytes: int) -> None:
        connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def send_object(self, connection, obj):
        data = json.dumps(obj).encode('utf-8')
        size = len(data)
        self.send_int(connection,size, servidor.INT_SIZE)
        connection.send(data)

    def broadcast_object(self, obj: Dict) -> None:
        """
        Broadcast
        """
        with self.lista_clientes._lock:
            for address, conn in list(self.lista_clientes._clientes.items()):
                try:
                    self.send_object(conn, obj)
                except Exception:
                    print(f"Removendo client morto {address}")
                    conn.close()
                    self.lista_clientes.remover(address)

    def run(self):
        print("ThreadBroadcast ativa")
        while self.running:
            try:
                time.sleep(self.intervalo)
                _hist = self.dados.get_operacoes()
                self.broadcast_object(_hist)
                print(f"Broadcast para {self.lista_clientes.obter_nr_clientes()} clients")
            except Exception as e:
                print(f"Erro: {e}")
                continue
        print("ThreadBroadcast terminada")