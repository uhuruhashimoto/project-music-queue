import secrets
import json
import pytz 
from datetime import datetime
from json import JSONEncoder

YEA = 'T'
NAY = 'F'

class Poll:
    """
    Poll object representing a poll submitted by a tracker for a specific song.
    """

    def __init__(self, song):
        """
        Initializes a poll object by accepting the song name, current head block,
        and submitter of the poll.

        parameters:
            song - name of the song

        returns:
            a Poll instance
        """
        self.song = song
        timezone = pytz.timezone('utc')
        self.start_time = datetime.now(tz=timezone).strftime('%Y-%M-%D %h:%m')  # submitter and start_time for demo purposes
        self.poll_id = secrets.token_bytes(16).hex()  # generate a 16-byte random token id 
        # for the poll to prevent duplication issues


    def serialize(self):
        """
        Serialize the poll object to a JSON string.

        returns:
            JSON representation of Poll
        """
        self_dict = self.__dict__

        return JSONEncoder().encode(self.__dict__)

def deserialize(jsonin):
    js = json.loads(jsonin)

    outPoll = Poll(js["song"])
    outPoll.start_time = js["start_time"]
    outPoll.poll_id = js["poll_id"]

    return outPoll





myPoll = Poll("chilltestsong")