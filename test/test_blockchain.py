from blockchain.block import Block
import unittest
from unittest.mock import Mock, patch
from blockchain.blockchain import Blockchain


def mock_block(verify=True, hash=True):
    block = Mock()
    block.verify.return_value = verify
    block.sha256.return_value = 'good_hash'

    if hash:    block.hash_prev = 'good_hash'
    else:       block.hash_prev = 'bad_hash'

    return block


def mockchain_stub():
    good_block = mock_block(verify=True)
    blockchain = Blockchain()

    blockchain.add_block(good_block)
    blockchain.head.block_prev = None

    return blockchain


class TestBlockchainMethods(unittest.TestCase):

    def test_add_block(self):
        blockchain = Blockchain()
        head = blockchain.head
        block = mock_block()

        blockchain.add_block(block)

        self.assertEqual(block.block_prev, head)
        self.assertEqual(block, blockchain.head)
        self.assertEqual(blockchain.length, 1)


    def test_verify_valid(self):
        # structure: 0 <- [h(0), A] <- [h(a), B] <- [h(B), C]
        # verify returns True for all three
        blockchain = mockchain_stub()
        blockchain.add_block(mock_block())
        blockchain.add_block(mock_block())

        self.assertTrue(blockchain.verify_chain(8))


    def test_verify_bad_signature(self):

        # structure: 0 <- [h(0), A] <- [h(a), B] <- [h(B), C]
        # verify(B.sig) returns False, others True
        blockchain = mockchain_stub()
        blockchain.add_block(mock_block(verify=False))
        blockchain.add_block(mock_block())

        self.assertFalse(blockchain.verify_chain(None))


    def test_verify_bad_data(self):
        
        # structure: 0 <- [h(0), A] <- [not h(A), B] <- [h(B), C]
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
