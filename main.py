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
import urllib
from tools import *
from google.appengine.ext.webapp import template

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

default_search = '"PLoS One"[jour]'
default_feeds = 10
default_rssguid= "1h9kEWSfxImUd3q0TuDX7eLhEJoM4-k3pB8scCPrUmcSn3lkLl"


class MainPage(webapp2.RequestHandler):
    def get(self, search_output="", rssguid_output="", twitter_output=""):
        """Renders a simple api doc with the implemented methods."""
        # template = JINJA_ENVIRONMENT.get_template('api.html')
        template_values = {}
        template_values['baseurl'] = ""
        template_values['default_search'] = default_search
        template_values['default_feeds'] = str(default_feeds)
        template_values['default_rssguid'] = default_rssguid
        
        template_values['search_output'] = search_output
        template_values['rssguid_output'] = rssguid_output
        template_values['twitter_output'] = twitter_output

        path = os.path.join(os.path.dirname(__file__), 'api.html')
        self.response.write(template.render(path, template_values))
        
        
class Search(webapp2.RequestHandler):        
    def post(self):
        search = self.request.get("search", default_search)
        search = urllib.quote_plus(search)
        return webapp2.redirect('/search/pubmed/string=%s' % search)


class Rss(webapp2.RequestHandler):
    def post(self):
        search = self.request.get("search", default_search)
        feeds = self.request.get("feeds", default_feeds)
        return webapp2.redirect('/rss/pubmed/string=%s&feeds=%s' % (search, feeds))


class Twitter(webapp2.RequestHandler):
    def post(self):
        rssguid = self.request.get("rssguid", default_rssguid)
        return webapp2.redirect('/twitter_bot&rss_guid=%s' % (rssguid))


class SearchPubmed(webapp2.RequestHandler):
    def get(self, string):
        """Return output from Pubmed - based on eutils API."""

        if string:
            return webapp2.redirect('/search_output=%s' % string)
        else:
            self.abort(500)


class RssPubmed(webapp2.RequestHandler):
    """Generate a rss feed from Pubmed - based on the main page search."""

    def get(self, string, feeds=50):
        if string:
            rss_guid = generate_rss_from_pubmed(string, feeds=feeds)
            return webapp2.redirect('/rssguid_output=%s' % rss_guid)
        else:
            self.abort(500)


class RssBot(webapp2.RequestHandler):
    """
    Consumes a feed and checks if there are new entries in db.
    If so, gets a shortened url and tweets the new status.
    """

    def get(self, rss_guid=None):
        try:
            tweets = twitter_bot(rss_guid=rss_guid)

            # template = JINJA_ENVIRONMENT.get_template('papers.html')
            template_values = {}
            template_values['baseurl'] = ""
            template_values['twitter_output'] = tweets

            path = os.path.join(os.path.dirname(__file__), 'papers.html')
            self.response.write(template.render(path, template_values))
            
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
    
    webapp2.Route(r'/search_output=<search_output:[^/]+>', handler='main.MainPage', name='search_output'),
    webapp2.Route(r'/rssguid_output=<rssguid_output:[^/]+>', handler='main.MainPage', name='rssguid_output'),
    
    webapp2.Route(r'/search', handler='main.Search'),
    webapp2.Route(r'/rss', handler='main.Rss'),
    webapp2.Route(r'/twitter', handler='main.Twitter'),
    
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

