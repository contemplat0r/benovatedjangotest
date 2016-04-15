from django.test import TestCase
from django.test import Client
#from mission.models import PersonDescription
#from mission.models import Request
from django.template import Context, Template

# Create your tests here.


class ResponseDescriptionViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_response(self):

        '''
        Simple tests that check response HTTP code correctnes,
        right template presence, and presence some string in rendered html.
        '''
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/transfer.html')
        self.assertContains(response, 'class="container"')


class UserAccountTest(TestCase):

    def setUp(self):
        pass

    def test_model_data_presence(self):

        '''
        Tests that check correct data presence in database
        '''

        user_account = UserAccount.objects.get(pk=1)
        self.assertEqual(user_account.sum >= 0, True)
        self.assertEqual(user_account.inn != '', True)

    def str_method(self):

        '''
        Check the correctness of str method.
        '''

        user_account = UserAccount.objects.get(pk=1)
        self.assertEqual(str(user_account),
            '%s %s' % (user_account.user.name, user_account.inn))

