# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
test.test_sync
==============

Test functions from pycsync.sync module.
'''
from unittest import TestCase
import os

from pycsync import sync


class MockPhoto(object):

    def __init__(self, title):
        self.title = title

    def save(self, file_path):
        pass


class MockPhotoSet(object):

    def __init__(self, title, photos):
        self.title = title
        self.photos = photos

    def getPhotos(self):
        return self.photos

    def addPhoto(self, photo):
        self.photos.append(photo)

    @classmethod
    def create(cls, title, primary_photo):
        return MockPhotoSet(title, [primary_photo])


sync.fapi.Photoset = MockPhotoSet


class TestSync(TestCase):
    '''
    Tests for sync module.
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

    def test_download(self):
        '''
        test_download
        '''
        albums = {'album1': MockPhotoSet('album1', [MockPhoto('photo1'),
                                                    MockPhoto('photo2')])}
        downloaded = sync.download(self.root_dir, albums)
        self.assertEqual(downloaded, 1)

    def test_populate_album(self):
        '''
        test_populate_album
        '''
        mock_album = MockPhotoSet('album1', [])
        mock_photos = [MockPhoto('photo1'), MockPhoto('photo2')]
        added = sync.populate_album(mock_album, mock_photos)
        self.assertEqual(added, 2)
        self.assertEqual(2, len(mock_album.photos))

    def test_create_album(self):
        '''
        test_create_album
        '''
        title = 'album1'
        mock_photo = MockPhoto('photo1')
        album = sync.create_album(title, mock_photo)
        self.assertEqual(title, album.title)
