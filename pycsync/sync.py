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


def sync(rootdir, dry_run=False):
    '''
    Preform the syncing.

    rootdir
        The root directory to sync.
    '''
    auth.setup_auth_handler(rootdir)
    photosets = _get_photosets()
    download(rootdir, photosets, dry_run=dry_run)
    upload(rootdir, photosets, dry_run=dry_run)


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


def exists_local(rootdir, album_title, photo_title):
    '''
    Check if the given album.photo exists in the rootdir on the local
    filesystem.

    rootdir
        The root directory on the local filesystem

    album_title
        The title of the album to search for.

    photo_title
        The title of the photo to search for.
    '''
    search_path = pjoin(rootdir, album_title, photo_title)
    matches = glob('{0}.*'.format(search_path))
    return True if matches else False


def download(rootdir, current_sets, dry_run=False):
    '''
    Download files from Flickr to ``rootdir``.

    rootdir
        The root directory to sync.

    current_sets
        A dict of PhotoSets by title that are already uploaded.
    '''
    for album in current_sets.values():
        dir_ = pjoin(rootdir, album.title)
        # If the directory does not exists, make it.
        if not isdir(dir_) and not dry_run:
            print 'Creating dir: {0}'.format(album.title)
            mkdir(pjoin(dir_))

        for photo in album.getPhotos():
            if exists_local(rootdir, album.title, photo.title):
                photo.save('{0}.jpg'.format(pjoin(rootdir,
                                                  album.title,
                                                  photo.title)))


def upload(rootdir, current_sets, dry_run=False):
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
                if not dry_run:
                    uploaded_photos.append(fapi.upload(photo_file=pjoin(fulldir,
                                                                        file_)))

        # If we actually uploaded something.
        if len(uploaded_photos) > 0:
            # If the photo set does not exist. Create it. Using the first
            # Photo that was uploaded as the primary photo.
            if not photoset:
                print 'Creating album {0}'.format(dir_)
                first = uploaded_photos[0]
                uploaded_photos = uploaded_photos[1:]
                photoset = fapi.Photoset.create(title=dir_,
                                                primary_photo=first)

            # Finally add any uploaded photo to the set
            for photo in uploaded_photos:
                print 'Adding photo: {0} to album: {1}'.format(dir_,
                                                               photo.title)
                photoset.addPhoto(photo=photo)
