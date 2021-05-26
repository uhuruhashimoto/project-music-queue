"""
client.py
Group 7: Project Music Queue
CS60 Dartmouth, Prof. Xia Zhou 

Contributors for this file:
Wendell Wu
Uhuru Hashimoto
James Fleming

Connect to the tracker and then all the peer
and send and receive blocks use the block and blockchain API's
"""

# -------- HELPER FUNCTIONS --------

# uses Block Api to first mine, and then attempt to send a block to be included in the block chain
def sendBlock():
	# if i receive a block during my attempt to mine and send a block what happens? 
	# do i give up on sending that block and just try to send another block? I mean i have to stop mining right? cause now what im hashing on
	# specifically "last hash" has changed. So do i just keep trying to get my message out over and over again until finally I get lucky enough and mine before anyone else. 
	# What if the proper Nonce value for the block I want to send is just super large? Then isnt linearly mining improper as it will always take longer to mine than a shorter Nonce ? but randoming mining would maybe check values multiple times and take much longer
	pass
def receiveBlock():
	# this gets really tricky i think? Do we immediately assume its correct and then discard if we later see a longer fork?
	# how does a fork actually work? multiple blocks point the the same block as a 'previous' 
	# When do we discard 
	pass 

def displayBlockChain():
	# I'm not sure how actual implementations of block chain / bitcoin tally the entire ledger / blockchain. Im pretty sure they use clever data stuctures / or just someone keeps track of their balance from the get-go 
	# but we need some way of displaying the entire block chain data... Maybe we only need to iterate over blocks we haven't iterated over and always keep track of the last block number that we have already tallied. 

	pass 


# Generate private and public key pair so that we can sign our transactions and verify them... However maybe not necessary for the scope of the assignment
def generateKeys():
	# most likely would just use an existing API for this 
	#  https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html
	pass

### Below here is the main entry point for our code, organized roughly in
### the style of C programs

import socket # for socket connections
import select # for select()/async stuff
import sys # for system i/o

# Global data we will need to pass between threads
blockchain = None
blockchain_updated = False # track if we can stop mining the current block
mining = False
key_file = ""
tracker_ip = ""
tracker_port = ""
tracker_sock = None # socket for the tracker
host_ip = socket.gethostbyname(socket.gethostname())
peers = {} # a dictionary to hold public ip -> public key mappings

# the entry point for the client program
if __name__ == "__main__":
	# parse command line args
	tracker_ip = sys.argv[1]
	tracker_port = int(sys.argv[2])
	mining = sys.argv[3] == "T"
	key_file = sys.argv[4]
	
	# make contact with the tracker, get the list of clients in the network
	tracker_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tracker_sock.connect((tracker_ip, tracker_port))

	# establish connections with all peers given in the list, a tcp socket for each
	# TODO

	# our main while loop to handle user inputs, listen for other clients
	# and listen for tracker updates
	# TODO

	# close out our sockets when we're finished up
	tracker_sock.close()