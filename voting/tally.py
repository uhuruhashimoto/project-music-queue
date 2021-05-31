from blockchain import Blockchain
from .poll import PollResults


def put_new_poll(song, head, miner_key, name='Anonymous'):
    """
    Allows a miner to submit a new poll, given they have credit to do so.

    parameters:
        song - name of the song for the poll
        head - current head of the blockchain
        miner_key - public key of the miner to verify poll credits
        name - name to display in application for submitting miner
    
    returns:
        either nothing or the poll object
    """
    # Need to first check if miner has credit
    # TODO Determine miner credit scheme

    # given they do have credit, next we have to make a poll
    poll = Poll(song, head, name)

    # now that we have a poll, blast it out
    # application.publish_poll(poll)


def tally_block_votes(poll_id, block, results):
    yeas = 0
    nays = 0
    for entry in block.entries:
        if entry.poll_id == poll_id:
            if entry.vote == 'yes':  # TODO DESCRIBE PROTOCOL FOR VOTING SOMEWHERE
                yeas += 1
            else:
                nays += 1

    results.update(yeas, nays)


def tally_votes(poll, blockchain):
    """
    Tally the votes in a poll as cast in the provided blockchain.

    parameters:
        poll - a Poll object (see poll.py) containing information about the poll to tally
        blockchain - blockchain to use as a vote ledger

    assumptions:
        blockchains passed to this function are valid.
    """
    results = PollResults()
    block = blockchain.head

    while block.sha256() != poll.start_block:
        tally_block_votes(poll.poll_id, block, results)
        block = block.block_prev

    return results
