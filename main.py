import sys

from msg_sender.sender import Sender

sender = Sender(sys.argv[1:])

#sender.execute()

print(sys.argv)