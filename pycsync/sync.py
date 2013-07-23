# vim: set et ts=4 sw=4 fileencoding=utf-8:

import os
import flickr_api

from pycsync import auth

def sync(user):
    auth.set_api_keys()
    a = flickr_api.auth.AuthHandler.load('.pycsync')
    flickr_api.set_auth_handler(a)
    u = flickr_api.Person.findByUserName(user)
    ps = u.getPhotosets()
    current_sets = dict()
    for pset in ps:
        current_sets[pset.title] = pset
    upload(current_sets)


def upload(current_sets):

    dirs = [s for s in os.listdir(os.path.curdir) if os.path.isdir(s)]

    for s in dirs:
        photos = list()
        current_set = current_sets.get(s)
        current_photos = list()
        if current_set:
            set_photos = current_set.getPhotos()
            for photo in set_photos:
                current_photos.append(photo.title)

        files = [p for p in os.listdir(
            os.path.join(os.path.curdir, s)) if os.path.isfile(
                os.path.join(os.path.curdir, s, p))]
        for p in files:
            if not os.path.splitext(p)[0] in current_photos:
                photos.append(flickr_api.upload(photo_file=os.path.join(s, p)))

        if len(photos) > 0:
            if not current_set:
                first_photo = photos[0]
                other_photos = photos[1:]
                set_ = flickr_api.Photoset.create(title=s,
                                                  primary_photo=first_photo)
            else:
                set_ = current_set
                other_photos = photos

            for p in other_photos:
                set_.addPhoto(photo=p)

