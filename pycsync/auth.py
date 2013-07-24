# vim: set et ts=4 sw=4 fileencoding=utf-8:
'''
pycsync.auth
============

Module for authentication related functions.
'''

import os
import flickr_api

def request_token(rootdir):
    '''
    Request an auth token. Prompt the user to accept the client API key and
    submit a verifier code. Then record out the auth file to ``rootdir``.

    rootdir
        The root directory to sync.
    '''
    set_api_keys()
    authfile = os.path.join(rootdir, '.pycsync')
    prompt = 'Please visit to get an verifier code:\n' \
             '---------------------------------\n' \
             '{0}\n' \
             '---------------------------------\n' \
             'Please input the verifier code here: '
    a = flickr_api.auth.AuthHandler()
    url = a.get_authorization_url('write')
    verifier = raw_input(prompt.format(url))
    a.set_verifier(str(verifier))
    a.write(authfile)


def setup_auth_handler(rootdir):
    '''
    Set up the auth handler using the authfile in ``rootdir``

    rootdir
        The root directory to sync.
    '''
    set_api_keys()
    authfile = os.path.join(rootdir, '.pycsync')
    flickr_api.set_auth_handler(authfile)


def set_api_keys():
    '''
    Set up the client api keys.
    '''
    flickr_api.keys.set_keys('e81b828b075041b2a22b7c1663efc492',
                             'b1174b27c8cdb649')
