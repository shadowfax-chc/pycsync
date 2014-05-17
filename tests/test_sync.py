# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
test.test_sync
==============

Test functions from pycsync.sync module.
'''
from unittest import TestCase
import os

from pycsync import sync


class TestExistsLocal(TestCase):
    '''
    Tests for test_exists_local
    '''

    def setUp(self):
        self.root_dir = os.path.join(os.path.dirname(__file__), 'example_root')

    def test_exist(self):
        '''
        test_exist
        '''
        exists = sync.exists_local(self.root_dir, 'album1', 'photo1')
        self.assertTrue(exists)

    def test_does_not_exist_photo(self):
        '''
        test_does_not_exist_photo
        '''
        exists = sync.exists_local(self.root_dir, 'album1', 'no_photo')
        self.assertFalse(exists)

    def test_does_not_exist_album(self):
        '''
        test_does_not_exist_album
        '''
        exists = sync.exists_local(self.root_dir, 'no_album1', 'photo1')
        self.assertFalse(exists)
