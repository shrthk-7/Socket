import socket
import threading

'''First message to the server must be an 8byte 
long header that contains the size of the upcoming message'''
HEADER = 8
PORT = 3000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'discon'

clients = []

#new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind(ADDR)

def broadcast(msg, currentConn):
	msg_length = len(msg)
	send_length = str(msg_length).rjust(HEADER).encode(FORMAT)
	for client in clients:
		conn = client['conn']
		if currentConn == conn:
			continue
		conn.send(send_length)
		conn.send(msg.encode(FORMAT))

def handle_client(conn, addr):
	print(f'[NEW CONNECTION] {addr}')

	while True:
		msg_length = conn.recv(HEADER).decode(FORMAT)
		if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(FORMAT)
			if msg == DISCONNECT_MESSAGE:
				print(f'[DISCONNECTED] {addr}')
				broadcast(f'[{addr} left]', conn)
				break
			broadcast(msg, conn)
			print(f'{addr} : {msg}')
	conn.close()

def start():
	server.listen()
	print(f'[LISTENING] Listening on {SERVER}')
	try:
		while True:
			conn, addr = server.accept()
			thread = threading.Thread(target=handle_client, args = (conn, addr))
			clients.append({
				'conn':conn,
				'addr':addr
			})
			broadcast(f'[{addr} joined]', conn)
			thread.start()
			print(f'[ACTIVE CONNECTIONS] {threading.active_count()-1}')
	except KeyboardInterrupt:
		print('[STOPPING] Server disconnected')

print('[STARTING] Server is starting...')
start()