# TESTING.md for Votechain

## Unit Tests

The following unit tests will verify that individual module components
work as intended. They employ the unittest package to assert and check
for proper states in our code.
### test_block.py
### test_blockchain.py
### test_entry.py
See the commented test module for more info. Each blockchain object has a 
seperate series of tests which covers any fundamental class functions.

## End-to-End/Blackbox Testing
This tests the flows:

2. basic demo + new peers receiving relevant data (blockchains, polls, etc.)
	- Demo video
3. client voting capability (modifying existing votes as well)
	- Video:
4. malicious block sending
	- 
5. bad inputs to stdin on tracker/clients
    - 
6. client or tracker unexpectedly leaves (ctrl^c/EXIT)
    - 
7. poll handling by tracker (starting, overwriting, and ending polls)

8. client display ("tally" command) during all stages of voting process

9. printing blockchains from each client to inspect for differences


