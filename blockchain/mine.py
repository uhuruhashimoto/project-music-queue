import json
import time
from block import *

TIMEOUT = 10000000000 #arbitrarily large timeout

''' Collection of APIs used by client in mining mode (miner)
 miner takes a block and uses its data, hash, and nonce to mine'''

#Inputs: block number, string of transactions, byte string prev hash, padding
def mine(block, shouldMine):
	nonce = 0
	is_mined = False
	
	pref = '0'*hash_padding #string for leading zeros

	#start time
	t = time.time()

	# serialize data to json string
	txt = block.serialize().encode('utf-8')
	
	while not is_mined and shouldMine:
		# compute hash val -- must always match block.py
		hash_val = sha256(txt).hexdigest()

		#check
		if hash_val.startswith(pref):
    		is_mined = True
  		
		if time.time()-t > TIMEOUT:
			raise BaseException(f'Mining timeout')
  		
		# increment nonce
		nonce = nonce + 1
		
	return hash_val
	
	
# def mine_block(block, hash_padding):
# 	hash_val = mine(block.entries.serialize(), block.hash_prev, hash_padding)
# 	return hash_val
	