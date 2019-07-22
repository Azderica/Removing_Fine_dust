import socket
import threading
import time


def send(sock):
    while True:
        sendData = input('>>> ')
        sock.send(sendData.encode('utf-8'))


def receive(sock):
    while True:
        recvData = sock.recv(1024)
        print('You : ', recvData.decode('utf-8'))

# ip_address = "172.31.31.144"
# port = 9999
wifi_ip_address = "192.168.43.41"

my_ip_address = '172.17.0.1'
my_port = 9009

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((wifi_ip_address, my_port))

sender = threading.Thread(target=send, args=(sock,))
receiver = threading.Thread(target=receive, args=(sock,))

sender.start()
receiver.start()

while True:
    time.sleep(1)
    pass
