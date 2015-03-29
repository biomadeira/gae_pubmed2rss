#!/usr/bin/python
# -*- coding: utf-8 -*-


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

    @classmethod
    def get_last_rss_guid(cls, ancestor_key):
        return (cls.query(ancestor=ancestor_key).order(-cls.date)).fetch(1)

