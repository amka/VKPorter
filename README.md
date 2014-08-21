VKPorter
========

Extremely small tool to export photo albums from [vk.com](https://vk.com).


## Prerequisites

Before you can start using VKPorter you have to install some python libraries if you don't have it.

    $ pip installe -r requirements.txt


* ProgressBar ([https://pypi.python.org/pypi/progressbar](https://pypi.python.org/pypi/progressbar))
* Requests ([https://github.com/kennethreitz/requests](https://github.com/kennethreitz/requests))
* VK_API ([https://github.com/python273/vk_api](https://github.com/python273/vk_api))


## Usage

Synopsis:

    $ vkporter.py [-h] [-v] [-o OUTPUT] username

See also `vkporter --help`.

### Examples

    $ vkporter.py username password
    
photo albums will be exported to `./exported`.

    $ vkporter.py -o ~/Documents/Exported username
    
photo albums will be exported to `~/Documents/Exported`.
