from unittest import TestCase, main
from datetime import time

from msg_sender.message import Message
from msg_sender.sender import Sender

class MessageSenderTester(TestCase):

    def setUp(self):
        self.ddd_3_digits = Message(['01', '041', '0', '0','0', 'ddd com 3 digitos'])
        self.invalid_ddd = Message(['02', '23', '0', '0', '0', 'ddd invalido'])
        self.msg_to_sp = Message(['03', '11', '986547552', '0', '0', 'mensagem para sao paulo'])
        self.valid_ddd = Message(['04', '41', '986547552', '0', '0', 'ddd valido'])

        self.phone_more_than_9_digits = Message(['05', '0', '9834512578', '0', '0', 'celular com mais de 9 digitos'])
        self.phone_less_than_9_digits = Message(['06', '0', '98345127', '0', '0', 'celular com menos de 9 digitos'])
        self.phone_doesnt_start_with_9 = Message(['07', '0', '684752198', '0', '0', 'celular nao começa com 9'])
        self.second_digit_smaller_than_6 = Message(['08', '0', '957845782', '0', '0', 'segundo digito menor que 6'])
        self.valid_number = Message(['09', '0', '970636588', '0', '0', 'numero valido'])

        self.number_in_blacklist = Message(['10', '68', '960636588', '0', '0', 'numero na blacklist'])
        self.number_not_in_blacklist = Message(['11', '68', '970636588', '0', '0', 'numero fora da blacklist'])

        self.msg_after_20h = Message(['12', '0', '0', '0', '20:00:00', 'mensagem apos as 20h'])
        self.valid_time = Message(['13', '0', '0', '0', '19:59:59', 'horario valido'])

        self.message_higher_than_140_characteres = Message(['14', '0', '0', '0', '0', """mensagem com mais de 140 caracteres mensagem com mais de
        140 caracteres mensagem com mais de 140 caracteres mensagem com mais de 140 caracteres mensagem com mais de 140 caracteres mensagem com
        mais de 140 caracteres mensagem com mais de 140 caracteres mensagem com mais de 140 caracteres mensagem com mais de 140 caracteres mensagem
        com mais de 140 caracteres mensagem com mais de 140"""])
        self.valid_message = Message(['15', '0', '0', '0', '0', 'mensagem valida'])

        self.invalid_broker = Message(['16', '0', '0', 'TELSTRA', '0', 'operadora invalida'])
        self.valid_broker = Message(['17', '0', '0', 'TIM', '0', 'operadora valida'])

        self.valid_output = Message(['18', '41', '995965773', 'TIM', '14:31:46', 'teste de saída'])

        self.same_numbers = Sender()
        self.same_numbers._valid_messages = [
            {'output': 'a', 'phone_number': '41995965773', 'sent_time': time(9, 15, 23)},
            {'output': 'b', 'phone_number': '41995965773', 'sent_time': time(6, 40, 6)},
            {'output': 'c', 'phone_number': '41995965773', 'sent_time': time(15, 32, 41)},
        ]


    def test_ddd_cases(self):
        self.assertFalse(self.ddd_3_digits._valid_ddd())
        self.assertFalse(self.invalid_ddd._valid_ddd())
        self.assertFalse(self.msg_to_sp._valid_ddd())
        self.assertTrue(self.valid_ddd._valid_ddd())

    def test_phone_cases(self):
        self.assertFalse(self.phone_more_than_9_digits._valid_number())
        self.assertFalse(self.phone_less_than_9_digits._valid_number())
        self.assertFalse(self.phone_doesnt_start_with_9._valid_number())
        self.assertFalse(self.second_digit_smaller_than_6._valid_number())
        self.assertTrue(self.valid_number._valid_number())

    def test_blacklist_cases(self):
        self.assertTrue(self.number_in_blacklist._check_blacklist())
        self.assertFalse(self.number_not_in_blacklist._check_blacklist())

    def test_time_cases(self):
        self.assertFalse(self.msg_after_20h._valid_time())
        self.assertTrue(self.valid_time._valid_time())

    def test_message_cases(self):
        self.assertFalse(self.message_higher_than_140_characteres._valid_msg())
        self.assertTrue(self.valid_message._valid_msg())

    def test_broker_cases(self):
        self.assertEqual(self.invalid_broker._find_broker(), None)
        self.assertEqual(self.valid_broker._find_broker(), '1')

    def test_output(self):
        self.assertEqual(self.valid_output.output(), {'output' : '18;1\n', 'phone_number': '41995965773', 'sent_time': time(14,31,46)})

    def test_multiple_messages_to_same_number(self):
        self.same_numbers._verify_duplicate()
        self.assertEqual(self.same_numbers._valid_messages, [{'output': 'b', 'phone_number': '41995965773', 'sent_time': time(6, 40, 6)}])


if __name__ == '__main__':
    main()