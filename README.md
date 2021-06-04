# CS60 Spring 2021 Final Project
# Project Title: Blockchain-based Voting for Music Queueing
## group7 Team members
- Jonah Weinbaum
- James Fleming
- Uhuru Hashimoto
- Thomas White
- Wendell Wu

## Presentation
We have live demo videos in `TESTING.md`, and here are the slides used
for the final presentation held on 6/4/21:
https://docs.google.com/presentation/d/1X6jwifSTiaHRHU0DOie0fw7vjMd3_Ui6SpBNKPgLvtI/edit#slide=id.ge0280943e3_2_17

(Also linked here as a hyperlink)[https://docs.google.com/presentation/d/1X6jwifSTiaHRHU0DOie0fw7vjMd3_Ui6SpBNKPgLvtI/edit#slide=id.ge0280943e3_2_17]

## Usage
All functionality is handled through the `p2p` files: `tracker.py` and
`client.py`. They are run, respectively, with `make tracker` and
`make client`, with the settings specified by the Makefile.

The very first thing that should be done is to navigate to the `p2p`
folder. The project depenencies can be set up by running `make setup`. This installs
all project interdependencies and all external packages. If, for any reason,
installing external packages fails, you can use `pip3 install [package]` to
separately install them. See (external project packages)[#external-project-packages]
for info about those packages.

By default, the tracker takes in the port 60005 (specified by
`TRACKER_PORT` in the Makefile), with a hash_padding of 16 bits.

In order to run multiple clients, connect to a single separate
babylon server per client.

To start the tracker ssh into
`babylon8.thayer.dartmouth.edu`, and start the tracker on it using
`make tracker`. The tracker address is set to babylon8 by default
in the makefile, and is configurable via the `TRACKER_ADDRESS`
variable in the makefile.

Then, open 4 separate ssh sessions to `babylon9-12.thayer.dartmouth.edu`
and run the client program separately on each of them with `make client` or `make miner`,
each of which signifies that the console is either non-mining or mining respectively.

On the client programs, there are a few commands you can do:
 - When a poll is active, type `Y` or `N`to vote
 - At any time, you can type `PRINT` to display the whole blockchain
 - At any time, you can type `TALLY` to tally the votes for the poll cycle
 - If there is no active poll, `TALLY` and the `Y/N` votes will not do anything
 - To exit the client, type `EXIT`

On the tracker program, there are a few commands as well:
- To start a poll, simply type the song name into the console and it will be sent to all peers
- At any time, type `END` to end an ongoing poll
- To exit the tracker, type `EXIT`

## Project Structure and Dependencies
This is the breakdown of our project directory:
```
project-music-queue
|	README.md
|	DESIGN.md
|   TESTING.md
|	setup.py
|	.gitignore
+---blockchain
|	|	__init__.py
|	|	blockchain.py
|	|	block.py
|	|	entry.py
+---p2p
|	|   __init__.py
|	|	client.py
|	|	tracker.py
|	|   Makefile
+---test
|	|	__init__.py
|	|	test_block.py
|	|   test_blockchain.py
|	|   test_entry.py
+---voting
|	|	__init__.py
|	|   poll.py
|	|   tally.py
```
Each of the `__init__.py` files is used during the `make setup` process
to establish inter-module dependencies.

All of the rest of the python files are documented with header comments
and in-line comments.

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
