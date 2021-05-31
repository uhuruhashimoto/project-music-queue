import json

from .block import Block, deserialize as deserialize_block
from .entry import Entry

class Blockchain:
    def __init__(self):
        """
        Initialize an empty blockchain
        """

        #Set the head of the blockchain as an empty block
        self.head = Block([], None, None)
        self.head.block_prev = None
        self.length = 0

    def add_block(self, block):
        """
        Adds a block to the end of the blockchain

        parameters:
            block -- Block to be added
        """

        block.block_prev = self.head
        self.head = block
        self.length = self.length + 1

    def verify_chain(self, padding):
        """
        Verify that the blockchain is valid. To be valid, the each block must satisfy requirements
        listed in "block.py"

        parameters:
            padding -- HASH_PADDING as given by tracker

        returns:
            True if the entire blockchain is valid, False otherwise
        """

        #TODO add padding functionality to block verification 
        #also -> what is the "head" parameter in the Block.verify() function?

        ptr = self.head


        while ptr is not None:
            if (not ptr.verify() or ptr.hash_prev != ptr.block_prev.sha256()):
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

def deserialize(jsonin):
    """
    Returns a Blockchain object given a JSON string representation of the object.

    parameters:
        jsonin -- A JSON string representation of a Blockchain object
        padding -- Required HASH_PADDING of the blockchain
    
    returns:
        Blockchain object filled with provided data
    """

    out = Blockchain()

    js = json.loads(jsonin)
    js.pop()    
    for block in reversed(js):
        out.add_block(deserialize_block(block))
    
    return out
    
