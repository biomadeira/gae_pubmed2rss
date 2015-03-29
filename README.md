## Python [Flask](http://flask.pocoo.org) API for Google App Engine

## Implemented Methods:

#### Decodes the inputed string.  
Example[http://api.papersetal.com/search/pubmed/%22PLoS%20One%22[jour]](http://api.papersetal.com/search/pubmed/%22PLoS%20One%22[jour])

*   /search/pubmed/<string>

#### Generates an rss_guid from Pubmed.  
Example[http://api.papersetal.com/rss/pubmed/string=%22PLoS%20One%22[jour]&feeds=20](http://api.papersetal.com/rss/pubmed/string=%22PLoS%20One%22[jour]&feeds=20)

*   /rss/pubmed/<string>
*   /rss/pubmed/string=<string>
*   /rss/pubmed/<string>&<feeds>
*   /rss/pubmed/<feeds>&<string>
*   /rss/pubmed/string=<string>&feeds=<feeds>
*   /rss/pubmed/feeds=<feeds>&string=<string>

#### Consumes a Pubmed rss feed (rss_guid) and tweets the new entries. If rss_guid is not provided uses the last one in the db.  
Example[http://api.papersetal.com/twitter_bot&rss_guid=10KSIBP312BFu5ZtZWGihbGEZXh4IK2Q9I44Hvc1UXvWiIeEp5](http://api.papersetal.com/twitter_bot&rss_guid=10KSIBP312BFu5ZtZWGihbGEZXh4IK2Q9I44Hvc1UXvWiIeEp5)

*   /twitter_bot
*   /twitter_bot&<rss_guid>
*   /twitter_bot&rss_guid=<rss_guid>


## Feedback
Star this repo if you found it useful. Use the github issue tracker to give
feedback on this repo.

## Contributing changes
See [CONTRIB.md](CONTRIB.md)

## Licensing
See [LICENSE](LICENSE)

## Author
Fábio Madeira


