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

        ptr = self.head

        while ptr.block_prev is not None:
            if (not ptr.verify(ptr.block_prev) or ptr.hash_prev != ptr.block_prev.sha256()):
                return False
            ptr = ptr.block_prev

        return True

    # Assumes that the blockchain is valid. Iterates through it and tallies the votes
    def tally(self, poll):
        currentBlock = self.head
        yeas = 0
        neas = 0

        accountedVoters = set()

        while currentBlock is not None:
            if currentBlock.entries:
                for entry in currentBlock.entries:
                    if entry.poll_id == poll.poll_id:
                        # for some reason the public key is a list not a tuple
                        pk = (entry.public_key[0], entry.public_key[1])
                        if pk not in accountedVoters:

                            if entry.vote == "Y":
                                yeas +=1
                            else:
                                neas +=1
                            accountedVoters.add(pk)
            currentBlock = currentBlock.block_prev
        print(f"The tally has commenced for song: {poll.song}. With {yeas} vote(s) for yes and {neas} votes for no")





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
