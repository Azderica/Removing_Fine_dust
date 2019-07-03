import socket
import threading
import time

def send(sock):
    while True:
        sendData = input('')
        sock.send(sendData.encode('utf-8'))

def receive(sock):
    while True:
        recvData = sock.recv(1024)
        print('', recvData.decode('utf-8'))

# this is for checking 
my_ip_address = '172.17.0.1'
my_port = 8300

# wifi ip address
wifi_ip_address = '192.168.43.88'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((wifi_ip_address, my_port))
server_socket.listen(1)

client_socket, addr = server_socket.accept()

sender = threading.Thread(target=send, args=(client_socket,))
receiver = threading.Thread(target=receive, args=(client_socket,))

sender.start()
receiver.start()

while True:
    time.sleep(1)
    pass
