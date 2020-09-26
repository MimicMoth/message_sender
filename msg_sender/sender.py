from msg_sender.message import Message
from pathlib import Path

class Sender:

    def __init__(self, argv):
        self.msg_list = []
        self.send_message_numbers = []
        self.batch_list = []
        self.argv = argv

    def run():
        self.select_operation_mode(self.argv)

    def execute(self):
        self.read_file()

        for msg in self.msg_list:
#            print(msg.split(';'))
            try:
                message = Message(msg.split(';'))

                if message.validate():
                    self.send_message_numbers.append(message.output())

            except:
                continue

        self.verify_duplicate()

        self.write_msg()

    def read_file(self):
        FILE_PATH = Path.cwd().joinpath('read_in.txt')
        with open(FILE_PATH, 'r') as f:
            self.msg_list = f.read().splitlines()

    def write_msg(self):
        with open('./write_out.txt', 'a') as f:
            f.writelines(map(lambda x: x['final_msg'], self.send_message_numbers))

    def verify_duplicate(self):

        for msg in self.send_message_numbers:
            for msg2 in self.send_message_numbers:
                if msg['phone_number'] == msg2['phone_number'] and msg['sent_time'] < msg2['sent_time']:
                    print(msg2)
                    self.send_message_numbers.remove(msg2)