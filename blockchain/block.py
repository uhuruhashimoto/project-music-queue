import bitstring
import hashlib
import json
import rsa

from .entry import deserialize as deserialize_entry
from .entry import Entry

NONCE_INIT = 0


class Block:
    def __init__(self, entries, public_key, hash_prev):
        """
        Initialize a block

        parameters:
            entries -- list of Entry objects (see ./entry.py) to be included in the block
            public_key -- RSA public key of the miner who has generated this block
            hash_prev -- SHA256 hash of the previous block in the chain
        """
        self.entries = entries
        self.public_key = public_key
        self.hash_prev = hash_prev
        self.nonce = NONCE_INIT
        self.signature = None
        self.block_prev = None
    

    def sign(self, private_key):
        
        """
        Sign the block's content with the provided private key instance (see 
        package rsa)

        parameters:
            private_key -- RSA private key
        """
        message = f'{self.entries[-1].serialize()}'.encode()
        self.signature = rsa.sign(message, private_key, 'SHA-1').hex() 


    def verify(self, block_prev, hash_padding):
        """
        Verify that a block is valid. To be valid, the block must satisfy:
            - self.sha256() must start with hash_padding number of zeroes
            - self.public_key must be the public RSA key of an authenticated miner
                - Considered a reach goal of the project, and not done for now. Would
                        require certification authority style management
            - self.signature must be a valid signature for self.public_key
                computed on the last entry in entries
            - self.hash_prev must match hash previous head of blockchain
            - each entry in self.entries must be valid (by calling Entry.verify())

        parameters:
            block_prev -- the previous block in the blockchain
            hash_padding -- the number of zeroes needed at the start of a valid block hash

        returns:
            True if the block is valid, False otherwise
        """
        if not self.block_prev:
            dat = self.serialize().encode('utf-8')
            hash_val = hashlib.sha256(dat).digest()
            bitarray = bitstring.BitArray(hash_val)

            # check the block prefix for necessary number of 0
            if (bitarray >> (len(bitarray) - hash_padding)):
                return False
        
            if len(self.entries):
                message = f'{self.entries[-1].serialize()}'.encode()
                try:
                    pk = self.public_key
                    rsa.verify(message, bytes.fromhex(self.signature), rsa.PublicKey(pk[0], pk[1]))
                except Exception as e:
                    print(f'Encountered verification error in Block/verify() \n{e}')
                    return False
            
            if block_prev.sha256() != self.hash_prev:
                return False

            for entry in self.entries:
                if not entry.verify():
                    return False

            return True
        else:
            return True


    def serialize(self):
        """
        Serialize the object to a JSON representation

        returns:
            string containing JSON
        """

        self_dict = self.__dict__.copy()
        self_dict['entries'] = [entry.serialize() for entry in self_dict['entries']]

        self_dict['block_prev'] = None
        self_dict['signature'] = str(self_dict['signature'])

        return json.JSONEncoder().encode(self_dict)


    def sha256(self):
        """
        Generate a SHA256 hash of the block's JSON representation

        returns:
            bytes data containing the SHA256 hash of the block
        """
        sha = hashlib.sha256()
        sha.update(self.serialize().encode('utf-8'))
        return sha.hexdigest()

    def getEntries(self):
        return 


def deserialize(jsonin):
    """
    Returns a Block object given a JSON string representation of the object.

    parameters:
        jsonin -- A JSON string representation of a Block object
    
    returns:
        Block object filled with provided data
    """
    js = json.loads(jsonin)
    es = js['entries']
    entries = [deserialize_entry(entry_str) for entry_str in es]
    # what?
    public_key = js["public_key"]

    block = Block(entries, public_key, js['hash_prev'])
    block.nonce = js['nonce']
    block.signature = js['signature']

    return block
