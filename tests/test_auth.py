# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
test.test_sync
==============

Test functions from pycsync.auth module.
'''
from unittest import TestCase
import os

from pycsync import auth


class MockAuthHandler(object):

    def __init__(self):
        self.verifier = None

    def get_authorization_url(self, prompt):
        return 'url'

    def set_verifier(self, verifier):
        self.verifier = verifier

    def write(self, authfile):
        pass


def mock_input(prompt):
    return 'verifier'


auth.fapi.auth.AuthHandler = MockAuthHandler


class TestAuth(TestCase):
    '''
    Tests for auth module.
    '''
    def setUp(self):
        self.root_dir = os.path.join(os.path.dirname(__file__), 'example_root')

    def test_request_token(self):
        '''
        test_request_token
        '''
        self.assertTrue(auth.request_token(self.root_dir,
                                           input_func=mock_input))
