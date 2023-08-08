# import json
# import socket
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(('', 5700))
# server.listen(128)
#
#
# def recv_request():
#     try:
#         connect_sock, client_info = server.accept()
#         recv_req = connect_sock.recv(1024).decode('UTF-8', 'ignore')
#         connect_sock.close()
#
#         for i in range(len(recv_req)):
#             if recv_req[i] == '{' and recv_req[-1] == '\n':
#                 return json.loads(recv_req[i:])
#         return None
#     except RuntimeError:
#         return None
