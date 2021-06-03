from distutils.core import setup

setup(
    name='votechain',
    version='0.1',
    description='Secure voting for playlist selection using blockchain',
    author='James Fleming, Uhuru Hashimoto, Joshua Weinbaum, Tommy White and Wendell Wu',
    url='n/a',
    packages=['blockchain', 'p2p', 'voting', 'test'],
    install_requires=[
          'rsa',
          'bitstring'
      ],
)