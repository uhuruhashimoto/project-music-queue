import rsa
import hashlib

''' Collection of APIs used by client in mining mode (miner)
 miner takes a single block and maintains a copy of the blockchain
 mining is the process of using rsa to find a hash for the block '''

#TODO FIX: get hash correctly (sha256 somehow?), use rightshift and AND operator for isMined (sep function), add error checking
# what is the hash? a string? maybe cast to a string 
# TODO: add recognition to re-start if another miner finds the hash first

#inputs: new block of transactions and hash padding
def mine(block, blockchain, hash_padding):
	hashValue = '' #string for leading zeros
	nonce = 0 #starts with nonce of 0
	isMined = False
	
	#mining uses previous block's hash (from the head of the blockchain)
	prevBlock = blockchain.getHead()
	prevHash = prevBlock.hash_prev
	
	while(!isMined):
	
		#computes hash w rsa using transactions and prevHash
		hashValue = str(hashlib.sha256())
		
		
		#checks if the hashValue is longer than the hash padding
		isMined = verify(hashValue, hash_padding)
		
		#increments nonce by 1 if unsuccessful
		nonce += nonce
		
	#returns hash value if successful
	return hashValue
	
	
#Do something like return hashValue & (111... or shift >> hash_padding)
def verify(hashValue, hash_padding):
	return (int(hashValue[:hash_padding]) == 0)
	
