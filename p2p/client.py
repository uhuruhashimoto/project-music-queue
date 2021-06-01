"""
client.py
Group 7: Project Music Queue
CS60 Dartmouth, Prof. Xia Zhou 

Contributors for this file:
Wendell Wu
Uhuru Hashimoto
James Fleming
Jonah Weinbaum
Thomas White

This class allows a user to create a new client. 
Connect to the tracker and then all the peers,
and then send and receive blocks use the block and blockchain API's
"""

import select, sys, queue
import json 
import blockchain.block
import blockchain.entry
from  voting.poll import Poll
from socket import *
import rsa
import time
import threading
import hashlib

BUFF_SIZE = 1024 # in Kb
TIMEOUT = 60*60 #arbitrarily large mining timeout

class Client:
	"""
	Initialize our client object, sets our parameters, and
	opens our ports.
	"""
	def __init__(self, trackerIp, trackerPort, listenPort, mining, timeToMine, keyFile):
		self.blockchain = None

		# padding required for valid block
		self.hash_padding = 0
		
		# poll information for the current cycle
		self.poll_id = None
		self.poll = None

		# get our host name
		self.ip = gethostbyname(gethostname())
		print(f"Found our own ip: {self.ip}")

		# my public and private keys, first parameter is number of bits
		# might have slightly less if accurate is set to false
		if keyFile is None:
			self.publicKey, self.privateKey  = rsa.newkeys(512,accurate = False)
			self.pk = (self.publicKey.n, self.publicKey.e)
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


		# Mining Specific variables
		self.timeToMine = timeToMine
		# entries that we are gonna build a block on if we are a miner
		self.entries = {}
		# 
		self.killMine = False
		self.miningResult = None

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

			# Socket has an error, assume it disconnected.
			for socket in exceptionSocks:
				print(f"Socket {socket} had error. Removing...")
				self.removePeer(socket)

			# take care of sockets with data to read
			for socket in inSocks:
				self.readSocket(socket)
	
	"""
	Check a socket for different possible scenarios. Handles new connections,
	user input from stdin, tracker data, peer data, and disconnects.
	"""
	def readSocket(self, socket):
		# A new peer is trying to connect with us, we should accept them
		# (they will send public key later)
		if (socket is self.myListeningSock):
			newConnection, address = socket.accept()
			self.peers.append((address[0], address[1], None, newConnection))
			print(f"Got new connection from peer: {address}")

		# User is sending from stdin
		elif socket is sys.stdin:
			data = sys.stdin.readline().strip()
			if (data == "EXIT"):
				keepRunning = False
			elif (data == "Y" or data == "N"):
				self.sendVote(data)
			else:
				print("Did not understand input. Please try again.")
				
		# tracker is sending data
		elif (socket is self.trackerSock):
			print(f"Received new tracker message.")
			pass # TODO: parse tally message once received
		#peer is sending data
		else:
			# read the socket
			data = socket.recv(BUFF_SIZE*1000)
			print(f"Received new peer message.")
			if data:
				self.handleP2PInput(data, socket)
			# No data was read from socket buffer, implies socket disconnect
			else:
				self.removePeer(socket)

	"""
	Mines a block 
	"""
	def mine(self, block):
		print("Starting to Mine!")
		is_mined = False

		pref = '0'*self.hash_padding #string for leading zeros

		#start time
		t = time.time()

		# serialize data to json string
		txt = block.serialize().encode('utf-8')

		while not is_mined and self.shouldMine:
			# compute hash val -- must always match block.py
			hash_val = hashlib.sha256(txt).hexdigest()

			# check the block prefix for necessary number of 0s
			if hash_val.startswith(pref):
				is_mined = True
			
			if (time.time()-t) > TIMEOUT:
				raise BaseException(f'Mining timeout')
			
			# increment nonce
			block.nonce = block.nonce + 1
			
		# Send this block to everyone we know and
		# update our own blockchain with this new block
		self.blockchain.add_block(block)

		sendblock = {"flag": "block", "block": block.serialize(), "length": self.blockchain.length}
		self.sendToPeers(sendblock)
		


	"""
	This thread is kicked off (when? under what conditions?)
	It first waits self.timeToMine seconds, then kicks off a mining
	thread.
	"""
	def timerThread(self):
		print("Starting a timer. Once it completes we will mine!")
		time.sleep(self.timeToMine)
		self.killMine = False
		
		# Fill the block object and start the mine thread
		block = blockchain.block.Block(self.entries, self.public_key, self.blockchain.head.sha256())
		block.sign(self.private_key)
		
		t1 = threading.Thread(self.mine, (block, self.hash_padding, not self.killMine), daemon=True)
		t1.start()
		
		
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

		if flag == "welcome":
			print("Welcome info recieved")
			self.connectToPeers(data["clients"])
			self.hash_padding = data["pad"]
		elif flag == "blockchain":
			print("Blockchain recieved")
			self.updateBlockchain(data["chain"])
		elif flag == "block":
			print("Block recieved")
			self.recieveBlock(data["block"], data["length"])
		elif flag == "entry" and self.mining:
			print("Entry recieved")
			self.recieveEntry(data["entry"])
		elif flag == "poll":
			print("Poll recieved")
			self.recievePoll(data["poll"])
		else:
			print(f"Invalid flag!")

	

	"""
	Given a list of peers from the tracker,
	attempt to establish tcp connections to all of them if they
	are not already in our peer list.
	"""
	def connectToPeers(self, clientList):
		for client in clientList:
			if client[0] != self.ip:
				newSock = socket(AF_INET, SOCK_STREAM) 
				newSock.connect((client[0], client[1]))
				self.peers.append(client[0], client[1], client[2], newSock)
				print(f"Added peer {client[0]}:{client[1]}")
				blockchain_update = {"flag": "update"}
				newSock.send(blockchain_update)

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
					print("Tried sending to a bad place, removing socket")
					self.remove_Socket(peer)

	# Receives an entire blockchain. Sets it to our blockchain if valid 
	def updateBlockchain(self, jsonin):
		inchain = blockchain.deserialize(jsonin)
		if self.blockchain.length < inchain.length and inchain.verify(self.hash_padding):
			self.blockchain = inchain

	def askBlockchain(self):
		update_msg = {"flag": "update"}
		self.sends(update_msg)

	# Prints the block chain to the command line
	def displayBlockChain(self):
		ptr = self.blockchain.head
		
		while ptr is not None:
			for entry in ptr.entries:
				print(f"{entry.public_key} voted {entry.vote} for {entry.poll_id}")
			ptr = ptr.block_prev

	# Recieves a block. Decide whether or not to add to our current blockchain. 
	def receiveBlock(self, block, length):
		inblock = block.deserialize(block)
		if inblock.verify():
			# We need to check its length
			if (length == (self.blockchain.length + 1)) and \
					(inblock.hash_prev == self.blockchain.head.sha256()):
				self.blockchain.add_block(inblock)
				self.killMine = True
				# Remove any entries in this new block from our entries pool
				print("Successfuly Added a new Block to our blockchain")
				
			elif length > self.blockchain.length + 1:
				self.askBlockchain()
				# Wipe our entries pool and stop mining
				self.killMine = True
				self.entries = {}
			else:  # ignore any block that is part of a shorter block
				pass

	def recieveEntry(self, jsonin):
			
			# Receive the entry
			recievedEntry = blockchain.entry.deserialize(jsonin)
			# Update the entries dictionary to point from the unique id to the entry itself
			if recievedEntry.verify():
				self.entries[recievedEntry.getID()] = recievedEntry
				print("Received a valid entry")
				# first entry we have receieved
				if len(self.entries.keys()) == 1:
					# kick off the timer thread
					
					t2 = threading.Thread(self.timerThread)
					t2.start()	
				
	def recievePoll(self, jsonin):
		poll = Poll.deserialize(jsonin)
		
		# Store the poll for display.
		self.poll = poll
		self.poll_id = poll.poll_id

		print(f"A poll has started. We are voting on {poll.song}. Vote 'Y/N'.")

	"""
	Send a vote inputted by the user for the current poll
	to the network.
	 - data should be a string of either "Y" or "N"
	"""
	def sendVote(self, data):
		# make an entry object
		newEntry = blockchain.entry.Entry(self.poll_id, data, self.pk)
		jsonout = json.dumps({"entry": blockchain.entry.serialize(newEntry), "flag": "entry"})
		# send it out 
		self.sendToPeers(jsonout)

if __name__ == "__main__":
	# parse command line args
	trackerIp = sys.argv[1]
	trackerPort = int(sys.argv[2])
	listenPort = int(sys.argv[3])
	# true if it is not passed, otherwise, T or F
	mining = sys.argv[4] == "T" if (len(sys.argv) >= 5) else True
	# If mining is true, set the time to mine here
	miningTime = int(sys.argv[5]) if (len(sys.argv) >= 6) else 30
	# only assigned if it is passed
	keyFile = sys.argv[6] if (len(sys.argv) >= 7) else None

	# initialize Client object with these arguments
	myClient = Client(trackerIp, trackerPort, listenPort, mining, miningTime, keyFile)

	# go into our client's main while loop
	myClient.runClient()

	print(f"Exiting client program...")