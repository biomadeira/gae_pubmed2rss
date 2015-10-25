#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
---------
config.py
---------
This defines the methods that load and validate user defined
parameters.
.. moduleauthor:: Fabio Madeira
:module_version: 1.0
:created_on: 28-02-2015
"""

from __future__ import print_function

import os
import sys
from ConfigParser import SafeConfigParser

# edit this name if you rename your config file
CONFIG_FILE = "config.txt"


def load_config(option):
    """
    Loads and tests input parameters.
    :param option: option name
    :return: returns a valid config value for the inputed option
    """

    parser = SafeConfigParser()
    try:
        filename = "{}/{}".format(os.getcwd(), CONFIG_FILE)
        parser.read(filename)

        # addresses
        if option == "pubmed_search":
            return parser.get('Addresses', 'pubmed_search')
        elif option == "pubmed_rss":
            return parser.get('Addresses', 'pubmed_rss')
        elif option == "pubmed_eutils":
            return parser.get('Addresses', 'pubmed_eutils')
        else:
            raise ValueError("ERROR: Invalid option")
    except IOError:
        print("ERROR: Invalid Config File")


# replace this with your keys
# TwitterKey = {
# 'consumer_key': "",
#         'consumer_secret': "",
#         'access_token': "",
#         'access_token_secret': ""
#         }
#
# BitlyKey = {
#         'login': "",
#         'apikey': ""
#         }
TwitterKey = {
    'consumer_key': "RlbAgjvY1f9dGSvle0BYpBodR",
    'consumer_secret': "eD0MKBwPSNvHIpkZ9iM29sYhQLzzD3y462wXft5qylK5Ke4QmN",
    'access_token': "3126293415-sKlyEYcNZbRSHXOsH39umr81R8ROo4xbuL01rut",
    'access_token_secret': "QjHoBO9P1edWIcKT9ywXMJPLRLgNrFnivp53IvkArcDTI"
}

BitlyKey = {
    'access_token': "d151a4ee794bfe72ff8b649cee7467b4fcf054f1",
    'client_id': "7b30000799bdc03f3a68eed3b27ec1229e04740b",
    'client_secret': "351800b58b3251bc326d3805691ada2e0ecdd5e5"
}

if __name__ == "__main__":
    print("Testing...")