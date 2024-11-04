import socket
import threading

class TCPServer:
    def __init__(self, host, port, callback=None):
        self.host = host
        self.port = port
        self.callback = callback
        self.clients = []
        self.thread = threading.Thread(target=self._start)

    def get_client(self, client, addr):
        while True:
            data = client.recv(1024)
            if not data:
                client.close()
                self.clients.remove(client)
                print(f"Connection closed from {addr}")
                break
            if self.callback:
                self.callback(data)
    
    def send_clients(self, data):
        if not self.clients:
            print("No clients connected")
            return
        for client in self.clients:
            client.sendall(data)
            
    def start(self):
        self.thread.daemon = True
        self.thread.start()
        
    def _start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(100)
        print(f"TCP Server Listening on {self.host}:{self.port}")
        while True:
            client, addr = self.server.accept()
            self.clients.append(client)
            client_thread = threading.Thread(target=self.get_client, args=(client,addr))
            client_thread.daemon = True
            client_thread.start()
            print(f"Connection TCP Server from {addr}")
            
    def stop(self):
        self.server.close()
        print(f"TCP Server Disconnected from {self.host}:{self.port}")
        
class TCPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = None
                
    def start(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        print(f"TCP Client Connected to {self.host}:{self.port}")
        
    def send(self, data):
        self.client.sendall(data)
        self.client.close()
        
    def stop(self):
        self.client.close()
        print(f"TCP Client Disconnected from {self.host}:{self.port}")
        
class UDPServer:
    def __init__(self, host, port, callback=None):
        self.host = host
        self.port = port
        self.callback = callback
        self.thread = threading.Thread(target=self._start)
        
    def start(self):
        self.thread.daemon = True
        self.thread.start()
        
    def _start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.host, self.port))
        print(f"UDP Server Listening on {self.host}:{self.port}")
        while True:
            data, addr = self.server.recvfrom(1024)
            # data에서 00 지우기
            data = data.decode().split('\x00')[0]
            if self.callback:
                self.callback(data)
            print(f"Received UDP Server from {addr}")
            
    def stop(self):
        self.server.close()
        print(f"UDP Server Disconnected from {self.host}:{self.port}")
        
class UDPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
    def send(self, data):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.sendto(data.encode(), (self.host, self.port))
        self.client.close()
        print(f"Sent UDP Client to {self.host}:{self.port}:{data}")
        
        
        