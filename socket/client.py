import socket
 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('172.17.0.1', 12345))
sock.send('Hello')

