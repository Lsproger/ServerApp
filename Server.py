from UserConnection import Connection
from socket import socket
import sqlite3
import threading
import collections


client_listeners = []
connections = []
port = 9090
ClientListener = collections.namedtuple('ClientListener', ['username', 'addr', 'port'])


def GetKey(conn: socket, addr, username):
    print('GetKey service started')
    usr = conn.recv(1024).decode(encoding='utf-8')

    dbconn = sqlite3.connect('ServerStorage.db')
    cur = dbconn.cursor()
    cur.execute("select openkey_x , openkey_y from OPEN_KEYS where username =  ?", [(usr)])
    key = cur.fetchone()
    print(key)
    if key is not None:
        key = key[0] + ';' + key[1]
        conn.send(bytes(key, 'utf-8'))
    else:
        conn.send(bytes('0 0', 'utf-8'))


def SaveKey(conn: socket, addr, username):
    print('SaveKey service started')
    key_string = conn.recv(1024).decode(encoding='utf-8')
    key = str(key_string).split(';')
    print(key)
    dbconn = sqlite3.connect('ServerStorage.db')
    cur = dbconn.cursor()
    cur.execute("insert or replace into OPEN_KEYS values(?, ?, ?)", (username, key[0], key[1]))
    dbconn.commit()
    # cursor = dbconn.cursor()


def DiffieHellman(conn: socket, addr, username):
    print('DiffieHellman service started')
    client_name = conn.recv(1024).decode(encoding='utf-8')
    client = None
    for c in client_listeners:
        if c.username == client_name:
            client = c
            print(client)
            break
    if client is not None:
        caddr_port = str(client.addr) + ';' + str(client.port)
        conn.send(bytes(caddr_port, 'utf-8'))
    else:
        conn.send(b'Fail')


def Disconnect(conn: socket, addr, username):
    for c in connections:
        if c.username == username:
            conn.close()
            connections.remove(c)


def PSEC_KEM(conn: socket, addr, username):
    print('PSEC_KEM service started')
    client_name = conn.recv(1024).decode(encoding='utf-8')
    client = None
    for c in client_listeners:
        if c.username == client_name:
            client = c
            print(client)
            break
    if client is not None:
        caddr_port = str(client.addr) + ';' + str(client.port)
        conn.send(bytes(caddr_port, 'utf-8'))
    else:
        conn.send(b'Fail')


def RegisterListener(conn: socket, addr, username):
    print('RegisterListener service started')
    listener_port = conn.recv(1024).decode(encoding='utf-8')
    client_listener = ClientListener(username, addr[0], listener_port)
    client_listeners.append(client_listener)
    conn.send(b'OK')
    print(client_listeners)
    print(connections)


services = {'SAVE_KEY': SaveKey,
            'GET_KEY': GetKey,
            'DIFFIE-HELLMAN': DiffieHellman,
            'SEND_MESSAGE': PSEC_KEM,
            'DISCONNECT': Disconnect,
            'REGISTER_LISTENER': RegisterListener}


def StartService(conn: socket, addr, username):
    #try:
        service = conn.recv(1024)
        print(service)
        isOK = False
        for s in services.keys():
            if service.decode(encoding='utf-8') == s:
                conn.send(bytes(s, 'utf-8'))
                t = threading.Thread(target=services[s], args=(conn, addr, username))
                t.start()
                t.join()
                isOK = True
                break
        if not isOK:
            conn.send(b'No such service')
    #except ConnectionResetError:
     #   print('Client connection is refused')
        # TODO: delete listener from list


def DispatchServer(conn: socket, addr, username):
    print('Dispatch started:', addr)
    while conn is not None:
        StartService(conn, addr, username)


def AcceptServer(sock: socket, command):
    try:
        while command[0] != 'exit':
            print('Accept')
            conn, addr = sock.accept()
            username = conn.recv(1024).decode(encoding='utf-8')
            conn.send(b'OK')
            connections.append(Connection(conn, addr, username))
            print('Client connected:\n\taddress: ', addr, '\n\tUsername: ', username)
            threading.Thread(target=DispatchServer, args=(conn, addr, username)).start()
    except Exception as ex:
        print('Exception %s' % ex.__str__())
        if sock:
            sock.close()
            print('Socket closed')
            raise SystemExit
    quit(1)


def CommandCycle(ssocket, command):
    while command[0] != 'exit':
        command[0] = input('Enter command:')
        if command[0] == 'exit':
            ssocket.close()
            quit(1)


if __name__ == '__main__':
    sock = socket()
    llist = [['work']]
    cmd = llist[0]
    x = 10
    print('Accept')
    sock.bind(('', port))
    print('listen')
    sock.listen(1)
    accept_serv = threading.Thread(target=AcceptServer, args=(sock, cmd))

    accept_serv.setDaemon(True)

    accept_serv.start()
    CommandCycle(sock, cmd)
    accept_serv.join()



