import hashlib
import json

from entry import deserialize as deserialize_entry
from entry import Entry

NONCE_INIT = 0  # TODO convert this to correct 64-bit datatype once known


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
        message = self.entries[-1].serialize().encode()
        self.signature = rsa.sign(message, private_key, 'SHA-1') 


    def verify(self, head):
        """
        Verify that a block is valid. To be valid, the block must satisfy:
            - self.public_key must be the public RSA key of an authenticated miner
            - self.signature must be a valid signature for self.public_key
                computed on the last entry in entries
            - self.hash_prev must match hash of current head of blockchain
            - each entry in self.entries must be valid (by calling Entry.verify())

        returns:
            True if the block is valid, False otherwise
        """
        # TODO figure out authentication of keys
        # if self.public_key <isn't one we trust>
        #    return False

        message = self.entries[-1].serialize()
        try:
            rsa.verify(message, self.signature, self.public_key)
        except rsa.pkcs1.VerificationError as e:
            print(f'Encountered verification error in Block/verify() \n{e}')
            return False

        if head.sha256() != self.hash_prev:
            return False

        for entry in self.entries:
            if not self.verify():
                return False

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
        return json.JSONEncoder().encode(self_dict)

    def sha256(self):
        """
        Generate a SHA256 hash of the block's JSON representation

        returns:
            bytes data containing the SHA256 hash of the block
        """
        sha = hashlib.sha256()
        sha.update(self.serialize().encode('utf-8'))
        return sha.digest()


def deserialize(jsonin):
    """
    Returns a Block object given a JSON string representation of the object.

    parameters:
        jsonin -- A JSON string representation of a Block object
    
    returns:
        Block object filled with provided data
    """
    # TODO convert json strings to correct types once correct type is known
    js = json.loads(jsonin)
    
    entries = [deserialize_entry(entry_str) for entry_str in js['entries']]

    block = Block(entries, js['public_key'], js['hash_prev'])
    block.nonce = js['nonce']
    block.hash_prev = js['signature']

    return block

entries = []
entries2 = []
entries.append(Entry("Backslide", "no", None))
entries.append(Entry("Backslide", "no", None))
entries.append(Entry("Backslide", "no", None))
entries.append(Entry("Backslide", "no", None))
entries2.append(Entry("Backslide", "yes", None))
entries2.append(Entry("Backslide", "no", None))
entries2.append(Entry("Backslide", "no", None))
entries2.append(Entry("Backslide", "no", None))
newblock = Block(entries, None, None)
newblock2 = Block(entries2, None, None)

newblock.serialize()

