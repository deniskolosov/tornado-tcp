import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 8888)
sock.connect(server_address)

s = 'Auth:: FastSource\r\nFoo:: Bar\r\n<Bar>:: baz\r\n13:: <144>\r\nEnd\r\n'
sock.send(s.encode('utf-8'))
print("message sent: ", s)
sock.close()
