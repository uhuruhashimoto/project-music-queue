# Makefile for easy testing of modules.

PYTHON = python3

# Port numbers
TRACKER_PORT = 60007

# Arguments for client program
# [tracker_address] [tracker_port] [self_port] [mining mode] [key_file]
CLIENT_ARGS = babylon8.thayer.dartmouth.edu $(TRACKER_PORT) 60008 F 30

# Arguments for tracker program
# [hash_padding] [cycle_config] [timeout]
TRACKER_ARGS = $(TRACKER_PORT) 2

# Rule for running client.
client: client.py
	clear
	$(PYTHON) $^ $(CLIENT_ARGS)

tracker: tracker.py
	clear
	$(PYTHON) $^ $(TRACKER_ARGS)