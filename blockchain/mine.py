import rsa
import hashlib
import math #for faster bitmask calculation

# Collection of APIs used by client in mining mode (miner)
# miner takes a single block and maintains a copy of the blockchain
# mining is the process of using rsa to find a hash for the block
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
	
		#computes hash w rsa
		#using transactions and prevHash
		hashValue = hashlib.sha256()
		
		
		#checks if the hashValue is longer than the hash padding
		#should use shifts and AND operator
		if (math.log10(hashValue))+1 - hash_padding  > 0): 
  			#checks with hash padding
			isMined = (int(hashValue[:hash_padding]) == 0)
		else:
  			print('Impossible to hash')
		
		#increments nonce by 1 if unsuccessful
		nonce += nonce
		
	#returns hash value if successful
	return hashValue
	
	def verify(hashValue, bitmask, hash_padding):
		return hashValue & (1 >> hash_padding)
		
		
		#Good job on: general structure
	#TODO FIX: get hash correctly (sha256 somehow?), use rightshift and AND operator for isMined (sep function), fix incorrect error checking
	# what is the hash? a string? maybe cast to a string or use toString or something
