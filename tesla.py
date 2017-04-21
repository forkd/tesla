#!/usr/bin/env python3
#tesla.py
#
# Copyright 2017 José Lopes de Oliveira Jr.
#
# Use of this source code is governed by a MIT-like
# license that can be found in the LICENSE file.
##


'''
Retrives the message inside a file exported by Outlook (file.msg).
Based on:
https://github.com/mattgwwalker/msg-extractor (ExtractMsg.py)

'''

__author__ = 'José Lopes de Oliveira Jr.'


import re
import sys
import olefile as of


def win_unicode(string):
    if string is None:
        return None
    return str(string, 'utf_16_le')


class Message(of.OleFileIO):
    '''
    Parses a .msg file allowing to retrieve the PGP message inside it.

    Args:
        - f (str): the path to .msg file.

    '''

    def __init__(self, f):
        of.OleFileIO.__init__(self, f)
        # Regex: . doesn't match \n and \r
        self.regex = re.compile(r'-----BEGIN PGP MESSAGE-----(.|\n|\r)*-----END PGP MESSAGE-----')  

    def _get_stream(self, f):
        if self.exists(f):
            stream = self.openstream(f)
            return stream.read()
        else:
            return None

    def _get_str_stream(self, f, prefer='unicode'):
        '''Gets a string representation of the requested filename.
        
        Checks for both ASCII and Unicode representations and returns
        a value if possible.  If there are both ASCII and Unicode
        versions, then the parameter /prefer/ specifies which will be
        returned.

        '''

        if isinstance(f, list):
            # Join with slashes to make it easier to append the type
            f = "/".join(f)

        ascii_version = self._get_stream(f + '001E')
        unicode_version = win_unicode(self._get_stream(f + '001F'))

        if ascii_version is None:
            return unicode_version
        elif unicode_version is None:
            return ascii_version
        else:
            if prefer == 'unicode':
                return unicode_version
            else:
                return ascii_version

    def get_pgp_msg(self):
        return re.search(self.regex, 
            self._get_str_stream('__substg1.0_1000')).group(0)


if __name__ == '__main__':
    print(Message(sys.argv[1]).get_pgp_msg())

