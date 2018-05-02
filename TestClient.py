# import socket
#
#
# def ConnectToServer(username):
#     print('Connect user')
#     sock = socket.socket()
#     sock.connect(('localhost', 9090))
#     sock.send(bytes(username, 'utf-8'))
#     resp = sock.recv(1024)
#     if resp == b'OK':
#         return sock
#     else:
#         return None
#
#
# services = [b'SAVE_KEY', b'DIFFIE-HELLMAN',  b'SEND_MESSAGE']
#
# try:
#     sock = ConnectToServer('Anton')
#     i = 0
#     print('Choose service')
#     for s in services:
#         print(i, ' -- ', s)
#         i += 1
#     service = services[int(input())]
#     sock.send(service)
#     answ = sock.recv(1024)
#     print(answ)
#     sock.send(b'1234 56789')
#     sock.close()
# except Exception as ex:
#     print('Exception:\n', ex.__str__())
#     sock.close()
#
#