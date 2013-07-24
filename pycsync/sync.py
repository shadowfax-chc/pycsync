# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
pycsync.sync
============

Module where the magic happens. Functions here are used for uploading and
downloading files/sets to and from Flickr.
'''

from os import listdir
from os.path import splitext, isdir, isfile, join as pjoin
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
    #download
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

        # Attempt to get the set that would match this dir.
        photoset = current_sets.get(dir_)
        if photoset:
            # Set already exists. Get all photos in set by title.
            for photo in photoset.getPhotos():
                uploaded_photos.append(photo.title)

        # Get all the files in this dir.
        fulldir = pjoin(rootdir, dir_)
        files = [file_ for file_ in listdir(fulldir) if isfile(pjoin(fulldir,
                                                                     file_))]

        # Upload new files. Storing the returned Photo in uploaded_photos.
        for file_ in files:
            if not splitext(file_)[0] in uploaded_photos:
                uploaded_photos.append(fapi.upload(photo_file=pjoin(fulldir,
                                                                    file_)))

        # If we actually uploaded something.
        if len(uploaded_photos) > 0:
            # If the photo set does not exist. Create it. Using the first
            # Photo that was uploaded as the primary photo.
            if not photoset:
                first = uploaded_photos[0]
                uploaded_photos = uploaded_photos[1:]
                photoset = fapi.Photoset.create(title=dir_,
                                                primary_photo=first)

            # Finally add any uploaded photo to the set
            for photo in uploaded_photos:
                photoset.addPhoto(photo=photo)
