
"""
Client.py
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
import rsa

class Client:
    def __init__(self):
        # get our host name 
        self.ip = gethostbyname(gethostname())
       
    
        # dictionary to hold peers, their public keys and port numbers 
        self.peers = {}

        # Our incoming sockets / files
        self.inputs = [sys.stdin]
        # Our outgoing sockets 
        self.outputs = []

        # The port that I advertise 
        self.myPort = int(input("Port to open On"))
        self.tracker_sock = None
        self.myListeningSock = None
        self.Open()
        
        
        # my public and private keys,, first parameter is number of bits , might have slightly less if accurate is set to false
        self.publicKey, self.privateKey  = rsa.newkeys(512,accurate = False)
        self.pk = (self.publicKey.n, self.publicKey.e)

        


        
    def remove_Socket(self,socket):
        peername = socket.getpeername()
        self.peers.pop(peername, None)

        try:
            self.inputs.remove(socket)
        except:
            pass
        try:
            self.outputs.remove(socket)
        except:
            pass


        
    def Open(self):
        # Create a socket and start listening on it
        self.myListeningSock = socket(AF_INET, SOCK_STREAM)
        
        self.myListeningSock.bind((self.ip, self.myPort))
        self.myListeningSock.listen()
        self.inputs.append(self.myListeningSock)
        
        print(f"Listening at {self.ip},{self.myPort}")
    
    # create a TCP connection with someone else
    def connectTo(self, Address, Port, isTracker =False):
        newSock = socket(AF_INET, SOCK_STREAM)
        
        try:
            newSock.connect((Address, Port))
        

        # add this socket to our inputs and outputs as we can both read from it and write to it. 
            

            if isTracker:
                self.inputs.append(newSock)
                self.outputs.append(newSock)
                self.tracker_sock = newSock
        
        # Tell the tracker the information other clients need to connect to it 
                myInfo = {"port": self.myPort, "publicKey":self.pk}
            
            else:
                newSock.setblocking(0)
                myInfo = (self.pk)
            myInfoInJson = json.dumps(myInfo, indent = None)
        # So we send a message with a "NEW" flag header and then the relevant information 
            newSock.send(bytes(f"NEW:{myInfoInJson}", 'utf-8'))
        except:
            print(f"Error trying to connect to {Address}, {Port}")




        


    # given a list of peers from the tracker, store their public key and open a TCP connection
    def connectToPeers(self, dictionary):
        
        
        for peer in dictionary:
            # elf.clients[peername[0]] = (msg["port"], msg["publicKey"])
            # Store the peer to this peer's publicKey 
            value = dictionary[peer]
            
            if (value[2] == self.ip and int(value[0]) == self.myPort):
                pass
                # Don't connect to yourself 
            else:
                self.peers[peer] = rsa.PublicKey(value[1][0], value[1][1])
                print(f"Connecting to {value[2]}, {int(value[0])}")
                self.connectTo(value[2], int(value[0]))
            # Create a connection with this peer 

        

   

    def runClient(self):
        buffer= {}
        while True:
            inputs, outputs, exceptional = select.select(self.inputs, self.outputs, self.inputs)
            for socket in exceptional: 
                self.remove_Socket(socket)
            for socket in inputs:
                # A new peer is trying to connect with us, we should accept them 
                if (socket is self.myListeningSock):
                    newConnection, address = socket.accept()
                    newConnection.setblocking(0)
                    self.inputs.append(newConnection)
                    self.outputs.append(newConnection)
                    print(f"Got new connection from {address}")
                # This socket is the tracker
                else:
                    
                        # Okay the issue here is that we only read in a fixed size, but if the message is longer than this size everything breaks. 
                    data = socket.recv(4096)
                    

                    if data: 
                        shouldSend = False
                            # Figure out where this message came from 
                        peername = socket.getpeername()
                        
                        # break the message into its header flag 
                        newPiece= data.decode('utf-8')
                        
                        try:
                            if (buffer[socket]):

                                data = buffer[socket] + newPiece
                                #print(data+ '\n')
                            
                        except:
                            buffer[socket] = newPiece
                            data = newPiece
                        
                        flag = data[0:3]
                        # and the actual JSON data
                        msg = data[4:len(data)-1]
                        # parse json into python dictionary
                        try:
                            if data[len(data)-1] == ';':
                                
                                msg = json.loads(msg)
                                shouldSend = True
                                #buffer[socket] = None
                            else:
                                
                            
                                if buffer[socket]:
                                    buffer[socket] = data
                                else:
                                    buffer[socket] = data

                            

                        except:
                            
                            print("Was not properlly formatted to be converted from JSON")
                        if (shouldSend):
                        # We got a message from the tracker
                            if (socket == self.tracker_sock):
                                if (flag == "ADD"):
                                    print("Received A list Of Peers")
                                    self.connectToPeers(msg)
                            else:
                                if (flag == "NEW"):
                                    # A fellow peer is telling us that they have connected and this is their publicKey
                                    self.peers[peername[0]] = rsa.PublicKey(msg[0], msg[1])
                    
                        




                            
                
            for socket in outputs:
                pass
            
               
        # run the actually client logic





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
    myClient = Client()
    tracker_ip = input("Tracker IP: ")
    tracker_port = int(input("Tracker Port: "))
    myClient.connectTo(tracker_ip, tracker_port, True)
    myClient.runClient()
