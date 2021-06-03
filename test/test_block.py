import unittest
from unittest.mock import Mock, patch
from blockchain.block import Block


def get_mock_entries(verify=True, n=5):
    entries = []
    for i in range(n):
        mock_entry = Mock()
        mock_entry.verify.return_value = verify
        entries.append(mock_entry)
    
    return entries

def get_mock_block(entry_verify = True):
    entries = get_mock_entries(entry_verify)
    key = (Mock(), Mock())
    hash_prev = Mock()
    return Block(entries, key, hash_prev)

class TestBlockMethods(unittest.TestCase):

    @patch('blockchain.block.rsa')
    def test_sign_block(self, rsa_m):
        block = get_mock_block()
        key = 'not_a_key'
        
        block.sign(key)
        rsa_m.sign.assert_called_once()

    @patch('blockchain.block.rsa')
    @patch('blockchain.block.bytes')
    def test_verify_all_valid(self, rsa_m, bytes_m):
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
        block = get_mock_block(True)
        head = Mock()
        block.hash_prev = 'prev'
        
        head.sha256.return_value = 'not_prev'
        self.assertFalse(block.verify(head))

        
    @patch('blockchain.block.rsa')
    @patch('blockchain.block.bytes')
    def test_verify_invalid_prev_invalid_entries(self, rsa_m, bytes_m):
        block = get_mock_block(False)
        head = Mock()
        block.hash_prev = 'prev'

        head.sha256.return_value = 'not_prev'
        self.assertFalse(block.verify(head))

        for entry in block.entries:
            entry.verify.assert_not_called()
        

    @patch('blockchain.block.rsa')
    @patch('blockchain.block.bytes')
    def test_verify_valid_prev_invalid_entries(self, rsa_m, bytes_m):
        block = get_mock_block(False)
        head = Mock()
        block.hash_prev = 'prev'

        head.sha256.return_value = block.hash_prev
        self.assertFalse(block.verify(head))

        block.entries[0].verify.assert_called_once()
        for entry in block.entries[1:]:
            entry.verify.assert_not_called()

## these three tests unnecessary as they are basic requirements of the protocol
## and because writing the tests would take far longer than any benefit gained
## as failing these tests would be immediately noticeable in integration    
#    def test_serialize(self):
#    def test_sha256(self):
#    def test_deserialize(self):


if __name__ == '__main__':
    unittest.main()
