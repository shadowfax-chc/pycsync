# vim: set et ts=4 sw=4 fileencoding=utf-8:

import argparse

from pycsync import version, auth, sync

def pycsync_main():
    parser = argparse.ArgumentParser(description='Sync pictures with Flickr.')
    parser.add_argument('username',
                        help='Flickr username')
    parser.add_argument('-a', '--auth',
                        action='store_true',
                        default=False,
                        help='Request authorization token')
    parser.add_argument('-v', '--version',
                        action='store_true',
                        default=False,
                        help='Display pycsync version')
    args = parser.parse_args()
    if args.version:
        print version.__version__
    elif args.auth:
        auth.request_token()
    else:
        sync.sync(args.username)
