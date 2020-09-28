import sys

from msg_sender.sender import Sender

if sys.argv[1:] and len(sys.argv[1:]) <= 2:
    sender = Sender(*sys.argv[1:])
else:
    sender = Sender()

sender.execute()