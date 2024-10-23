from mojo import context
import threading
from socket_server import TCPServer, UDPServer

logger = context.log
idevice = context.devices.get("idevice")
relays = idevice.relay

def run_mojo():
    context.run(globals())

def on_message(data):
    logger.info(f"Received: {data}")
    if (data == '1'):
        relays[0].state.value = True
    elif (data == '0'):
        relays[0].state.value = False
    # tcp_server.send_clients(data)

if __name__ == '__main__':
    # mojo  start
    thread_mojo = threading.Thread(target=run_mojo)
    thread_mojo.start()
    logger.info('Mojo started')
    # tcp server
    HOST, PORT = '', 10002
    tcp_server = TCPServer(HOST, PORT, on_message)
    if tcp_server:
        server_thread = threading.Thread(target=tcp_server.start)
        server_thread.daemon = True
        server_thread.start()
    # udp server
    HOST, PORT = '', 10003
    udp_server = UDPServer(HOST, PORT, on_message)
    if udp_server:
        server_thread = threading.Thread(target=udp_server.start)
        server_thread.daemon = True
        server_thread.start()
    
    # end
    logger.info('Main thread running')

