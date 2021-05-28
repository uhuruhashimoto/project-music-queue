import json
import rsa

class Entry: 
    def __init__(self, song, vote, public_key):
        """
        Initialize an entry

        parameters:
            song -- song title
            vote -- yes/no vote
            public_key -- RSA public key
        """
        self.song = song
        self.vote = vote
        self.public_key = public_key
        self.signature = None

    def sign(self, private_key):
        """
        Sign the entry's content with the provided private key instance (see 
        package rsa)

        parameters:
            private_key -- RSA private key
        """
        message = (self.song + self.vote).encode()
        self.signature = rsa.sign(message, private_key, 'SHA-1') 
        

    def verify(self):
        """
        Verify an entry against the listed public key (see package rsa)
        
        returns:
            True if verification is successful, False otherwise
        """
        # TODO figure out authentication of keys
        message = f'{self.song} - {self.vote}'.encode()

        try:
            rsa.verify(message, self.signature, self.public_key)
            return True
        except rsa.pkcs1.VerificationError as e:
            print(f'Encountered verification error in Entry/verify() \n{e}')
            return False
        

    def serialize(self):
        """
        Serialize the entry to a JSON representation

        returns:
            string containing JSON
        """
        self_dict = self.__dict__.copy()
        self_dict['public_key'] = str(self_dict['public_key'].n)

        return json.JSONEncoder().encode(self_dict)


def deserialize(jsonin):
    """
    Returns an Entry object given a JSON string representation of the object.

    parameters:
        jsonin -- A JSON string representation of an Entry object
    
    returns:
        Entry object filled with provided data
    """
    # TODO convert json strings to correct types once correct type is known
    js = json.loads(jsonin)
    entry = Entry(js['song'], js['vote'], js['public_key'])
    entry.signature = js['signature'] 
    return entry
