from msg_sender.message import Message
from pathlib import Path

class Sender:
    """
    Controls the flow of the execution
    Accepts two parameters at initialization
    The first is the input file name and the second is the output file name
    If no parameters are passed, it utilizes the standard input.txt and output.txt
    """

    def __init__(self, input = 'input.txt', output = 'output.txt'):
        self._data_list = []
        self._valid_messages = []
        self.input = input
        self.output = output

    def execute(self):
        """
        Executes
        Starts by reading the file, then create an message object that will verify if the message is valid.
        If the message is valid its appended to the valid_message list
        Further it verifies if there are messages to the same number
        Finally it writes the output to a file
        """
        self._read_file()

        for data in self._data_list:
            try:
                message = Message(data.split(';'))
                if message.validate():
                    self._valid_messages.append(message.output())
            except:
                continue

        self._verify_duplicate()
        self._write_msg()

    def _read_file(self):
        """
        Reads the file at the standard input path and add each line as an item into the list data_list
        """
        FILE_PATH = Path.cwd().joinpath(self.input)

        with open(FILE_PATH, 'r') as f:
            self._data_list = f.read().splitlines()

    def _write_msg(self):
        """
        Writes the "output" content accumulated in the valid_messages into the standard output file
        """
        FILE_PATH = Path.cwd().joinpath(self.output)

        with open(FILE_PATH, 'a') as f:
            output_text = map(lambda msg: msg['output'], self._valid_messages)
            f.writelines(output_text)

    def _verify_duplicate(self):
        """
        Verify duplicate messages to the same number and filter to keep only the one with the earliest sent time
        """
        for message in self._valid_messages:
            for verification in self._valid_messages:
                if message['phone_number'] == verification['phone_number'] and message['sent_time'] < verification['sent_time']:
                    self._valid_messages.remove(verification)
