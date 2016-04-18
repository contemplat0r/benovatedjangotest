import json
from django.test import TestCase
from django.test import Client
from django.template import Context, Template
from accounts.models import UserAccount
from decimal import Decimal, ROUND_HALF_DOWN, ROUND_DOWN



# Create your tests here.


class SimpleTransferViewGetTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_response(self):

        '''
        Simple tests that check response HTTP code,
        right template presence, and presence some string in rendered html.
        '''
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/transfer.html')
        self.assertContains(response, 'class="container"')


class UserAccountTest(TestCase):

    fixtures = ['dbdata.json']

    def setUp(self):
        pass

    def test_model_data_presence(self):

        '''
        Tests that check correct data presence in database
        '''

        user_account = UserAccount.objects.get(pk=1)
        self.assertEqual(user_account.ammount >= 0, True)
        self.assertEqual(user_account.itn != '', True)

    def test_str_method(self):

        '''
        Check the correctness of str method.
        '''

        user_account = UserAccount.objects.get(pk=1)
        self.assertEqual(str(user_account),
            '%s %s' % (user_account.user.username, user_account.itn))


class TransferRequestProcessingTest(TestCase):
    fixtures = ['dbdata.json']

    def setUp(self):
        self.client = Client()
        self.user_account = UserAccount.objects.get(pk=1)
    
    
    def test_correct_input_data(self):
        '''
        All data is correct: itn valid, accounts from which transfered exists
        transfered sum is correct.
        '''
        transfer_sum = Decimal((self.user_account.ammount / 10).quantize(Decimal('.00'), rounding=ROUND_HALF_DOWN))
        response = self.client.post('/', {'users' : 'User_1', 'itn' : '1111111112', 'transfer_sum': transfer_sum}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(response.content)
        self.assertEqual(content['success'], True)

    def test_incorrect_decimal_digits(self):
        '''
        Incorrect number decimal digiths in transfered sum
        '''
        transfer_sum = self.user_account.ammount / 10
        response = self.client.post('/', {'users' : 'User_1', 'itn' : '1111111112', 'transfer_sum': transfer_sum}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(response.content)
        self.assertEqual(content['success'], False)

    def test_invalid_itn(self):
        '''
        Itn not valid (too long). 
        '''
        transfer_sum = Decimal((self.user_account.ammount / 10).quantize(Decimal('.00'), rounding=ROUND_HALF_DOWN))
        response = self.client.post('/', {'users' : 'User_1', 'itn' : '111111111200000', 'transfer_sum': transfer_sum}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(response.content)
        self.assertEqual(content['success'], False)

    def test_incorrect_transfer_sum(self):
        '''
        Transfer sum exceeds account ammount. 
        '''
        transfer_sum = Decimal((self.user_account.ammount + 1).quantize(Decimal('.00'), rounding=ROUND_HALF_DOWN))
        response = self.client.post('/', {'users' : 'User_1', 'itn' : '111111111200000', 'transfer_sum': transfer_sum}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(response.content)
        self.assertEqual(content['success'], False)

    def test_nonexistent_itn(self):
        '''
        None account with that itn
        '''
        transfer_sum = Decimal((self.user_account.ammount + 1).quantize(Decimal('.00'), rounding=ROUND_HALF_DOWN))
        response = self.client.post('/', {'users' : 'User_1', 'itn' : '2222222222', 'transfer_sum': transfer_sum}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        content = json.loads(response.content)
        self.assertEqual(content['success'], False)
