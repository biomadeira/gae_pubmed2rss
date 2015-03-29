from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

from flask import render_template

from tools import *


@app.route('/')
def hello():
    """Renders a simple api doc with the implemented methods."""
    return render_template("api.html")


@app.route('/search/pubmed/<string>')
def search_pubmed(string):
    """Return output from Pubmed - based on eutils API."""

    if string:

        return '%s' % string
    else:
        page_not_found(404)


@app.route('/rss/pubmed/<string>')
@app.route('/rss/pubmed/string=<string>')
@app.route('/rss/pubmed/<string>&<feeds>')
@app.route('/rss/pubmed/<feeds>&<string>')
@app.route('/rss/pubmed/string=<string>&feeds=<feeds>')
@app.route('/rss/pubmed/feeds=<feeds>&string=<string>')
def rss_pubmed(string, feeds=50):
    """Generate a rss feed from Pubmed - based on the main page search."""

    if string:
        rss_url = generate_rss_from_pubmed(string, feeds=feeds)
        return '%s' % rss_url
    else:
        page_not_found(404)



@app.route('/twitter_bot')
@app.route('/twitter_bot&<rss_guid>')
@app.route('/twitter_bot&rss_guid=<rss_guid>')
def bot(rss_guid=None):
    """
    Consumes a feed and checks if there are new entries in db.
    If so, gets a shortened url and tweets the new status.
    """

    return twitter_bot(rss_guid=rss_guid)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
