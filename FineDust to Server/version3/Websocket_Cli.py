from websocket import create_connection
import time

ws = create_connection("ws://15.164.166.134:8000/")
while(True) :
    print("Sending 'Hello, World'...")
    ws.send("Hello, World")
    print("Sent")
    print("Receiving...")
    result =  ws.recv()
    print("Received '%s'" % result)
    time.sleep(2)
ws.close()
    