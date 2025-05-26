import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 10000))
sock.listen(5)

connections = []
lock = threading.Lock()

def handler(c, a):
    global connections
    try:
        while True:
            data = c.recv(1024)
            if not data:
                break  # Exit the loop if client disconnects

            with lock:
                # Broadcast to all others except the sender
                for connection in connections:
                    if connection != c:
                        try:
                            connection.send(data)
                        except:
                            pass  # Ignore broken sockets
    finally:
        with lock:
            if c in connections:
                connections.remove(c)
        c.close()

while True:
    conn, addr = sock.accept()
    with lock:
        connections.append(conn)
    print(f"Connected: {addr}, Active Connections: {len(connections)}")

    cThread = threading.Thread(target=handler, args=(conn, addr))
    cThread.daemon = True
    cThread.start()
