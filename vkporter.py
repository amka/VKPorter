#!/usr/bin/env python

"""
    :mod:`vkporter`
    ~~~~~~~~~~~~~~~

    A micro tool for export photo albums from `vk.com <https://vk.com>`_.
     It's based on `VK_API <https://github.com/python273/vk_api>`_
     by Kirill Python <mikeking568@gmail.com>,
     `Requests <python-requests.org>`_
     and `ProgressBar <https://code.google.com/p/python-progressbar/>`_.

    :copyright: (c) 2013 by Andrey Maksimov.
    :license: BSD, see LICENSE for more details.
"""
__author__ = 'Andrey Maksimov <meamka@me.com>'
__date__ = '09.03.13'
__version__ = '0.1.1'

import argparse
import datetime
import os
import time
import sys

try:
    import requests
except ImportError:
    print("Cannot find 'requests' module. Please install it and try again.")
    sys.exit(0)

try:
    from vk_api import VkApi
except ImportError:
    print("Cannot find 'vk_api' module. Please install it and try again.")
    sys.exit(0)


def connect(login, password):
    """Initialize connection with `vk.com <https://vk.com>`_ and try to authorize user with given credentials.

    :param login: user login e. g. email, phone number
    :type login: str
    :param password: user password
    :type password: str

    :return: :mod:`vk_api.vk_api.VkApi` connection
    :rtype: :mod:`VkApi`
    """
    return VkApi(login, password)


def get_albums(connection):
    """Get albums list for currently authorized user.

    :param connection: :class:`vk_api.vk_api.VkApi` connection
    :type connection: :class:`vk_api.vk_api.VkApi`

    :return: list of photo albums or ``None``
    :rtype: list
    """
    try:
        return connection.method('photos.getAlbums')
    except Exception as e:
        print(e)
        return None


def get_photos(connection, album_id):
    """Get photos list for selected album.

    :param connection: :class:`vk_api.vk_api.VkApi` connection
    :type connection: :class:`vk_api.vk_api.VkApi`
    :param album_id: album identifier returned by :func:`get_albums`
    :type album_id: int

    :return: list of photo albums or ``None``
    :rtype: list
    """
    try:
        return connection.method('photos.get', {'aid': album_id})
    except Exception as e:
        print(e)
        return None


def download(photo, output):
    """Download photo

    :param photo:
    """
    url = photo.get('src_xxxbig') or photo.get('src_xxbig') or photo.get('src_xbig') or photo.get('src_big')

    r = requests.get(url)
    title = photo['pid']
    with open(os.path.join(output, '%s.jpg' % title), 'wb') as f:
        for buf in r.iter_content(1024):
            if buf:
                f.write(buf)


def sizeof_fmt(num):
    """Small function to format numbered size to human readable string

    :param num: bytes to format
    :type num: int

    :return: human readable size
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


if __name__ == '__main__':

    # Connect to vk.com
    # Get list of user albums
    # For every album do the follow:
    # # create folder if not exists
    # # get list of photos
    # # download photo and put it in album folder
    # # do it while have photos
    # do it while have albums

    parser = argparse.ArgumentParser(description='', version='%(prog)s ' + __version__)
    parser.add_argument('username', help='vk.com username')
    parser.add_argument('password', help='vk.com username password')
    parser.add_argument('-o', '--output', help='output path to store photos',
                        default=os.path.abspath(os.path.join(os.path.dirname(__file__), 'exported')))

    args = parser.parse_args()

    # expand user path if necessary
    if args.output.startswith('~'):
        args.output = os.path.expanduser(args.output)

    start_time = datetime.datetime.now()
    try:
        # Initialize vk.com connection
        connection = connect(args.username, args.password)

        # Request list of photo albums
        albums = get_albums(connection)
        print("Found %s album%s:" % (len(albums), 's' if len(albums) > 1 else ''))
        print('%-40s|%4s|%10s' % ('title', 'size', 'aid'))
        print('-' * 61)
        ix = 0
        for album in albums:
            print('%3d. %-40s|%4s|%10s' % (ix + 1, album['title'], album['size'], album['aid']))
            ix += 1

        # Sleep to prevent max request count
        time.sleep(1)

        if not os.path.exists(args.output):
            os.makedirs(args.output)

        for album in albums:
            response = get_photos(connection, album['aid'])
            output = os.path.join(args.output, album['title'])
            if not os.path.exists(output):
                os.makedirs(output)

            processed = 0

            for photo in response:
                percent = round(float(processed) / float(len(response)) * 100, 2)
                sys.stdout.write(
                    "\rExporting %s... %s of %s (%2d%%)" % (album['title'], processed, len(response), percent))
                sys.stdout.flush()

                download(photo, output)
                processed += 1

            print("\n")

    except Exception as e:
        print(e)
        sys.exit(1)

    except KeyboardInterrupt:
        print('VKPorter exporting stopped by keyboard')
        sys.exit(0)

    finally:
        print("Done in %s" % (datetime.datetime.now() - start_time))
