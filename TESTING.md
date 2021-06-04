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

1. basic demo + new peers receiving relevant data (blockchains, polls, etc.)
	- Demo video: https://cutt.ly/unxQklZ
2. client voting capability (modifying existing votes as well)
	- Video: https://cutt.ly/nnxQUKu
3. malicious block sending
	- Video: https://cutt.ly/BnxQPgp
4. bad inputs to stdin on tracker/clients
   	- Video: https://cutt.ly/HnxQHDP
5. client or tracker unexpectedly leaves (ctrl^c/EXIT)
        - Video: https://cutt.ly/HnxQHDP (Same as 4)
6. poll handling by tracker (starting, overwriting, and ending polls)
        - Video: https://cutt.ly/HnxQHDP (Same as 4)
7. client display ("tally" command) during all stages of voting process
        - Video: https://cutt.ly/HnxQHDP (Same as 4)
8. printing blockchains from each client to inspect for differences
        - Video: https://cutt.ly/HnxQHDP (Same as 4)


