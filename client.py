import socket

class Client(object):
	def __init__(self,address):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.address = address

	def connect(self):
		self.sock.connect(self.address)
	def send(self,message):
		self.sock.sendall(message)
	def receive(self):
		return self.sock.recv(1024)

	def disconnect(self):
		self.sock.close()
