#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
---------
models.py
---------
This defines the models used in the api. It uses the GAE NDB datastore.
.. moduleauthor:: Fabio Madeira
:module_version: 1.0
:created_on: 30-02-2015
"""

from google.appengine.ext import ndb


class FeedItem(ndb.Model):
    # title = ndb.StringProperty(required=False)
    # link = ndb.StringProperty(required=False)
    # category = ndb.StringProperty(required=False)
    pmid = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)


class FeedConsume(ndb.Model):
    rss_guid = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    entry = ndb.StringProperty(required=True)

    @classmethod
    def get_last_rss_guid(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)

