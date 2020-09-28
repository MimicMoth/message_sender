import re
from datetime import time
from requests import get

class Message:
    """
    Message class
    Contains the set of valid DDDs, the blacklist endpoint and the broker and its respectives ids.
    When initialized it sets up a descriptor as a dictionary with the essential information about the messages.
    It validates the message format and information and returns the valid output string to be written in the file.
    """

    _DDD_LIST = {
        11, 12, 13, 14, 15, 16, 17, 18, 19,
        21, 22, 24, 27, 28,
        31, 32, 33, 34, 35, 37, 38,
        41, 42, 43, 44, 45, 46, 47, 48, 49,
        51, 53, 54, 55,
        61, 62, 63, 64, 65, 66, 67, 68, 69,
        71, 73, 74, 75, 77, 79,
        81, 82, 83, 84, 85, 86, 87, 88, 89,
        91, 92, 93, 94, 95, 96, 97, 98, 99,
        }
    _DDD_SP = {
        11, 12, 13, 14, 15, 16, 17, 18, 19,
    }

    _DDD_VALID_LIST = _DDD_LIST - _DDD_SP

    _BLACK_LIST_ENDPOINT = 'https://front-test-pg.herokuapp.com/blacklist/'

    _ID_BROKER = (
        ('1', ('VIVO', 'TIM')),
        ('2', ('CLARO', 'OI')),
        ('3', ('NEXTEL',)),
    )

    def __init__(self, info):
        self.info = info

    @property
    def content(self):
        return {
            'id_message' : self.info[0],
            'ddd' : self.info[1],
            'phone' : self.info[2],
            'broker' : self.info[3],
            'sent_time' : self.info[4],
            'message' : self.info[5],
        }

    def validate(self) -> bool:
        """
        Calls the validate functions
        Returns a boolean.
        """
        return (self._valid_phone() and
                self._valid_msg() and
                self._valid_time())

    def _valid_phone(self) -> bool:
        """
        Call the valid_number, valid_ddd and check_blacklist functions to verify all the number conditions

        Returns a boolean.
        """
        valid_number = self._valid_number()

        valid_ddd = self._valid_ddd()

        blacklist = self._check_blacklist()

        if valid_number and valid_ddd and not blacklist:
            return True

        return False

    def _valid_ddd(self) -> bool:
        """
        Verifies if the ddd has 2 digits and is in the valid ddd list

        Returns a boolean
        """
        return len(self.content['ddd']) == 2 and int(self.content['ddd']) in self._DDD_VALID_LIST

    def _valid_number(self) -> bool:
        """
        Verifies if the phone has the valid format:
        - starts with 9
        - second digit is higher than 6
        - has 9 digits

        Return a boolean
        """
        phone_validator = re.compile('9[7-9]\d{7}$')
        return re.findall(phone_validator, self.content['phone'])

    def _check_blacklist(self) -> bool:
        """
        Check if the number is in the blacklist by calling the api.
        if the status code is 200 it's in the blacklist.
        Returns a boolean.
        """
        phone_number = self.content['ddd'] + self.content['phone']
        response = get(self._BLACK_LIST_ENDPOINT + phone_number)

        if response.status_code == 200:
            return True

        return False

    def _valid_msg(self) -> bool:
        """
        Verify if the length of the message is higher than 140 characteres.
        Returns a boolean.
        """
        if len(self.content['message']) <= 140:
            return True

        return False

    def _valid_time(self) -> bool:
        """
        Verify if the message was sent latter than 19:59:59 by analyzing the hour component.
        Returns a boolean
        """
        hour = int(self.content['sent_time'].split(':')[0])

        if hour < 20:
            return True

        return False

    def output(self) -> str:
        """
        Builds the output dictionary.
        It contains the output to be written with the id_message and broker_id.
        The phone number of the respective message
        The time as a time time object

        Returns a dictionary.
        """
        broker = self._find_broker()
        final_output = ';'.join([self.content['id_message'], broker]) + '\n'

        phone_number = self.content['ddd'] + self.content['phone']

        sent_time_details = self.content['sent_time'].split(':')
        sent_time = time(int(sent_time_details[0]), int(sent_time_details[1]), int(sent_time_details[2]))

        answer = {
            'output': final_output,
            'phone_number': phone_number,
            'sent_time': sent_time,
        }

        return answer

    def _find_broker(self) -> str:
        """
        Check the broker in the content and returns the brokers id.
        """
        for broker in self._ID_BROKER:
            for broker_name in broker[1]:
                if self.content['broker'] == broker_name:
                    return broker[0]
