# vim: set et ts=4 sw=4 fileencoding=utf-8:

import os
import flickr_api

def sync(user):
    flickr_api.method_call.set_keys('e81b828b075041b2a22b7c1663efc492',
                                    'b1174b27c8cdb649')
    a = flickr_api.auth.AuthHandler.load('.pycsync')
    flickr_api.set_auth_handler(a)
    u = flickr_api.Person.findByUserName(user)
    ps = u.getPhotosets()

    for i,p in enumerate(ps) :
        print i,p.title
    upload()


def upload():

    dirs = [s for s in os.listdir(os.path.curdir) if os.path.isdir(s)]

    photos = list()
    for s in dirs:
        files = [p for p in os.listdir(
            os.path.join(os.path.curdir, s)) if os.path.isfile(
                os.path.join(os.path.curdir, s, p))]
        for p in files:
            photos.append(flickr_api.upload(photo_file=os.path.join(s, p)))

        first_photo = photos[0]
        other_photos = photos[1:]
        set_ = flickr_api.Photoset.create(title=s, primary_photo=first_photo)
        for p in other_photos:
            set_.addPhoto(photo=p)

