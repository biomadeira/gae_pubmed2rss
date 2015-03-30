#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
-------
main.py
-------
Main methods (views + routes) implemented in the API.
.. moduleauthor:: Fabio Madeira
:module_version: 1.0
:created_on: 28-02-2015
"""

import webapp2
import logging
import os
import jinja2
from tools import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
    def get(self):
        """Renders a simple api doc with the implemented methods."""
        template = JINJA_ENVIRONMENT.get_template('api.html')
        self.response.write(template.render())


class SearchPubmed(webapp2.RequestHandler):
    def get(self, string):
        """Return output from Pubmed - based on eutils API."""

        if string:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('%s' % string)
        else:
            self.abort(500)


class RssPubmed(webapp2.RequestHandler):
    """Generate a rss feed from Pubmed - based on the main page search."""

    def get(self, string, feeds=50):
        if string:
            rss_guid = generate_rss_from_pubmed(string, feeds=feeds)
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('%s' % rss_guid)
        else:
            self.abort(500)


class RssBot(webapp2.RequestHandler):
    """
    Consumes a feed and checks if there are new entries in db.
    If so, gets a shortened url and tweets the new status.
    """

    def get(self, rss_guid=None):
        try:
            twitter_bot(rss_guid=rss_guid)

            self.response.headers['Content-Type'] = 'text/plain'
            url = "https://twitter.com/papersetal_bot"
            self.response.write('%s' % url)
        except:
            self.abort(500)


def handle_404(request, response, exception):
    logging.exception(exception)
    response.write('Sorry, nothing at this URL!')
    response.set_status(404)


def handle_500(request, response, exception):
    logging.exception(exception)
    response.write('A server error occurred!')
    response.set_status(500)


debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

app = webapp2.WSGIApplication(routes=[
    webapp2.Route(r'/', handler='main.MainPage', name='home'),

    webapp2.Route(r'/search/pubmed/string=<string:[^/]+>', handler='main.SearchPubmed', name='string'),
    webapp2.Route(r'/search/pubmed/<string:[^/]+>', handler='main.SearchPubmed', name='string'),

    webapp2.Route(r'/rss/pubmed/string=<string:[^/]+>&feeds=<feeds:[^/]+>', handler='main.RssPubmed', name='string'),
    webapp2.Route(r'/rss/pubmed/<string:[^/]+>&<feeds:[^/]+>', handler='main.RssPubmed', name='string'),
    webapp2.Route(r'/rss/pubmed/string=<string:[^/]+>', handler='main.RssPubmed', name='string'),
    webapp2.Route(r'/rss/pubmed/<string:[^/]+>', handler='main.RssPubmed', name='string'),

    webapp2.Route(r'/twitter_bot&rss_guid=<rss_guid:[^/]+>', handler='main.RssBot', name='rss_guid'),
    webapp2.Route(r'/twitter_bot&<rss_guid:[^/]+>', handler='main.RssBot', name='rss_guid'),
    webapp2.Route(r'/twitter_bot', handler='main.RssBot', name='rss_guid'),
], debug=debug)

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500

