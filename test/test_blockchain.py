from blockchain.block import Block
import unittest
from unittest.mock import Mock, patch
from blockchain.blockchain import Blockchain


def mock_block(verify=True, hash=True):
    """
    Initialize a mock block object. Allows caller to make the block either pass 
    or fail verification and either pass or fail hash integrity check using 
    `verify` and `hash` fields respectively.

    parameters:
        verify -- sets the return value for when block.verify() is called.
        hash -- sets the value for block.hash_prev to be 'good_hash' if True and
                'bad_hash' if False 
    
    returns:
        Block instance with specified behavior
    """
    block = Mock()
    block.verify.return_value = verify
    block.sha256.return_value = 'good_hash'

    if hash:    block.hash_prev = 'good_hash'
    else:       block.hash_prev = 'bad_hash'

    return block


def mockchain_stub():
    """
    Initialize a mock blockchain (mockchain) object stub. This stub contains
    a mock block (see mock_block() above) which will successfully verify as
    the root node in the blockchain (replacing our usual head setting protocol
    in ~/blockchain/blockchain.py).

    returns:
        blockchain of length 1 with a good mock block as its only block
    """
    good_block = mock_block(verify=True, hash=True)
    blockchain = Blockchain()

    blockchain.add_block(good_block)
    blockchain.head.block_prev = None

    return blockchain


class TestBlockchainMethods(unittest.TestCase):

    def test_add_block(self):
        """
        Test adding a block to the chain. The block does not need to pass
        verification to use this function, so this test covers the function
        fully.
        """
        blockchain = Blockchain()
        head = blockchain.head
        block = mock_block()

        blockchain.add_block(block)

        self.assertEqual(block.block_prev, head)
        self.assertEqual(block, blockchain.head)
        self.assertEqual(blockchain.length, 1)


    def test_verify_valid(self):
        """
        Test that a valid chain passes blockchain.verify_chain().

        Blockchain structure: 0 <- [h(0), A] <- [h(a), B] <- [h(B), C]
        block.verify() returns True for all three blocks
        """
        blockchain = mockchain_stub()
        blockchain.add_block(mock_block())
        blockchain.add_block(mock_block())

        self.assertTrue(blockchain.verify_chain(8))


    def test_verify_bad_block(self):
        """
        Tests that a chain with a bad block fails blockchain.verify_chain().

        Blockchain structure: 0 <- [h(0), A] <- [h(a), B] <- [h(B), C]
        block.verify() returns False for B, True for the others
        """
        blockchain = mockchain_stub()
        blockchain.add_block(mock_block(verify=False))
        blockchain.add_block(mock_block())

        self.assertFalse(blockchain.verify_chain(None))


    def test_verify_bad_hash(self):
        """
        Tests that a chain where there is a bad hash fails blockchain.verify_chain().
        
        Blockchain structure: 0 <- [h(0), A] <- [not h(A), B] <- [h(B), C]
        block.verify() returns True for all three
        """
        blockchain = mockchain_stub()
        blockchain.add_block(mock_block(hash=False))
        blockchain.add_block(mock_block())        

        self.assertFalse(blockchain.verify_chain(None))

## these three tests unnecessary as they are basic requirements of the protocol
## and because writing the tests would take far longer than any benefit gained
## as failing these tests would be immediately noticeable in integration    
#    def test_serialize(self):
#    def test_sha256(self):
#    def test_deserialize(self):


if __name__ == '__main__':
    unittest.main()
