# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
pycsync.sync
============

Module where the magic happens. Functions here are used for uploading and
downloading files/sets to and from Flickr.
'''

from os import listdir, mkdir
from os.path import splitext, isdir, isfile, join as pjoin
from glob import glob
import flickr_api as fapi

from pycsync import auth


def sync(rootdir):
    '''
    Preform the syncing.

    rootdir
        The root directory to sync.
    '''
    auth.setup_auth_handler(rootdir)
    photosets = _get_photosets()
    download(rootdir, photosets)
    upload(rootdir, photosets)


def _get_photosets():
    '''
    Gets the flickr_api.Photoset objects for the authorized user.

    Returns a dict of Photosets by set title.
    '''
    user = fapi.test.login()
    photosets = user.getPhotosets()
    current_sets = dict()
    for pset in photosets:
        current_sets[pset.title] = pset
    return current_sets


def download(rootdir, current_sets):
    '''

    rootdir
        The root directory to sync.

    current_sets
        A dict of PhotoSets by title that are already uploaded.
    '''
    for photoset in current_sets.values():
        dir_ = pjoin(rootdir, photoset.title)
        # If the directory does not exists, make it.
        if not isdir(dir_):
            print 'Creating dir: {0}'.format(photoset.title)
            mkdir(pjoin(dir_))

        for photo in photoset.getPhotos():
            # Name of file without extension, since Flickr does not include it.
            file_ = pjoin(dir_, photo.title)

            # Due to lack of extension, need to glob for filename.
            matching = glob('{0}.*'.format(file_))

            # If no file with this name, download this photo.
            if not matching:
                msg = 'Downloading photo: {0} to set: {1}'
                print msg.format(photo.title, photoset.title)
                photo.save('{0}.jpg'.format(file_))


def upload(rootdir, current_sets):
    '''
    Upload files from the ``rootdir`` to Flickr. It will create a PhotoSet for
    each directory in ``rootdir``. It will upload each file in a directory
    and add it to the set. If a set already exists, it will be reused and new
    photos will be added to it. If a file is already uploaded to the PhotoSet,
    it will be skipped.

    rootdir
        The root directory to sync.

    current_sets
        A dict of PhotoSets by title that are already uploaded.
    '''

    dirs = [dir_ for dir_ in listdir(rootdir) if isdir(pjoin(rootdir, dir_))]

    for dir_ in dirs:
        files = list()
        uploaded_photos = list()
        current_photos = list()

        # Attempt to get the set that would match this dir.
        photoset = current_sets.get(dir_)
        if photoset:
            # Set already exists. Get all photos in set by title.
            for photo in photoset.getPhotos():
                current_photos.append(photo.title)

        # Get all the files in this dir.
        fulldir = pjoin(rootdir, dir_)
        files = [file_ for file_ in listdir(fulldir) if isfile(pjoin(fulldir,
                                                                     file_))]

        # Upload new files. Storing the returned Photo in uploaded_photos.
        for file_ in files:
            if not splitext(file_)[0] in current_photos:
                print 'Uploading photo: {0}'.format(file_)
                uploaded_photos.append(fapi.upload(photo_file=pjoin(fulldir,
                                                                    file_)))

        # If we actually uploaded something.
        if len(uploaded_photos) > 0:
            # If the photo set does not exist. Create it. Using the first
            # Photo that was uploaded as the primary photo.
            if not photoset:
                print 'Creating photoset {0}'.format(dir_)
                first = uploaded_photos[0]
                uploaded_photos = uploaded_photos[1:]
                photoset = fapi.Photoset.create(title=dir_,
                                                primary_photo=first)

            # Finally add any uploaded photo to the set
            for photo in uploaded_photos:
                print 'Adding photo: {0} to photoset: {1}'.format(dir_,
                                                                  photo.title)
                photoset.addPhoto(photo=photo)
