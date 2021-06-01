import secrets

from datetime import datetime
from json import JSONEncoder

YEA = 'T'
NAY = 'F'

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
            a Poll instance
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
        self_dict['start_block'] = self.start_block.encode('utf-8')

        return JSONEncoder().encode(self.__dict__)


class PollResults:
    """
    Simple object to store yea/nay count for polls
    """
    def __init__(self):
        self.yeas = 0
        self.nays = 0
        self.votes = {}


    def update(self, votes, replace=False):
        """
        Update the poll results with the provided votes. Each user can only vote once per poll,
        so the most recent vote for the song is chosen in cases of multiple votes from a user.

        parameters:
            votes: dictionary from voter public key to voter id
            replace: whether to replace votes for voters or not. Default False as we 
                traverse the blockchain from head to tail (i.e. most recent first)
        """
        if not replace:
            unseen_voters = set(self.votes.keys()).intersection(votes.keys()) 

        for pub_key, vote in votes.entries:
            if replace or pub_key in unseen_voters:
                votes[pub_key] = vote


    def tally(self):
        """
        Calculate the yeas and nays

        returns:
            tuple with (yeas, nays) as integers
        """
        yeas = 0
        nays = 0

        for vote in votes:
            if vote == 'Y': # TODO FIGURE OUT VOTING PROTOCOL
                yeas += 1
            elif vote == 'N':
                nays += 1        

        return yeas, nays


    def serialize(self):
        """
        Serialize the poll result object to a JSON string.

        returns:
            JSON representation of PollResults
        """
        return JSONEncoder.encode(self.__dict__)
