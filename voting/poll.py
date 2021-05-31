import secrets

from datetime import datetime
from json import JSONEncoder


class Poll:
    """
    Poll object representing a poll submitted by a tracker for a specific song.
    """

    def __init__(self, song, head, submitter):
        """
        Initializes a poll object by accepting the song name, current head block,
        and submitter of the poll.

        parameters:
            song - name of the song
            start_block - current head of the blockchain, provided by submitter of the poll
            submitter - id provided by the submitter of the poll (for demo purposes)

        returns:
            an Poll instance
        """
        self.song = song
        self.start_block = head.sha256()
        self.submitter = submitter 

        self.start_time = datetime.now(tz='utc').strftime('%Y-%M-%D %h:%m')  # submitter and start_time for demo purposes
        self.poll_id = secrets.token_bytes(16)  # generate a 16-byte random token id 
                                                # for the poll to prevent duplication issues


    def serialize(self):
        """
        Serialize the poll object to a JSON string.

        returns:
            JSON representation of Poll
        """
        self_dict = self.__dict__
        self_dict['start_block'] = start_block.encode('utf-8')

        JSONEncoder().encode(self.__dict__)
