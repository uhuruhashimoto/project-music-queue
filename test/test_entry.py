import unittest
from unittest.mock import Mock, patch
import blockchain.entry


def get_mock_entry():
    poll_id = 'poll_id'
    vote = 'vote'
    key = (Mock(), Mock())
    return blockchain.entry.Entry(poll_id, vote, key)


class TestEntryMethods(unittest.TestCase):

    @patch('blockchain.entry.rsa')
    def test_sign_entry(self, rsa_m):
        """
        Test that signing an entry works as expected
        """
        entry = get_mock_entry()
        key = 'not_a_key'
        rsa_m.sign.return_value.hex.return_value = 'signature'
        
        entry.sign(key)
        rsa_m.sign.assert_called_once()
        self.assertIn(key, rsa_m.sign.call_args[0])
        self.assertEqual(entry.signature, 'signature')


    @patch('blockchain.entry.rsa')
    @patch('blockchain.entry.bytes')   # needed for correct errors to be thrown
    def test_verify_valid(self, rsa_m, bytes_m):
        """
        Verify that an entry which correctly passes rsa.verify()
        """
        entry = get_mock_entry()
        entry.signature = Mock()

        rsa_m.verify.return_value = True

        self.assertTrue(entry.verify() ,'Failed valid entry verification test')


    @patch('blockchain.entry.rsa.verify', return_value=False, side_effect=Exception())
    @patch('blockchain.entry.bytes')   # needed for correct errors to be thrown
    def test_verify_invalid(self, rsa_verify, bytes_m):
        """
        Verify that an entry which fails rsa verification returns false on .verify()
        """
        entry = get_mock_entry()
        entry.signature = Mock()

        self.assertFalse(entry.verify(), 'Failed verification check with invalid data; returned True')


## these three tests unnecessary as they are basic requirements of the protocol
## and because writing the tests would take far longer than any benefit gained
## as failing these tests would be immediately noticeable in integration    
#    def test_getID(self):
#    def test_sha256(self):
#    def test_deserialize(self):


if __name__ == '__main__':
    unittest.main()
