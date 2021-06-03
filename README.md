# CS60 Spring 2021 Final Project
# Project Title: Blockchain-based Voting for Music Queueing
## group7 Team members
- Jonah Weinbaum
- James Fleming
- Uhuru Hashimoto
- Thomas White
- Wendell Wu

## Usage
All functionality is handled through the `p2p` files: `tracker.py` and
`client.py`. They are run, respectively, with `make tracker` and
`make client`, with the settings specified by the Makefile.

By default, the tracker takes in the port 60005 (specified by
`TRACKER_PORT` in the Makefile), with a hash_padding of ??

In order to run multiple clients, connect to a single separate
babylon server per client. For example, open an ssh session to
`babylon8.thayer.dartmouth.edu`, and start the tracker on it using
`make tracker`.

Then, open 4 separate ssh sessions to `babylon9-12.thayer.dartmouth.edu`
and run the client program separately on each of them with `make client`,
making sure that the correct `TRACKER_ADDRESS` is used.

On the client programs, there are a few commands you can do:
 - When a poll is active, type `Y` or `N` 

## Assumptions About Input

## Project Structure and Dependencies
### External Project Packages
We depend on the `rsa` module provided by the Python Package Index.
It can be found [here](https://pypi.org/project/rsa/), and should be
installed on the running machine with `pip install rsa` or
`pip3 install rsa` prior to running any of our code.

For mining purposes, we also need `pip3 install bitstring` for bit
operations with our hashes.

We have configured our code such that `pip3 install -e .` should install
the package as well as all dependencies. This is done during the make
procedures.

Alternatively, you can also go into the `p2p` folder and `make setup` to
set up all the imports (it runs the above command).

## Error/Exit Codes and Meaning
Client:
 - exit (1): the tracker went down and the client is exiting.
