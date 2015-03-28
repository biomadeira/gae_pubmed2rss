#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
--------
tools.py
--------
This defines the methods that implement routines used in the api.
.. moduleauthor:: Fabio Madeira
:module_version: 1.0
:created_on: 28-02-2015
"""

from __future__ import print_function

import urllib
import urllib2
import feedparser

from config import load_config as conf


def request_url(url, list_iter=True, verbose=False):

    req = urllib2.urlopen(url)
    if verbose:
        print(req.getcode(), req.geturl())

    if req.getcode() == 200:
        return req
    elif req.getcode() == 429: # or req.getcode() == 503 or req.getcode() == 504:
        request_url(url, list_iter=list_iter, verbose=verbose)
    else:
        # message = "%s\t%s" % (req.getcode()ß, url)
        # TODO: add logging
        return 0


def post_url(url, data, verbose=False):

    req = urllib2.urlopen(url, data)
    if verbose:
        print(req.getcode(), req.geturl())

    if req.getcode() == 200:
        return req
    else:
        # message = "%s\t%s" % (req.getcode(), url)
        # TODO: add logging
        return 0


def generate_rss_from_pubmed(input_string, feeds=50):

    input_string = urllib.quote_plus(input_string)
    pubmed_url = conf("pubmed_search")
    url = "{}?term={}".format(pubmed_url, input_string)
    read = request_url(url, list_iter=False, verbose=False)

    if read:
        # parse info from the response html - quick and dirty
        hid = ''
        qk = ''
        line = read.read()
        # the field to parse is the HID and qk
        if 'data-hid="' in line:
            hid = line.split('data-hid="')[1]
            hid = hid.split('"')[0]
        if 'data-qk="' in line:
            qk = line.split('data-qk="')[1]
            qk = qk.split('"')[0]

        dataload = {'p$site': 'pubmed',
                    'p$rq': 'EntrezSystem2.PEntrez.PubMed.Pubmed_SearchBar.Entrez_SearchBar:CreateRssFeed',
                    'QueryKey': qk,
                    'Db': 'pubmed',
                    'RssFeedName': input_string,
                    'RssFeedLimit': str(feeds),
                    'HID': hid}
        dataload = urllib.urlencode(dataload)
        read = post_url(pubmed_url, dataload, verbose=False)
        if read:
            rss_guid = ''
            line = read.read()
            # the field to parse is rss_guid
            if "rss_guid=" in line:
                rss_guid = line.split("rss_guid=")[2]
                rss_guid = rss_guid.split("'")[0]
            # parse the rss feed generated
            url = "{}erss.cgi?rss_guid={}".format(conf("pubmed_rss"), rss_guid)
            return url

            # feed = feedparser.parse(url)
            # for entry in feed["entries"]:
            #     title = entry["title"]
            #     id = entry["id"]
            #     print(title, id)
            #     # break


if __name__ == '__main__':
    # testing routines
    generate_rss_from_pubmed('"PLoS Comput Biol."[jour]')
