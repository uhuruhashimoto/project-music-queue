# Makefile for easy testing of modules.

PYTHON = python3

# Port numbers
<<<<<<< HEAD
TRACKER_PORT = 60006

# Arguments for client program
# [tracker_address] [tracker_port] [self_port] [mining mode] [timeToMine]
CLIENT_ARGS = babylon7.thayer.dartmouth.edu $(TRACKER_PORT) 60009 T 5

# Arguments for tracker program
# [hash_padding] [cycle_config] [timeout]
TRACKER_ARGS = $(TRACKER_PORT) 4
=======
TRACKER_PORT = 60005
LISTEN_PORT = 60009

# Arguments for client program
# -t [tracker_address] -tp [tracker_port] -lp [self_port] -m [mining mode] -mt [timeToMine]
CLIENT_ARGS = -t babylon7.thayer.dartmouth.edu -tp $(TRACKER_PORT) -lp $(LISTEN_PORT) -m T -mt 10

# Arguments for tracker program
# -l [listen_port] -h [hash_padding]
TRACKER_ARGS = $(TRACKER_PORT) -l 2
>>>>>>> 1bc4c2ab11e736876b99f2e50be4462df67f30e2

# Rule for running client.
client: client.py
	clear
	$(PYTHON) $^ $(CLIENT_ARGS)

tracker: tracker.py
	clear
	$(PYTHON) $^ $(TRACKER_ARGS)