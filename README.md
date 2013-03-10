VKPorter
========

Extremely small tool to export photo albums from [vk.com](https://vk.com).


## Prerequisites

Before you can start using VKPorter you have to install some python libraries if you don't have it.

### ProgressBar

[https://pypi.python.org/pypi/progressbar](https://pypi.python.org/pypi/progressbar)

    $ pip install progressbar


### Requests

[https://github.com/kennethreitz/requests](https://github.com/kennethreitz/requests)

    $ pip install requests

or, with [easy_install](http://pypi.python.org/pypi/setuptools):

    $ easy_install requests

### VK_API
[https://github.com/python273/vk_api](https://github.com/python273/vk_api)

    $ pip install vk_api

## Usage

Synopsis:

    $ vkporter.py [-h] [-v] [-o OUTPUT] username

See also `vkporter --help`.

### Examples

    $ vkporter.py username password
    
photo albums will be exported to `./exported`.


    $ vkporter.py -o ~/Documents/Exported username
    
photo albums will be exported to `~/Documents/Exported`.
