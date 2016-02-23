# VKPorter [deprecated]

## [Spelt](http://github.com/amka/Spelt) is a replacement for VKPorter.


Extremely small tool to export photo albums from [vk.com](https://vk.com).


## Prerequisites

Before you can start using VKPorter you have to install some python libraries if you don't have it.

    $ pip install -r requirements.txt


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


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/amka/vkporter/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

