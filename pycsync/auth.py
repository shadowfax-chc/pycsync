# vim: set et ts=4 sw=4 fileencoding=utf-8:

import flickr_api

def request_token():
    prompt = 'Please visit to get an verifier code:\n' \
             '---------------------------------\n' \
             '{0}\n' \
             '---------------------------------\n' \
             'Please input the verifier code here: '
    flickr_api.method_call.set_keys('e81b828b075041b2a22b7c1663efc492',
                                    'b1174b27c8cdb649')
    a = flickr_api.auth.AuthHandler()
    url = a.get_authorization_url('write')
    verifier = raw_input(prompt.format(url))
    a.set_verifier(str(verifier))
    a.write('.pycsync')

