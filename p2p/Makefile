# Makefile for easy testing of modules.

PYTHON = python3

# Arguments for client program
# [tracker_address] [tracker_port] [self_port] [mining mode] [key_file]
CLIENT_ARGS = babylon8.thayer.dartmouth.edu 60005 60010

# Rule for running client.

client: client.py
	$(PYTHON) $^ $(CLIENT_ARGS)