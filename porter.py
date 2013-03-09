# -*- coding: utf-8 -*-
__author__ = 'amka'
__date__ = '09.03.13'

from progressbar import FileTransferSpeed, Percentage, Bar, ProgressBar
import requests
from vk_api import vk_api


def connect(login, password):
    """Initialize connection with `vk.com <https://vk.com>`_ and try to authorize user with given credentials.

    :param login: user login e. g. email, phone number
    :type login: str
    :param password: user password
    :type password: str

    :return: :class:`vk_api.VkApi` connection
    :rtype: :class:`vk_api.VkApi`
    """
    return vk_api.VkApi(login, password)


def get_albums(connection):
    """Get albums list for currently authorized user.

    :param connection: :class:`vk_api.VkApi` connection
    :type connection: :class:`vk_api.VkApi`

    :return: list of photo albums
    :rtype: list
    """
    return []


def download(photo):
    """Download photo

    :param photo:
    """
    url = photo.get('src_xxxbig') or photo.get('src_xxbig') or photo.get('src_xbig') or photo.get('src_big')

    r = requests.get(url)
    size = int(r.headers['content-length'].strip())
    bytes = 0
    title = photo['text'] or '%s' % photo['pid']
    widgets = [title, ": ", Bar(marker="|", left="[", right=" "),
               Percentage(), " ", FileTransferSpeed(), "] ",
               ' ',
               " of {0}".format(sizeof_fmt(size))]
    pbar = ProgressBar(widgets=widgets, maxval=size).start()
    file = []
    for buf in r.iter_content(1024):
        if buf:
            file.append(buf)
            bytes += len(buf)
            pbar.update(bytes)
    pbar.finish()


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

if __name__ == '__main__':
    login = raw_input(u"Enter your username: ")
    password = raw_input(u"Enter your password: ")
    connection = connect(login, password)

    # Connect to vk.com
    # Get list of user albums
    # For every album do the follow:
    # # create folder if not exists
    # # get list of photos
    # # download photo and put it in album folder
    # # do it while have photos
    # do it while have albums