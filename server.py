import socket

# CHANGE IP AND PORT!!!!

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 10001))  # max port 65535
sock.listen(socket.SOMAXCONN)
conn, addr = sock.accept()

while True:
    data = conn.recv(1024)
    if not data:
        break
        # process data
    print(data)

    conn.send(data+':'.encode('ascii'))


conn.close()
sock.close()
