
"""
client.py
Group 7: Project Music Queue
CS60 Dartmouth, Prof. Xia Zhou 

Contributors for this file:
Wendell Wu
Uhuru Hashimoto
James Fleming
Jonah Weinbaum

This class allows a user to create a new client. 
Connect to the tracker and then all the peers,
and then send and receive blocks use the block and blockchain API's
"""

import select, sys, queue
import json 
from socket import *
import rsa

BUFF_SIZE = 1024 # in Kb

class Client:
	"""
	Initialize our client object, sets our parameters, and
	opens our ports.
	"""
	def __init__(self, trackerIp, trackerPort, listenPort, mining, keyFile):
		# get our host name
		self.ip = gethostbyname(gethostname())
		print(f"Found our own ip: {self.ip}")

		# my public and private keys, first parameter is number of bits
		# might have slightly less if accurate is set to false
		if keyFile is None:
			self.publicKey, self.privateKey  = rsa.newkeys(512,accurate = False)
			print(f"Generated our own keys. PK: {self.publicKey}")
		else:
			pass # read keyfile here, TODO

		# dictionary to hold peers, mapping their
		# 4-tuple of ips, port, public key, and socket
		# if public key is None, then it's a tracker
		# if public key and port is none, then it's stdin
		# if public key is self.public_key it's listening socket
		self.peers = []
		# insert stdin into peer list
		self.peers.append((self.ip, None, None, sys.stdin))

		# The port that I advertise for peer-2-peer connections
		self.myPort = listenPort
		self.myListeningSock = None
		# set up our listening socket
		self.openListenSock()

		# a socket to talk to the tracker
		self.trackerIp = gethostbyname(trackerIp)
		self.trackerPort = trackerPort
		self.trackerSock = None
		# establish tracker connection
		self.connectTracker()

	"""
	Initialize our own listening socket.
	Takes nothing, returns nothing.
	Preconditions:
		- self.publicKey and self.ip are initialized
	Postconditions:
		- self.myListeningSock is initialized
		- self.peers contains our own listening sock
	"""
	def openListenSock(self):
		# Create a socket and start listening on it
		self.myListeningSock = socket(AF_INET, SOCK_STREAM)
		self.myListeningSock.bind((self.ip, self.myPort))
		self.myListeningSock.listen()

		#Add listening socket to list of peers
		self.peers.append((self.ip, self.myPort, self.publicKey, self.myListeningSock))
		
		# Tell user we are listening now
		print(f"Listening at {self.ip}:{self.myPort}")

	"""
	Establish connection to tracker.
	Takes nothing, returns nothing.
	Preconditions:
		- self.trackerIp and self.trackerPort are initialized.
	Postconditions:
		- self.trackerSock is connected to the tracker
		- self.peers contains the tracker sock
		- We sent our own "information" to tracker for other clients to connect.
	"""
	def connectTracker(self):
		# Attempt to make the connection
		print(f"Attempting to connect to tracker at {self.trackerIp}, {self.trackerPort}")
		self.trackerSock = socket(AF_INET, SOCK_STREAM)
		self.trackerSock.connect((self.trackerIp, self.trackerPort))

		# Add tracker socket to list of peers
		self.peers.append((self.trackerIp, self.trackerPort, None, self.trackerSock))
	
		# Tell the tracker the information other clients need to connect to it
		myInfo = {"ip": self.ip, "port": self.myPort, "publicKey": (self.publicKey.n, self.publicKey.e), "flag": "new"}
		myInfoInJson = (json.dumps(myInfo)).encode()
		self.trackerSock.send(myInfoInJson)

		print(f"Successfully connected to tracker {self.trackerIp}:{self.trackerPort}")
	
	"""
	The main while loop of our client program. Continually listen to input fd's
	using select, and act appropriately.
	Takes: nothing
	Returns: nothing
	"""
	def runClient(self):
		keepRunning = True
		
		while keepRunning:
			# construct our list of fd's to listen to. We need to do this because
			# of our choice to store peers as a list of 4-tuples, with the socket/fd
			# being in the last slot of the tuple (index 3)
			inputs = []
			for peer in self.peers:
				inputs.append(peer[3])

			inSocks, outSocks, exceptionSocks = select.select(inputs, [], inputs)

			# Socket has error (disconnected) TODO: check if socket disconnect causes error or empty read. TODO: pretty sure it's an empty read/Null
			for socket in exceptionSocks:
				self.removePeer(socket)

			# take care of sockets with data to read
			for socket in inSocks:
				# A new peer is trying to connect with us, we should accept them
				# (they will send public key later)
				if (socket is self.myListeningSock):
					newConnection, address = socket.accept()
					self.peers.append((address[0], address[1], None, newConnection))
					print(f"Got new connection from peer: {address}")

				# User is sending from stdin
				elif (socket is sys.stdin):
					data = sys.stdin.readline().strip()
					if (data == "EXIT"):
						keepRunning = False
				# tracker is sending data
				elif (socket is self.trackerSock):
					pass
				#peer is sending data
				else:
					# read the socket
					data = socket.recv(BUFF_SIZE*1000)
					if data:
						self.handleP2PInput(data, socket)
					# No data was read from socket buffer, implies socket disconnect
					else:
						self.removePeer(socket)
						
	"""
	Handle p2p input.
	Preconditions:
	- data is always non-None
	"""
	def handleP2PInput(self, data, socket): 
		# load the data into a json object
		data = json.loads(data)
		# see what kind of data we are receiving
		flag = data["flag"]

		if flag == "peers":
			self.connectToPeers(data["clients"])
		else:
			print(f"Invalid flag!")


	"""
	Given a list of peers from the tracker,
	attempt to establish tcp connections to all of them if they
	are not already in our peer list.
	
	"""
	def connectToPeers(self, clientList):
		seen = False

		for client in clientList:
			for peer in self.peers:
				#client has been seen before
				if client[0] == peers[0]:
					seen = True
					break
			if not seen:
				newSock = socket(AF_INET, SOCK_STREAM) 
				newSock.connect((client[0], client[1]))
				self.peers.append(client[0], client[1], client[2], newSock)
			

	'''
		Removes a peer from list of peers. Either the peer was

		parameters:
			socket - socket of the peer which is disconnected
	'''
	def removePeer(self, socket):
		peername = socket.getpeername()
		self.peers.pop(peername, None)

		try:
			self.inputs.remove(socket)
			self.outputs.remove(socket)
		except Exception as e:
			print(f"Encountered error {e}")


	
	def sendToPeers(self, JSONData):
		for peer in self.peers:
			if peer[3] != self.trackerSock and peer[3] != sys.stdin and peer[3] != self.myListeningSock:
				# Has a header, the jsonData one wants to send and an "EOF" symbol which I have been using ';' for 
				try:
					peer.send(bytes(JSONData, 'utf-8'))
				except:
					# Not good to send to a broken pipe!
					print("Tried Sending to a bad place, removing socket")
					self.remove_Socket(peer)

	
	# uses Block Api to first mine, and then attempt to send a block to be included in the block chain
	def sendBlock(self):
		# if i receive a block during my attempt to mine and send a block what happens? 
		# do i give up on sending that block and just try to send another block? I mean i have to stop mining right? cause now what im hashing on
		# specifically "last hash" has changed. So do i just keep trying to get my message out over and over again until finally I get lucky enough and mine before anyone else. 
		# What if the proper Nonce value for the block I want to send is just super large? Then isnt linearly mining improper as it will always take longer to mine than a shorter Nonce ? but randoming mining would maybe check values multiple times and take much longer

		pass

	def receiveBlock(self):
		# this gets really tricky i think? Do we immediately assume its correct and then discard if we later see a longer fork?
		# how does a fork actually work? multiple blocks point the the same block as a 'previous' 
		# When do we discard 
		pass 

	def displayBlockChain(self):
		# I'm not sure how actual implementations of block chain / bitcoin tally the entire ledger / blockchain. Im pretty sure they use clever data stuctures / or just someone keeps track of their balance from the get-go 
		# but we need some way of displaying the entire block chain data... Maybe we only need to iterate over blocks we haven't iterated over and always keep track of the last block number that we have already tallied. 
		pass 

	# Generate private and public key pair so that we can sign our transactions and verify them... However maybe not necessary for the scope of the assignment
	def generateKeys():
		# most likely would just use an existing API for this 
		#  https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html
		pass
	
if __name__ == "__main__":
	# parse command line args
	trackerIp = sys.argv[1]
	trackerPort = int(sys.argv[2])
	listenPort = int(sys.argv[3])
	# true if it is not passed, otherwise, T or F
	mining = sys.argv[4] == "T" if (len(sys.argv) >= 5) else True
	# only assigned if it is passed
	keyFile = sys.argv[5] if (len(sys.argv) >= 6) else None

	# initialize Client object with these arguments
	myClient = Client(trackerIp, trackerPort, listenPort, mining, keyFile)

	# go into our client's main while loop
	myClient.runClient()
