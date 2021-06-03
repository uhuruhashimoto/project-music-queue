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

import argparse
import copy
import select, sys, queue
import json 
import blockchain.block
import blockchain.entry
import blockchain.blockchain
import bitstring
import voting.poll
from  voting.poll import Poll
from socket import *
import rsa
import time
import random
import threading
import hashlib

BUFF_SIZE = 1024 # in Kb
MINING_TIMEOUT = 60 # mining timeout; in minutes

class Client:
	"""
	Initialize our client object, sets our parameters, and
	opens our ports.
	"""
	def __init__(self, trackerIp, trackerPort, listenPort, mining, timeToWait, keyPaths):
		# Start us off with an initial Blockchain that we can add to . We will also call for all clients to update us with theirs
		self.blockchain = blockchain.blockchain.Blockchain()

		# padding required for valid block
		self.hash_padding = 0
		
		# poll information for the current cycle
		self.poll_id = None
		self.poll = None
		
		self.mining = mining

		# get our host name
		self.ip = gethostbyname(gethostname())
	
		if keyPaths:
			try:
				with open(keyPaths[0], 'rb') as keyFile:
					keyData = keyFile.read()
				self.publicKey = rsa.PublicKey.load_pkcs1(keyData)

				with open(keyPaths[1], 'rb') as keyFile:
					keyData = keyFile.read()
				self.privateKey = rsa.PrivateKey.load_pkcs1(keyData)
				print(f'Loaded keys from file. PK: \n{self.publicKey}')
			except Exception as e:
				print(f'Error encountered while attempting to load keys from file')
				raise e
		else:
			# might have slightly less if accurate is set to false
			self.publicKey, self.privateKey  = rsa.newkeys(nbits=512,accurate = False)
			self.pk = (self.publicKey.n, self.publicKey.e)
			print(f"Generated our own keys. PK: {self.publicKey}")

		# dictionary to hold peers, mapping their
		# 4-tuple of ips, port, public key, and socket
		# if public key is None, then it's a tracker
		# if public key and port is none, then it's stdin
		# if public key is self.public_key it's listening socket
		self.peers = []
		# insert stdin into peer list
		self.peers.append((self.ip, None, None, sys.stdin))

		# The port"" that I advertise for peer-2-peer connections
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
		self.timeToWait = timeToWait
		# entries that we are gonna build a block on if we are a miner
		self.entries = {}
		# set defaults
		self.killMine = False
		self.miningResult = None
		self.preparingToMine = False

		# boolean for exiting the program
		self.keepRunning = True

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
		self.myListeningSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
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
		# kick off the timer thread, which keeps track of mining business
		if self.mining:
			t2 = threading.Thread(target=self.timerThread, daemon=True)
			t2.start()

		self.keepRunning = True
		while self.keepRunning:
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
		if socket is self.myListeningSock:
			newConnection, address = socket.accept()
			self.peers.append((address[0], address[1], None, newConnection))
			print(f"Got new connection from peer: {address}")

		# User is sending from stdin
		elif socket is sys.stdin:
			data = sys.stdin.readline().strip()
			if (data == "EXIT"):
				self.keepRunning = False
			elif (data == "Y" or data == "N"):
				self.sendVote(data)
			elif(data =="PRINT"):
				# User is asking to see the current block chain!
				self.displayBlockChain()
			elif (data == "TALLY"):
				if self.poll:
					self.blockchain.tally(self.poll)
				else:
					print("No running poll to tally")
			else:
				print("Did not understand input. Please try again.")
				
		# tracker is sending data
		elif (socket is self.trackerSock):
				# read the socket
			data = socket.recv(BUFF_SIZE*1000)
			if data:
				#print(f"Received new tracker message.")
				self.handleP2PInput(data, socket)
			# No data was read from socket buffer, implies socket disconnect
			else:
				print(f"Tracker went down!")
				exit(1)
	
		#peer is sending data
		else:
			# read the socket
			data = None
			try:
				data = socket.recv(BUFF_SIZE*1000)
			except:
				self.removePeer(socket)
			#print(f"Received new peer message.")
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
		#start time
		t = time.time()

		while not is_mined and not self.killMine:
			block.hash_prev = self.blockchain.head.sha256()

			# check the block prefix for necessary number of 0
			is_mined = block.verify(self.blockchain.head, self.hash_padding)
			
			if (time.time()-t) > MINING_TIMEOUT*60:
				raise BaseException(f'Mining timeout')
			
			# increment nonce
			block.nonce = random.getrandbits(64)
			
		# Send this block to everyone we know and
		# update our own blockchain with this new block
		if (not self.killMine):
			print("Mined a block! Adding it to blockchain")
			print("Stopped mining!")
			self.blockchain.add_block(block)
			self.removeFromEntryPool(block.entries)
			sendblock = json.dumps({"flag": "block", "block": block.serialize(), "length": self.blockchain.length})
			self.sendToPeers(sendblock)
		else:
			print("Stopped mining!")
		
	"""
	This thread is kicked off once, and functions on a set-interval cycle.
	It first waits self.timeToWait seconds, then kicks off a mining
	thread.
	"""
	def timerThread(self):
		i = 1
		while True:
			time.sleep(self.timeToWait)
			# if self.entries is not empty
			if len(self.entries):
				print(f"Mine timer hit, mining block {i}")
				self.killMine = False
				# Fill the block object and start the mine thread
				block = blockchain.block.Block(copy.deepcopy(list(self.entries.values())), self.pk, self.blockchain.head.sha256())
				block.sign(self.privateKey)
				
				self.mine(block)
				i += 1
			else:
				print(f"No entries to add. Not mining.")
		
	"""
	Handle p2p input
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
			self.receivePoll(data["poll"])
			self.updateBlockchain(data["chain"])
		elif flag == "block":
			print("Block recieved")
			self.receiveBlock(data["block"], data["length"])
		elif flag == "entry":
			if self.mining:
				print("Entry recieved")
				self.receiveEntry(data["entry"])
		elif flag == "poll":
			if data["poll"] is not None:
				print("Poll recieved")
			
			self.receivePoll(data["poll"])
		elif flag == "update":
			if self.poll is not None:
				toSend = json.dumps({"flag": "blockchain",\
					"chain": self.blockchain.serialize(),\
					"poll": self.poll.serialize()})\
						.encode()
			else:
				toSend = json.dumps({"flag": "blockchain",\
					"chain": self.blockchain.serialize(),\
					"poll": None})\
						.encode()
			print("Sent blockchain update to peer")
			socket.send(toSend)
		else:
			print(f"Invalid flag: {flag}")

	"""
	Given a list of peers from the tracker,
	attempt to establish tcp connections to all of them if they
	are not already in our peer list.
	"""
	def connectToPeers(self, clientList):
		clientList = json.loads(clientList)
		for client in clientList:
			if client[0] != self.ip:
				print(f"Attempting connection to {client[0]}:{client[1]}")
				newSock = socket(AF_INET, SOCK_STREAM) 
				newSock.connect((client[0], client[1]))
				self.peers.append((client[0], client[1], client[2], newSock))
				print(f"Added peer {client[0]}:{client[1]}")
		self.askBlockchain()

	"""
	Removes a peer from list of peers. 
	parameters:
		socket - socket of the peer which is disconnected
	"""
	def removePeer(self, socket):
		for client in self.peers:
			if client[3] == socket:
				self.peers.remove(client)
				print(f"Removed peer: {client[0]}:{client[1]}")
				break

	"""
	sends JSON data to peers (except for self and tracker)
	"""
	def sendToPeers(self, JSONData):
		for peer in self.peers:
			if peer[3] != self.trackerSock and peer[3] != sys.stdin and peer[3] != self.myListeningSock:
				# Has a header, the jsonData one wants to send and an "EOF" symbol which I have been using ';' for 
				try:
					peer[3].send(JSONData.encode())
				except Exception as e:
					# Not good to send to a broken pipe!
					print(f"Tried sending {JSONData} to {peer[3]}, but it failed with exception {e} so I am removing socket")
					self.removePeer(peer)

	"""
	Receives an entire blockchain. Sets it to our blockchain if valid
	"""
	def updateBlockchain(self, jsonin):
		inchain = blockchain.blockchain.deserialize(jsonin)
		if self.blockchain.length < inchain.length and inchain.verify_chain(self.hash_padding):
			self.blockchain = inchain

	"""
	Asks peers for an updated blockchain 
	"""
	def askBlockchain(self):
		print(f"Getting blockchain from peers...")
		update_msg = json.dumps({"flag": "update"})
		self.sendToPeers(update_msg)

	"""
	Prints the block chain to the command line
	"""
	def displayBlockChain(self):
		ptr = self.blockchain.head
		# Prints blocks with delineators and anonymous transactions
		while ptr is not None:
			if ptr.entries:
				for entry in ptr.entries:
							print(f"{entry.vote} vote for {self.poll.song}")
				print("----------------------------")
			else:
				print("Initial Block")
			ptr = ptr.block_prev

	"""
	Recieves a block. Decide whether or not to add to our current blockchain. 
	"""
	def receiveBlock(self, block, length):
		inblock = blockchain.block.deserialize(block)
		if inblock.verify(self.blockchain.head, self.hash_padding):
			# We need to check its length
			if (length == (self.blockchain.length + 1)):
				self.blockchain.add_block(inblock)
				self.removeFromEntryPool(inblock.entries)
				self.killMine = True

				print("Successfuly Added a new Block to our blockchain")
				
			elif length > self.blockchain.length + 1:
				# If we encounter a discrepancy (out of order block), immediately ask peers for their versions of the blockchain, and take the longest 
				# after asking, we handle the recieved blockchains in handleP2P and updateBlockchain
				self.askBlockchain()
				# Wipe our entries pool and stop mining
				self.killMine = True
				self.entries = {}
			else:  # ignore any block that is part of a shorter block
				pass
		print("Block not verified on recieve block")
	
	"""
	Recieves an entry and adds it to entry list
	"""
	def receiveEntry(self, jsonin):
			# Receive the entry
			if (self.poll_id != None):
				recievedEntry = blockchain.entry.deserialize(jsonin)
				# Update the entries dictionary to point from the unique id to the entry itself
				if recievedEntry.verify():
					self.entries[recievedEntry.getID()] = recievedEntry
					print("Received a valid entry")
			else:
				print("No Poll has been initiated, entry will be discarded")

	"""
	Recieves an poll; if not a duplicate, displays and stores it
	"""	
	def receivePoll(self, jsonin):
		if jsonin:
			self.blockchain.tally(self.poll)
			poll = voting.poll.deserialize(jsonin)
			if poll.poll_id != self.poll_id:
			# Store the poll for display.
				self.poll = poll
				self.poll_id = poll.poll_id
				print(f"A poll has started. We are voting on {poll.song}. Vote 'Y/N'.")
		else:
			self.blockchain.tally(self.poll)
			self.poll = None
			self.poll_id = None

	"""
	Send a vote inputted by the user for the current poll
	to the network.
	 - data should be a string of one character: either "Y" or "N"
	"""
	def sendVote(self, data):
		# make sure a poll has been initiated 
		if (self.poll_id != None):
			# make an entry object
			newEntry = blockchain.entry.Entry(self.poll_id, data, self.pk)
			# sign the vote
			newEntry.sign(self.privateKey)
			jsonout = json.dumps({"entry": newEntry.serialize(), "flag": "entry"})
			# send it out 
			self.sendToPeers(jsonout)
			
			if self.mining:
				self.entries[newEntry.getID()] = newEntry
		else:
			print(f"A poll is not ongoing.")

	"""
	Remove all entries from `entries` from self.entries, by
	entry ID.
	"""
	def removeFromEntryPool(self, entries):
		for entry in entries:
			try:
				if self.entries[entry.getID()].vote == entry.vote:
					del self.entries[entry.getID()]
			except:
				continue


"""
if __name__ == "__main__":
	argparser = argparse.ArgumentParser(description='Run a votechain client!', add_help=True)
	argparser.add_argument('-t', '--tracker-ip', default=None, help='set the tracker ip to use')
	argparser.add_argument('-tp', '--tracker-port', default=None, help='set the port to send data to the tracker')
	argparser.add_argument('-lp', '--listen-port', default=None, help='set the port to use for listening')
	argparser.add_argument('-tp', '--tracker-port', default=None, help='set the port to use on the tracker')
	argparser.add_argument('-m', '--mining', default='T', help='set this flag to enable mining')
	argparser.add_argument('-mt', '--mining-time', default=30, help='set the time to mine')
	argparser.add_argument('-pub', '--public-key', default=None, help='pass a path for RSA public key')
	argparser.add_argument('-priv', '--private-key', default=None, help='pass a path for RSA private key')
	args = argparser.parse_args()

	# initialize Client object with these arguments
	myClient = Client(args.tracker_ip, args.tracker_port, args.listen_port, args.mining, args.mining_time, (args.public_key, args.private_key))

	# go into our client's main while loop
	myClient.runClient()

	print(f"Exiting client program...")
"""

if __name__ == "__main__":
	# parse command line args
	trackerIp = sys.argv[1]
	trackerPort = int(sys.argv[2])
	listenPort = int(sys.argv[3])
	# true if it is not passed, otherwise, T or F
	mining = sys.argv[4] == "T" if (len(sys.argv) >= 5) else True
	# If mining is true, set the time to wait between mine sessions here
	waitingTime = int(sys.argv[5]) if (len(sys.argv) >= 6) else 30
	# only assigned if it is passed
	keyFile = sys.argv[6] if (len(sys.argv) >= 7) else None

	# initialize Client object with these arguments
	myClient = Client(trackerIp, trackerPort, listenPort, mining, waitingTime, keyFile)

	# go into our client's main while loop
	myClient.runClient()

	print(f"Exiting client program...")