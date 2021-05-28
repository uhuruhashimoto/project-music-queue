import json
import time
from hashlib import sha256

TIMEOUT = 1000000000000000000000000000000000000000000

''' Collection of APIs used by client in mining mode (miner)
 miner takes a block and uses its data, hash, and nonce to mine
Currently uses hashlib for sha256 implementation'''

#Inputs: block number, string of transactions, byte string prev hash, padding
def mine(blocknum, transactions, prev_hash, hash_padding):
	hash_val = '' #string for leading zeros
	nonce = 0
	is_mined = False
	
	pref = '0'*hash_padding
	
	#start time
	t = time.time()
	
	while not(is_mined):
		#concatenate data
   		txt = str(blocknum) + str(transactions) + prev_hash + str(nonce)
		
  		#compute hash val
   		hash_val = SHA256(txt)
  		
		elapsed = time.time() - t
  		
  		#check
		if (hash_val.startswith(pref)):
    		is_mined = True
  		
		if (elapsed > TIMEOUT):
    		raise BaseException(f'Mining timeout')
    		is_mined = True
  		
  		# increment nonce
		nonce = nonce + 1
		
	return hashValue
	
	
def mine(block, hash_padding):
	mine(block.blocknum, block.entries.serialize(), block.hash_prev, hash_padding)
	
#returns sha256 hash of a string
def SHA256(txt):
	return sha256(txt.encode("ascii")).hexdigest()
	