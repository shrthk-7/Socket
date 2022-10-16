import socket
import threading

HEADER = 8
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 3000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'discon'
ADDR = (SERVER, PORT)

connected = True

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print('[JOINED SERVER]')

def send(msg):
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).rjust(HEADER).encode(FORMAT)
	client.send(send_length)
	client.send(message)

def receive():
	try:
		while connected:
			msg_length = client.recv(HEADER).decode(FORMAT)
			if msg_length:
				msg_length = int(msg_length)
				msg = client.recv(msg_length).decode(FORMAT)
				print(f">>>{msg}")
	except:
		pass
	print('[STOPPED RECEIVING]')

thread = threading.Thread(target=receive)
thread.start()

while connected:
	msg = input("")
	send(msg)
	if msg == DISCONNECT_MESSAGE:
		print('[DISCONNECTED]')
		break

client.close()