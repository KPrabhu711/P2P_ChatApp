import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #make a socket;AF.INET speciies IPv4 and SOCK_STREAM for TCP
sock.bind(('0.0.0.0', 10000))
sock.listen(5)  #specify how many connection requests can wait in queue

connections = []
lock = threading.Lock() #obtain lock to be used on the global variable connections

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
    cThread.daemon = True           #Automatically close when main program closes
    cThread.start()                 #Starts the thread
