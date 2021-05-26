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

# Port number that we open and wait for connections from clients
class Tracker:
    def __init__(self):
        self.listeningPort = 60005

        # A dictionary of all clients relating them by ip address  to their ( public key , listening port number)
        # Will sent to a new clients when a new client joins
        self.clients = {}
        self.inputs =[]
        self.outputs = []
        
        self.ip = gethostbyname(gethostname())
        
        
        

        self.tracker_sock = None
        # Call Open
        self.Open()
        
    

    def Open(self):
        # Create a socket and start listening on it
        self.tracker_sock = socket(AF_INET, SOCK_STREAM)
        
        self.tracker_sock.bind((self.ip, self.listeningPort))
        self.tracker_sock.listen()
        self.inputs.append(self.tracker_sock)
        print(f"Listening at {self.ip},{self.listeningPort}")
        
    # accepts a newClient. Tells all other clients to open a connection to this new client
    # adds the newClient to the client list
    def acceptNewClient():
        # most likely call "broadCastNewClient"
        pass


    # once a client signifies they are leaving we must tell everybody else 
    # remove client from 'clients'
    def removeClient():
        pass

    #tell all other clients they need to make a TCP connection with the new client 
    def broadCastNewClient():
        pass 
    
    def sendClientList(self, socket):
        jsonClients = json.dumps(self.clients, indent = None)
        # Send the entire dictionary in jsonForm with a "ADD" header 
        socket.send(bytes(f"ADD:{jsonClients};", 'utf-8'))

    def runTracker(self):
        while True:
            inputs, outputs, exceptional = select.select(self.inputs, self.outputs, self.inputs)
            for socket in inputs:
                # this means a client is attempting to create a new connection
                if socket is self.tracker_sock:
                    newConnection, address = socket.accept()
                    newConnection.setblocking(0)
                    self.inputs.append(newConnection)
                    self.outputs.append(newConnection)
                    print(f"Got new connection from {address}")
                else:
                    
                    data = socket.recv(4096)
                    if data:
                        # Figure out where this message came from 
                        peername = socket.getpeername()
                        # break the message into its header flag 
                        data = data.decode('utf-8')
                        flag = data[0:3]
                        # and the actual JSON data
                        msg = data[4:]
                        # parse json into python dictionary
                        try:
                            msg = json.loads(msg)
                        except:
                            print("Was not properlly formatted to be converted to JSON")
                        
                        
                        if(flag == "NEW"):
                            # Before we add this client, Send this client the list of all other clients they need to connect to
                            if (self.clients):
                                self.sendClientList(socket)
                            # A client has recently connected. Store their relevant information as a tuple
                            p = msg["port"]
                            # This code can actually occur during the sending of the list 
                            self.clients[f"{p}:{peername[0]}"] = (msg["port"], msg["publicKey"], peername[0])



        


            for socket in outputs:
                pass
            for socket in exceptional:
                print("Removing exceptional")
                ip = (socket.getpeername())[0]
                try:
                    self.clients.pop(ip)
                except:
                    print("client to remove not found")

                try:
                    self.inputs.remove(socket)
                except:
                    pass
                try:
                    self.outputs.remove(socket)
                except:
                    pass
                print(self.clients)

        self.tracker_sock.close()



if __name__ == "__main__":
    myTracker = Tracker()
    myTracker.runTracker()








