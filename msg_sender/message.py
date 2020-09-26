import re
from datetime import time
from requests import get
from typing import List

class Message:

    DDD_LIST = {
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
    DDD_SP = {
        11, 12, 13, 14, 15, 16, 17, 18, 19,
    }

    DDD_VALID_LIST = DDD_LIST - DDD_SP

    BLACK_LIST_ENDPOINT = 'https://front-test-pg.herokuapp.com/blacklist/'

    ID_BROKER = (
        ('1', ('VIVO', 'TIM')),
        ('2', ('CLARO', 'OI')),
        ('3', ('NEXTEL',))
    )

    def __init__(self, info):
        self.info = info

    @property
    def content(self):
        return {
            'id_mensagem' : self.info[0],
            'ddd' : self.info[1],
            'celular' : self.info[2],
            'operadora' : self.info[3],
            'horario_envio' : self.info[4],
            'mensagem' : self.info[5],
        }

    def validate(self) -> bool:
        return (self.valid_phone() and
                self.valid_msg() and
                self.valid_time())

    def valid_phone(self) -> bool:
        phone_validator = re.compile('9[6-9]\d{7}$')
        valid_number = re.findall(phone_validator, self.content['celular'])
        valid_ddd = len(self.content['ddd']) == 2 and int(self.content['ddd']) in self.DDD_VALID_LIST
        blacklist = self.check_blacklist()

        if valid_number and valid_ddd and not blacklist:
            return True

        return False

    def check_blacklist(self) -> bool:
        phone_number = self.content['ddd'] + self.content['celular']
        response = get(self.BLACK_LIST_ENDPOINT + phone_number)

        print(self.BLACK_LIST_ENDPOINT + phone_number, response.status_code)

        if response.status_code == 200:
            return True

        return False

    def valid_msg(self) -> bool:
        if len(self.content['mensagem']) <= 140:
            return True

        return False

    def valid_time(self) -> bool:
        hour = int(self.content['horario_envio'].split(':')[0])

        if hour < 20:
            return True

        return False

    def output(self) -> str:
        broker = self.find_broker()
        final_msg = ';'.join([self.content['id_mensagem'], broker]) + '\n'
        phone_number = self.content['ddd'] + self.content['celular']
        sent_time_details = self.content['horario_envio'].split(':')
        sent_time = time(int(sent_time_details[0]), int(sent_time_details[1]), int(sent_time_details[2]))

        answer = {
            'final_msg': final_msg,
            'phone_number': phone_number,
            'sent_time': sent_time,
        }

        return answer

    def find_broker(self) -> str:
        for broker in self.ID_BROKER:
            for broker_name in broker[1]:
                if self.content['operadora'] == broker_name:
                    return broker[0]
