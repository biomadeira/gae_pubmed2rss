#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
--------
tools.py
--------
This defines the routines used in the api.
.. moduleauthor:: Fabio Madeira
:module_version: 1.0
:created_on: 28-02-2015
"""

from __future__ import print_function

import urllib
import urllib2
import feedparser
import bitly_api
import tweepy

from config import load_config as conf

from models import FeedItem, FeedConsume
from google.appengine.ext import ndb

from config import TwitterKey, BitlyKey


def request_url(url, list_iter=True, verbose=False):
    """Generic url request method."""
    req = urllib2.urlopen(url)
    if verbose:
        print(req.getcode(), req.geturl())

    if req.getcode() == 200:
        return req
    elif req.getcode() == 429:  # or req.getcode() == 503 or req.getcode() == 504:
        request_url(url, list_iter=list_iter, verbose=verbose)
    else:
        # message = "%s\t%s" % (req.getcode()ß, url)
        # TODO: add logging
        return 0


def post_url(url, data, verbose=False):
    """Generic url post method."""

    req = urllib2.urlopen(url, data)
    if verbose:
        print(req.getcode(), req.geturl())

    if req.getcode() == 200:
        return req
    else:
        # message = "%s\t%s" % (req.getcode(), url)
        # TODO: add logging
        return 0


def shorten_url_bitly(url):
    """Generic method to shorten a url with Bitly"""
    conn = bitly_api.Connection(login=None,
                                api_key=BitlyKey["client_id"],
                                access_token=BitlyKey["access_token"],
                                secret=BitlyKey["client_secret"])
    return conn.shorten(url)["url"]


def update_status_twitter(status):
    """Generic metho to update the status in Twitter"""

    auth = tweepy.OAuthHandler(TwitterKey['consumer_key'], TwitterKey['consumer_secret'])
    auth.set_access_token(TwitterKey['access_token'], TwitterKey['access_token_secret'])
    bot = tweepy.API(auth)
    return bot.update_status(status=status)


def generate_rss_from_pubmed(input_string, feeds=50):
    """Returns the url of a rss generated at Pubmed by the queried string."""
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
            # url = "{}erss.cgi?rss_guid={}".format(conf("pubmed_rss"), rss_guid)
            return rss_guid

        else:
            return 0
    else:
        return 0


def twitter_bot(rss_guid=None):
    """
    Consumes a feed and checks if there are new entries in db.
    If so, gets a shortened url and tweets the new status.
    """

    if rss_guid is None:
        # ancestor_key = ndb.Key("RSS_GUID", rss_guid or "*norss*")
        # consumer = FeedConsume.get_last_rss_guid(ancestor_key)
        # rss_guid = consumer[0].rss_guid
        query = FeedConsume.gql("WHERE entry = :1", "latest")
        result = query.get()
        rss_guid = result.rss_guid
    else:
        consumer = FeedConsume(parent=ndb.Key("RSS_GUID", rss_guid or "*norss*"),
                               rss_guid=rss_guid, entry="latest")
        consumer.put()
    url = "{}erss.cgi?rss_guid={}".format(conf("pubmed_rss"), rss_guid)
    feeds = feedparser.parse(url)
    for feed in feeds["items"]:
        pmid = (feed["link"].split("/")[-1]).rstrip("?dopt=Abstract")
        query = FeedItem.gql("WHERE pmid = :1", pmid)
        # if pmid not in db
        if (query.count() == 0):
            title = feed["title"]
            url = feed["link"]
            category = feed["category"]
            item = FeedItem()
            item.pmid = pmid
            item.put()

            # shorten the url with Bitly.com
            shorturl = shorten_url_bitly(url)

            # tweet the new entry
            max_length = (140 - len(category) - len(shorturl) - 7)
            if len(title) > max_length:
                title = title[0:max_length]
            status = "#{}: {}... {}".format("".join(category.split()), title.rstrip("."), shorturl)
            try:
                status = unicode(status).encode("utf-8")
            except UnicodeEncodeError:
                pass
                # TODO: add logging

            # tweet new status
            update_status_twitter(status)
    return


if __name__ == '__main__':
    # testing routines
    # example_url = generate_rss_from_pubmed('"PLoS Comput Biol."[jour]')

    # ALl new entries from 01/04/2015
    # example_url = "http://www.ncbi.nlm.nih.gov/entrez/eutils/erss.cgi?rss_guid=1z3zFLTMk-jx9dXqtE4SfGE05yDieJhVzE72yLMWr0JyN7xEQ0"
    # fee_a_bot(example_url)
    # PlosOne example
    example_rss_guid = "1vMcRd_vquRX1CBvT4N0TK0nWJfp2afjnnSfhZ6IFOQwlrgkoj"
    twitter_bot(example_rss_guid)