# Final Project--Queued Voting via Blockchain--DESIGN.md
## Date: 5/17/21

## Rough Requirements
We are making a music voting mechanism that allows users to queue up
a specific song to be played next.

The song-player will be something (a website, program, etc.) which
serves as the tracking node as well--it keeps its own blockchain to
serve as the vote tally, and will (clear it/keep it?) for the next 


## User interface
Users of the program will type names of songs into stdin/the gui, and
at the end of each song, tallies of 


## Inputs and outputs
## Functional decomposition into modules
## Dataflow through modules
## Pseudo code (plain English-like language) for logic/algorithmic flow

A user logs onto the application by telling the tracker they have joined and what their public key is and what port they will listen for new connections on. The tracker tells them all the other users and their respective public keys and ports
Every user that joined before will have the job of opening a TCP connection with the new client. Therefore for this toy application we create an entirely connected topology with TCP connections 


We need to files to handle this P2Pclient.py and P2Ptracker.py 
P2P client can then send a message to all of the other nodes and also communicate with the tracker about leaving. 


## The Protocol (Application-Level)
What will the format of the block data look like?
What does one "vote" look like?


## The Protocol (Blockchain-Level)

## Major data structures
We are following a roughly object-oriented model.


Entry (The Ledger)
```
	//Data 

	- Public Key
  - Song Vote
  - Signature 
  
  //Functions
  
  - sign()
     {
     	 generates public key and signature of entry
     }
  - verify()
     {
     	
     }
  - write()
```

Block

 //Data

 - Block ID
 - Nonce
 - Entries (The Data)
 - Prev Hash
 
 //Functions 
 
 - hash() 
     {
     	 SHA256 hash function
     }
 - verify()
 	   {
     	 Bitshift self.hash() to isolate desired HASH_PADDING, and check 
       this is 0
     }
 - mine(Data, numOfZero) 
     {
       generate nonce values until self.verify() == TRUE
     
      
     }
 - write()
     {
     	 writes data to entries 
     }

Blockchain  (The Ledger)

	//Parameters
  HASH_PADDING - # of zeros for valid hash

	//Data
  

 	//Functions
  - tally()
    {
    	looks through blockchain and tallies votes 
    }


## Application
Clients will be in the form of a compiled Python program. We could consider a browser-based solution (which would allow for an easy demo in real time), but this
would require either JavaScript or some careful handling of different APIs (brython, WASM, etc.) to allow us to run mining code originally written in C on 
the client. A downloadable webapp which the user runs manually would be better. The client should display the currently playing music and the queue, as well as
any previous blockchain transactions (votes) by the client.

Nodes/peers will consist of 3+ nodes running on the Thayer servers. These nodes will allow for votes to be submitted. One possible structure would be to have a
webpage which allows for submission of votes to a vote pool. The nodes themselves will package votes from the pool into a block and mine to try to submit them.

Tracker will be in the form of a webapp set up using (Django? Flask? Tornado? I (tommy) would lean toward using Flask). Should allow for setting up of clients.
Should display information about voting tallies, visualization, and the music queue (as well as playing the music). 


Questions?
What happens if there is only 1 user? or all users leave? Then the ledger disinegrates ? 
Do we need external miners? Or do we just make it so that each client mines their own block and broadcasts that?
Is the entire topolgy connected in real life applications like BitCoin? 

How does a client that joins get a the blockchain. From multiple users and compares any discrepancies?  From a single user and just hopes it is correct? 
How do we deal with forks?

Do we need to sign our "transactions". I mean in voting i guess we have to sign it to say that this vote is from the person I say it is.

How do we distribute the mining application to the class? Not sure how we would be able to run arbitrary Python/C
code on people's machines in a demo.


## Testing plan
Unit testing for each new function and class.

Webapp testing/debugging features included in both Django and Flask.

Integration testing could be done via randomly generated inputs within set parameter ranges/options.

