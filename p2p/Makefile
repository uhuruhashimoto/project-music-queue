# Makefile for easy testing of modules.

PYTHON = python3

# Port numbers
TRACKER_PORT = 60006

# Arguments for client program
# [tracker_address] [tracker_port] [self_port] [mining mode] [timeToMine]
CLIENT_ARGS = babylon7.thayer.dartmouth.edu $(TRACKER_PORT) 60009 T 5

# Arguments for tracker program
# [hash_padding] [cycle_config] [timeout]
TRACKER_ARGS = $(TRACKER_PORT) 4

# Rule for running client.
client: client.py
	clear
	$(PYTHON) $^ $(CLIENT_ARGS)

tracker: tracker.py
	clear
	$(PYTHON) $^ $(TRACKER_ARGS)