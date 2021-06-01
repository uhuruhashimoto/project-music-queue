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
from  voting.poll import Poll

BUFF_SIZE = 1024 # in Kb

# Port number that we open and wait for connections from clients
class Tracker:
	"""
	Construct the tracker object. Tracker keeps track of the list of
	clients for now. TODO: handle voting/blockchain stuff
	"""
	def __init__(self, listeningPort, hashPadding):
		self.listeningPort = listeningPort
		self.hashPadding = hashPadding

		self.blockchain = None

		# A list of all clients which sent to new clients
		# 4-tuple of ips, port, public key, and socket
		self.clients = []
		
		# get our own IP
		self.ip = gethostbyname(gethostname())
		print(f"Found our own ip: {self.ip}")
		
		# our listening socket
		self.trackerSock = None

		# Open Tracker listening Socket
		self.openListenSocket()

	'''
	Opens self.trackersock as a listening socket
	'''
	def openListenSocket(self):
		# Create a socket and start listening on it
		self.trackerSock = socket(AF_INET, SOCK_STREAM)
		
		self.trackerSock.bind((self.ip, self.listeningPort))
		self.trackerSock.listen()
		print(f"Listening at {self.ip}:{self.listeningPort}")

	"""
	Runs tracker operations and receives/sends data to peers
	"""
	def runTracker(self):
		keepRunning = True
		while keepRunning:
			# build our list of sources to listen to
			inputs = []
			for client in self.clients:
				inputs.append(client[3])
			inputs.append(self.trackerSock)
			inputs.append(sys.stdin)

			inSocks, outSocks, exceptionSocks = select.select(inputs, [], inputs)

			for socket in exceptionSocks:
				print(f"Socket {socket} had error. Removing...")
				self.removeClient(socket)

			# handle input sockets
			for socket in inSocks:
				if socket is sys.stdin:
					data = sys.stdin.readline().strip()
					if (data == "EXIT"):
						keepRunning = False
					else:
						# Send a poll, for now just assume whatever we read was name of poll
						# new poll
						newPoll = Poll(data)
						jsonOut = json.dumps({"poll": newPoll.serialize(), "flag":"poll"})
						for client in self.clients:
							client[3].send(jsonOut.encode())
				else:
					self.readSocket(socket)

		# close our listening sock when we're done
		self.trackerSock.close()

	"""
	Check a socket for different possible scenarios. Handles new connections,
	user input from stdin, tracker data, peer data, and disconnects.
	"""
	def readSocket(self, socket):
		# this means a client is attempting to create a new connection
		if socket is self.trackerSock:
			newConnection, address = socket.accept()
			newConnection.setblocking(0)
			self.clients.append((address[0], None, None, newConnection))
			print(f"Got new connection from {address}")
		# client is sending data
		else:
			# read the socket
			data = socket.recv(BUFF_SIZE*1000)
			if data:
				self.handleP2PInput(data, socket)
			# No data was read from socket buffer, implies socket disconnect
			else:
				self.removeClient(socket)

	"""
	Removes a client from the client list
	Requires:
		- the socket of the relevant client
	"""
	def removeClient(self, socket):
		for client in self.clients:
			if(client[3] == socket):
				self.clients.remove(client)
				print(f"Removed client {(client[0], client[1])}")
				
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
		
		flag = data["flag"]

		# client is sending information
		if (flag == "new"):
			# linear search for the client that sent this
			for client in self.clients:
				# if we match the target socket
				if(client[3] == socket):
					self.clients.remove(client)
					# sets public key to a JSON deserialization of the public key __dict__
					self.clients.append((client[0], int(data["port"]), data["publicKey"], client[3]))
					self.sendClientList(client[3])
					break

		else:
			print(f"Invalid flag!")

	"""
	Send current client list
	Preconditions:
	- socket is connected
	"""
	def sendClientList(self, socket):
		out = []
		for client in self.clients:
			out.append((client[0], client[1], client[2]))
		clientInfo = json.dumps({"clients": json.dumps(out), "pad": self.hashPadding, "flag": "welcome"})
		socket.send(clientInfo.encode())


if __name__ == "__main__":
	# parse command line arguments
	listenPort = int(sys.argv[1])
	hashPadding = int(sys.argv[2]) if len(sys.argv) >= 3 else 50
	
	# initialize Tracker object with these arguments
	myTracker = Tracker(listenPort, hashPadding)

	# go into the tracker's main while loop
	myTracker.runTracker()