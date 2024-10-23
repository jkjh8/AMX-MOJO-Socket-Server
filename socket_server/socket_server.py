from mojo import context
import socket
import threading

class TCPServer:
    def __init__(self, host, port, callback=None):
        self.host = host
        self.port = port
        self.callback = callback
        self.clients = []
        self.logger = context.log

    def get_client(self, client, addr):
        while True:
            data = client.recv(1024)
            if not data:
                client.close()
                self.clients.remove(client)
                self.logger.warn(f"Connection closed from {addr}")
                break
            if self.callback:
                self.callback(data)
    
    def send_clients(self, data):
        if not self.clients:
            self.logger.warn("No clients connected")
            return
        for client in self.clients:
            client.sendall(data)
            
    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(100)
        self.logger.info(f"TCP Server Listening on {self.host}:{self.port}")
        while True:
            client, addr = self.server.accept()
            self.clients.append(client)
            client_thread = threading.Thread(target=self.get_client, args=(client,addr))
            client_thread.daemon = True
            client_thread.start()
            self.logger.info(f"Connection TCP Server from {addr}")
            
    def stop(self):
        self.server.close()
        
class UDPServer:
    def __init__(self, host, port, callback=None):
        self.host = host
        self.port = port
        self.callback = callback
        self.logger = context.log
        
    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.host, self.port))
        self.logger.info(f"UDP Server Listening on {self.host}:{self.port}")
        while True:
            data, addr = self.server.recvfrom(1024)
            # data에서 00 지우기
            data = data.decode().split('\x00')[0]
            if self.callback:
                self.callback(data)
            self.logger.info(f"Received UDP Server from {addr}")
            
    def stop(self):
        self.server.close()
        
class UDPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.logger = context.log
        
    def send(self, data):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.sendto(data.encode(), (self.host, self.port))
        self.client.close()
        self.logger.info(f"Sent UDP Client to {self.host}:{self.port}")
        
        