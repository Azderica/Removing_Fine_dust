import socket
 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('172.17.0.1', 12345))
server_socket.listen(0)
client_socket, addr = server_socket.accept()
data = client_socket.recv(65535)
print(data)
