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
from getpass import getpass
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


def get_albums(connection, id=0):
    """Get albums list for currently authorized user.

    :param connection: :class:`vk_api.vk_api.VkApi` connection
    :type connection: :class:`vk_api.vk_api.VkApi`

    :return: list of photo albums or ``None``
    :rtype: list
    """
    try:
        if id == 0:
            return connection.method('photos.getAlbums')
        else:
            return connection.method('photos.getAlbums', {'owner_id': id})

    except Exception as e:
        print(e)
        return None


def download_album(connection, output_path, date_format, album, owner=0, desc=False, comments=False, prev_s_len=0):
    if album['id'] == 'user':
        response = get_user_photos(connection)
    else:
        response = get_photos(connection, album['id'], owner)

    output = os.path.join(output_path, album['title'])
    if not os.path.exists(output):
        os.makedirs(output)

    photos_count = response['count']
    photos = response['items']
    processed = 0

    for photo in photos:
        percent = round(float(processed) / float(photos_count) * 100, 2)
        output_s = "Exporting %s... %s of %s (%2d%%)" % (album['title'], processed, photos_count, percent)
        # Pad with spaces to clear the previous line's tail.
        # It's ok to multiply by negative here.
        output_s += ' '*(prev_s_len - len(output_s))
        write_line(output_s)
        prev_s_len = len(output_s)
        sys.stdout.flush()

        download(photo, output, date_format, desc, comments)
        processed += 1

        # crazy hack to prevent vk.com "Max retries exceeded" error
        # pausing download process every 50 photos
        if processed % 50 == 0:
            time.sleep(1)


def get_user_photos(connection):
    """Get user photos list"""
    try:
        return connection.method('photos.getUserPhotos', {'count': 1000})
    except Exception as e:
        print(e)
        return None


def get_photos(connection, album_id, owner_id):
    """Get photos list for selected album.

    :param connection: :class:`vk_api.vk_api.VkApi` connection
    :type connection: :class:`vk_api.vk_api.VkApi`
    :param album_id: album identifier returned by :func:`get_albums`
    :type album_id: int

    :return: list of photo albums or ``None``
    :rtype: list
    """

    try:
        if owner_id == 0:
            return connection.method('photos.get', {'album_id': album_id})
        else:
            return connection.method('photos.get', {'owner_id': owner_id, 'album_id': album_id})
    except Exception as e:
        print(e)
        return None


def download(photo, output, date_format, desc, comments):
    """Download photo

    :param photo:
    """
    url = photo.get('photo_2560') or photo.get('photo_1280') or photo.get('photo_807') or photo.get('photo_604') or photo.get('photo_130')

    formatted_date = datetime.datetime.fromtimestamp(photo['date']).strftime(date_format)
    title = '%s_%s' % (formatted_date, photo['id'])

    filename_download = os.path.join(output, '%s.jpg.download' % title)
    filename_final = os.path.join(output, '%s.jpg' % title)

    if os.path.isfile(filename_final):
        write_line('File %s already exists.' % title)
    else:
        r = requests.get(url)
        with open(filename_download, 'wb') as f:
            for buf in r.iter_content(1024):
                if buf:
                    f.write(buf)
        os.rename(filename_download, filename_final)

    if desc:
        fd = open(os.path.join(output, '%s.txt' % title), 'w')
        fd.write(photo['text'].encode('utf-8'))

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

def write_line(text):
    print u'\r %s' % text

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
    # parser.add_argument('password', help='vk.com username password')
    parser.add_argument('-o', '--output', help='output path to store photos',
                        default=os.path.abspath(os.path.join(os.path.dirname(__file__), 'exported')))
    parser.add_argument('-f', '--date_format', help='for photo title',                  default='%Y%m%d@%H%M')
    parser.add_argument('-a', '--album_id', help='dowload a particular album. Additional values: wall, profile, saved, user')
    parser.add_argument('-w', '--owner_id', help='dowload albums of a particular user or group', default=0)
    parser.add_argument('-d', '--desc', help='save description of the photo', default=False)
    parser.add_argument('-c', '--comments', help='save comments of the photo', default=False)

    args = parser.parse_args()

    # expand user path if necessary
    if args.output.startswith('~'):
        args.output = os.path.expanduser(args.output)

    start_time = datetime.datetime.now()
    try:
        password = getpass("Password: ")
        if not password:
            print('Password too short')
            sys.exit(0)

        # Initialize vk.com connection
        connection = connect(args.username, password)

        if args.album_id:
            album = {
                'id': args.album_id,
                'title': args.album_id
            }
            download_album(connection, args.output, args.date_format, album, args.owner_id, args.desc, args.comments)
        else:
            # Request list of photo albums
            albums_response = get_albums(connection, args.owner_id)
            albums_count = albums_response['count']
            albums = albums_response['items']

            print("Found %s album%s:" % (albums_count, 's' if albums_count > 1 else ''))
            ix = 0
            for album in albums:
                print('%3d. %-40s %4s item%s' % (
                    ix + 1, album['title'], album['size'], 's' if int(album['size']) > 1 else ''))
                ix += 1

            # Sleep to prevent max request count
            time.sleep(1)

            if not os.path.exists(args.output):
                os.makedirs(args.output)

            for album in albums:
                download_album(connection, args.output, args.date_format, album, args.owner_id, args.desc, args.comments)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e)
        print(exc_type, fname, exc_tb.tb_lineno)

        sys.exit(1)

    except KeyboardInterrupt:
        print('VKPorter exporting stopped by keyboard')
        sys.exit(0)

    finally:
        print("Done in %s" % (datetime.datetime.now() - start_time))
