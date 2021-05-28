import json
import hashlib

from .block import Block

class Blockchain:
    def __init__(self, padding):
        """
        Initialize an empty blockchain

        parameters:
            padding -- HASH_PADDING as given by tracker
        """

        #Set the head of the blockchain as an empty block
        self.head = Block(None, None, None)

    def add_block(self, block):
        """
        Adds a block to the end of the blockchain

        parameters:
            block -- Block to be added
        """

        block.prev_block = self.head
        self.head = block

    def verify_chain(self):
        """
        Verify that the blockchain is valid. To be valid, the each block must satisfy requirements
        listed in "block.py"

        returns:
            True if the entire blockchain is valid, False otherwise
        """
        ptr = self.head

        while ptr is not None:
            if (not ptr.verify()):
                return False
            ptr = ptr.block_prev

        return True

    def serialize(self):
        """
        Serialize the object to a JSON representation

        returns:
            string containing JSON representation of chain
        """

        ptr = self.head
        chain = []

        while ptr is not None:
            chain.append(ptr.serialize())
            ptr = ptr.block_prev

        return json.dumps(chain)

def deserialize(jsonin, padding):
    """
    Returns a Blockchain object given a JSON string representation of the object.

    parameters:
        jsonin -- A JSON string representation of a Blockchain object
        padding -- Required HASH_PADDING of the blockchain
    
    returns:
        Blockchain object filled with provided data
    """

    out = Blockchain(padding)

    js = json.loads(jsonin)

    for block in reversed(js):
        out.add_block(block)
    
    return out
    


    
        

        