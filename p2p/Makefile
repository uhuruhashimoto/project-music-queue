# Makefile for easy testing of modules.
PYTHON = python3

# Port numbers and addresses
TRACKER_PORT = 60005
CLIENT_LISTEN_PORT = 60010
TRACKER_ADDR = babylon8.thayer.dartmouth.edu

# Arguments for client program
# [tracker_address] [tracker_port] [self_port] [mining mode] [Malicious] [timeToMine] 
CLIENT_ARGS = $(TRACKER_ADDR) $(TRACKER_PORT) $(CLIENT_LISTEN_PORT) F F 15
MINER_ARGS = $(TRACKER_ADDR) $(TRACKER_PORT) $(CLIENT_LISTEN_PORT) T F 15
MALICIOUS_ARGS = $(TRACKER_ADDR) $(TRACKER_PORT) $(CLIENT_LISTEN_PORT) T T 15


# Arguments for tracker program
# [listen_port] [hash_padding] [timeout]
TRACKER_ARGS = $(TRACKER_PORT) 16

# Run this rule to install all necessary dependency structures and packages
setup:
	pip3 install -e ..
	make test

# Rule for running client.
client: client.py
	clear
	$(PYTHON) $^ $(CLIENT_ARGS)

# Rule for running miner
miner: client.py
	clear
	$(PYTHON) $^ $(MINER_ARGS)

malicious: client.py
	clear
	$(PYTHON) $^ $(MALICIOUS_ARGS)

# Rule for running tracker
tracker: tracker.py
	clear
	$(PYTHON) $^ $(TRACKER_ARGS)

# a rule to run the unit tests in the test folder
test:
	cd ..; \
	$(PYTHON) -m unittest -v

.PHONY: clean

clean:
	cd ..; rm -rf */__pycache__; rm -f **/*.pyc; rm -rf votechain.egg-info