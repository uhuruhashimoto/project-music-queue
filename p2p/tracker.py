"""
Tracker.py
Group 7: Project Music Queue
CS60 Dartmouth Xia Zhou 

Jonah Weinbaum
James Fleming
Uhuru Hashimoto
Thomas White
Wendell Wu


This class allows a user to create a new client. 
Connect to the tracker and then all the peers, and then send and receive blocks use the block and blockchain API's

"""
import select, sys, queue
import json 
from socket import *

BUFF_SIZE = 1024 # in Kb

# Port number that we open and wait for connections from clients
class Tracker:
	"""
	Construct the tracker object. Tracker keeps track of the list of
	clients for now. TODO: handle voting/blockchain stuff
	"""
	def __init__(self):
		self.listeningPort = 60005

		# A list of all clients which sent to new clients
		# 4-tuple of ips, port, public key, and socket
		self.clients = []
		
		self.ip = gethostbyname(gethostname())
		print(f"Found our own ip: {self.ip}")
		
		# our listening socket
		self.trackerSock = None

		# Open Tracker listening Socket
		self.Open()

	'''
	Opens self.trackersock as a listening socket
	'''
	def Open(self):
		# Create a socket and start listening on it
		self.trackerSock = socket(AF_INET, SOCK_STREAM)
		
		self.trackerSock.bind((self.ip, self.listeningPort))
		self.trackerSock.listen()
		print(f"Listening at {self.ip},{self.listeningPort}")

							
	"""
	Removes a client from the client list
	Requires:
		- the socket of the relevant client
	"""
	def removeClient(self, socket):
		for client in self.clients:
			if(client[3] == socket):
				self.clients.remove(client)
							
	"""
	Handle p2p input.
	Preconditions:
	- data is always non-None
	"""
	def handleP2PInput(self, data, socket):
		try:
			data = json.loads(data)
		except Exception as e:
			print(f"Encountered error {e}")
		
		flag = msg["flag"]

		#client is sending information
		if (flag == "new"):
			for client in self.clients:
				if(client[3] == socket):
					client[2] = msg["publicKey"] #sets public key to a JSON deserialization of the public key __dict__
				else:
					self.sendClientList(client[3])
		else:
			print(f"Invalid flag!")

						
	"""
	Send current client list
	Preconditions:
	- socket is connected
	"""
	def sendClientList(self, socket):
		clientInfo = {"clients": json.dumps(self.clients), "flag": "peers"}
		socket.send(clientInfo)

	"""
	Runs tracker operations and recieves/sends data to peers
	"""
	def runTracker(self):
		keepRunning = True
		while keepRunning:
			inputs = []
			for client in self.clients:
				inputs.append(client[3])
			inputs.append(self.trackerSock)
			inputs.append(sys.stdin)

			inSocks, outSocks, exceptionSocks = select.select(inputs, [], inputs)

			for socket in exceptionSocks:
				self.removeClient(socket)

			for socket in inSocks:
				# this means a client is attempting to create a new connection
				if socket is self.trackerSock:
					newConnection, address = socket.accept()
					newConnection.setblocking(0)
					self.clients.append((address[0], address[1], None, newConnection))
					print(f"Got new connection from {address}")
				# client is sending data
				elif socket is sys.stdin:
					data = socket.recv(BUFF_SIZE*1000)
					if (data == "EXIT"):
						keepRunning = False
				else:
					# read the socket
					data = socket.recv(BUFF_SIZE*1000)
					if data:
						self.handleP2PInput(data, socket)
					# No data was read from socket buffer, implies socket disconnect
					else:
						self.removeClient(socket)

		self.trackerSock.close()


if __name__ == "__main__":
	myTracker = Tracker()
	myTracker.runTracker()