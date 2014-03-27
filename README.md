VKPorter
========

Extremely small tool to export photo albums from [vk.com](https://vk.com).


## Prerequisites

Before you can start using VKPorter you have to install some python libraries.
To do so run this command in project root.

    $ pip install -r requirements.txt

## Usage

Synopsis:

    $ vkporter.py [-h] [-v] [-o OUTPUT] username

See also `vkporter --help`.

### Examples

    $ vkporter.py username password
    
photo albums will be exported to `./exported`.


    $ vkporter.py -o ~/Documents/Exported username
    
photo albums will be exported to `~/Documents/Exported`.
