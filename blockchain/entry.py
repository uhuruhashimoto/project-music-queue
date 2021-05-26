import json
import rsa

class Entry: 
    def __init__(self, song, vote, public_key):
        """
        Initialize an entry

        parameters:
            song -- Song Title
            vote -- Yes/No Vote
            public_key -- RSA Public Key
        """
        self.song = song
        self.vote = vote
        self.public_key = public_key
        self.signature = None

    def sign(self, private_key):
        """
        Sign the entry's content with the provided private key instance (see 
        <whatever_crypto_package_we_end_up_using>/rsa)

        parameters:
            private_key -- RSA Private Key
            
        returns:
            nothing
        """
        message = (self.song + self.vote).encode()
        self.signature = rsa.sign(message, private_key, 'SHA-1') 
        
        

    def verify(self):
        """
        Verify an entry against the listed public key (see 
        <whatever_crypto_package_we_end_up_using>/rsa)
        
        returns:
            True if verification is successful, False otherwise
        """
        message = (self.song + self.vote).encode()

        try:
            rsa.verify(message, self.signature, self.public_key)
            return True
        except rsa.pkcs1.VerificationError as e:
            print(f'Encountered verification error {e}')
            return False
        
    def serialize(self):
        '''
        Returns a JSON String representing the entry.

        returns:
            string containing JSON
        '''
        return json.JSONEncoder().encode(self.__dict__)


def deserialize(jsonin):
    '''
    Returns an Entry object given a JSON string representation of the object.

    parameters:
        jsonin -- A JSON string representation of an Entry object
    
    returns:
        Entry object filled with provided data
    '''
    js = json.loads(jsonin)
    entry = Entry(js["song"], js["vote"], js["public_key"])
    entry.signature = js["signature"]
    return entry
