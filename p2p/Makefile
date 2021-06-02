# Makefile for easy testing of modules.

PYTHON = python3

# Port numbers
TRACKER_PORT = 60005
LISTEN_PORT = 60009

# Arguments for client program
# -t [tracker_address] -tp [tracker_port] -lp [self_port] -m [mining mode] -mt [timeToMine]
CLIENT_ARGS = -t babylon7.thayer.dartmouth.edu -tp $(TRACKER_PORT) -lp $(LISTEN_PORT) -m T -mt 10

# Arguments for tracker program
# -l [listen_port] -h [hash_padding]
TRACKER_ARGS = $(TRACKER_PORT) -l 2

# Rule for running client.
client: client.py
	clear
	$(PYTHON) $^ $(CLIENT_ARGS)

tracker: tracker.py
	clear
	$(PYTHON) $^ $(TRACKER_ARGS)