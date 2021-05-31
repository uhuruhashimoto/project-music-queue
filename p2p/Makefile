# Makefile for easy testing of modules.

PYTHON = python3

# Arguments for client program
# [tracker_address] [tracker_port] [self_port] [mining mode] [key_file]
CLIENT_ARGS = babylon7.thayer.dartmouth.edu 60005 60010

# Arguments for tracker program
# [hash_padding] [cycle_config] [timeout]
TRACKER_ARGS = 2

# Rule for running client.
client: client.py
	$(PYTHON) $^ $(CLIENT_ARGS)

tracker: tracker.py
	$(PYTHON) $^ $(TRACKER_ARGS)