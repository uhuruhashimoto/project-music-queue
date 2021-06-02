import json
import rsa
import hashlib


class Entry: 
    def __init__(self, poll_id, vote, public_key):
        """
        Initialize an entry

        parameters:
            poll_id -- ID relating to a specific poll for a song
            vote -- yes/no vote
            public_key -- RSA public key as a tuple (n, e)
        """
        self.poll_id = poll_id
        self.vote = vote
        self.public_key = public_key
        self.signature = None
    

    def getID(self):
        sha = hashlib.sha256()
        sha.update((self.poll_id + str(self.public_key[0]) + str(self.public_key[1])).encode('utf-8'))
        return sha.hexdigest()


    def sign(self, private_key):
        """
        Sign the entry's content with the provided private key instance (see 
        package rsa)

        parameters:
            private_key -- RSA private key
        """
        message = f'{self.poll_id} + {self.vote}'.encode()
        # Create the signature and then turn it to string. 
        self.signature = rsa.sign(message, private_key, 'SHA-1').hex()
        

    def verify(self):
        """
        Verify an entry against the listed public key (see package rsa)
        
        returns:
            True if verification is successful, False otherwise
        """
       
        message = f'{self.poll_id} + {self.vote}'.encode()

        try:
            # Remember  that public key and signature are stored as primitives for serialization, so before we verify revert them back to their proper forms for rsa.verify
            pk = self.public_key
           
            rsa.verify(message, bytes.fromhex(self.signature), rsa.PublicKey(pk[0], pk[1]))
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
        # Need to serialize both n and e 
       

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
    entry = Entry(js['poll_id'], js['vote'], js['public_key'])
    entry.signature = js['signature'] 
    return entry
