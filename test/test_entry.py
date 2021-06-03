import unittest
from unittest.mock import Mock, patch
from blockchain.entry import Entry


def get_mock_entry():
    poll_id = 'poll_id'
    vote = 'vote'
    key = (Mock(), Mock())
    return Entry(poll_id, vote, key)


class TestEntryMethods(unittest.TestCase):

    @patch('blockchain.entry.rsa')
    def test_sign_entry(self, rsa_m):
        entry = get_mock_entry()
        key = 'not_a_key'
        
        entry.sign(key)
        rsa_m.sign.assert_called_once()

    @patch('blockchain.entry.bytes')
    @patch('blockchain.entry.rsa')
    def test_verify_entry(self, rsa_m, bytes_m):
        ## test fully valid
        entry = get_mock_entry()
        entry.signature = Mock()
        self.assertTrue(entry.verify() ,'Failed valid entry verification test')

        rsa_m.verify.side_effect = Exception()
        ## test invalid prev
        self.assertFalse(entry.verify(), 'Failed verification check with invalid data; returned True')


## these three tests unnecessary as they are basic requirements of the protocol
## and because writing the tests would take far longer than any benefit gained
## as failing these tests would be immediately noticeable in integration    
#    def test_getID(self):
#    def test_sha256(self):
#    def test_deserialize(self):


if __name__ == '__main__':
    unittest.main()
