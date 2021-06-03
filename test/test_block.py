import unittest
from unittest.mock import Mock, patch
from blockchain.block import Block


def get_mock_entries(verify=True, n=5):
    """
    Initialize a mock entry list. Allows caller to make the entries within the list
    fail verification if `verify` set to False

    parameters:
        entry_verify -- set the return value for entry.verify() for each of the entries in 
                    the mock block
        n -- number of entries to generate

    returns:
        Block instance with specified behavior
    """
    entries = []
    for i in range(n):
        mock_entry = Mock()
        mock_entry.verify.return_value = verify
        entries.append(mock_entry)
    
    return entries

def get_mock_block(entry_verify = True):
    """
    Initialize a mock block object. Allows caller to make the entries within the block
    either fail verification if `entry_verify` set to False

    parameters:
        entry_verify -- set the return value for entry.verify() for each of the entries in 
                    the mock block
    
    returns:
        Block instance with specified behavior
    """
    entries = get_mock_entries(entry_verify)
    key = (Mock(), Mock())
    hash_prev = Mock()
    return Block(entries, key, hash_prev)

class TestBlockMethods(unittest.TestCase):

    @patch('blockchain.block.rsa')
    def test_sign_block(self, rsa_m):
        """
        Test that signing a block works as expected
        """
        block = get_mock_block()
        key = 'not_a_key'
        rsa_m.sign.return_value.hex.return_value = 'signature'
        
        block.sign(key)
        rsa_m.sign.assert_called_once()
        self.assertEqual(block.signature, 'signature')
        self.assertIn(key, rsa_m.sign.call_args[0])


    @patch('blockchain.block.rsa')
    @patch('blockchain.block.bytes')
    def test_verify_all_valid(self, rsa_m, bytes_m):
        """
        Test that verification passes when all entries are valid in a block with
        a valid signature
        """
        block = get_mock_block(True)
        head = Mock()
        block.signature = Mock()
        block.hash_prev = 'prev'
        head.sha256.return_value = 'prev'
        self.assertTrue(block.verify(head) ,'Failed fully valid block verification test')

        for entry in block.entries:
            entry.verify.assert_called_once()


    @patch('blockchain.block.rsa')
    @patch('blockchain.block.bytes')
    def test_verify_invalid_prev_valid_entries(self, rsa_m, bytes_m):
        """
        Test that verification fails when a block with valid entries but an invalid 
        previous block is passed for verification (i.e. a hash mismatch).
        """
        block = get_mock_block(True)
        head = Mock()
        block.hash_prev = 'prev'
        
        head.sha256.return_value = 'not_prev'
        self.assertFalse(block.verify(head))
        

    @patch('blockchain.block.rsa')
    @patch('blockchain.block.bytes')
    def test_verify_valid_prev_invalid_entries(self, rsa_m, bytes_m):
        """
        Test that verification fails when a block with invalid entries and a valid 
        previous block is passed for verification.
        """
        block = get_mock_block(False)
        head = Mock()
        block.hash_prev = 'prev'

        head.sha256.return_value = block.hash_prev
        self.assertFalse(block.verify(head))

        block.entries[0].verify.assert_called_once()
        for entry in block.entries[1:]:
            entry.verify.assert_not_called()

        
    @patch('blockchain.block.rsa')
    @patch('blockchain.block.bytes')
    def test_verify_invalid_prev_invalid_entries(self, rsa_m, bytes_m):
        """
        Test that verification fails when a block with invalid entries but an invalid 
        previous block is passed for verification (i.e. a hash mismatch).
        """
        block = get_mock_block(False)
        head = Mock()
        block.hash_prev = 'prev'

        head.sha256.return_value = 'not_prev'
        self.assertFalse(block.verify(head))

        for entry in block.entries:
            entry.verify.assert_not_called()


## these three tests unnecessary as they are basic requirements of the protocol
## and because writing the tests would take far longer than any benefit gained
## as failing these tests would be immediately noticeable in integration    
#    def test_serialize(self):
#    def test_sha256(self):
#    def test_deserialize(self):


if __name__ == '__main__':
    unittest.main()
