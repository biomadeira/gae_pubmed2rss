### Pubmed to Rss feeds
Pubmed2rss app running in [Google App Engine](https://cloud.google.com/appengine/). 

#### API methods:

##### Decodes the inputted string.  
Example [http://pubmed2rss.appspot.com/search/pubmed/%22PLoS%20One%22[jour]](http://pubmed2rss.appspot.com/search/pubmed/%22PLoS%20One%22[jour])

*   /search/pubmed/&lt;string&gt;
*   /search/pubmed/string=&lt;string&gt;

##### Generates an unique Rss id(rss_guid) from Pubmed.  
Example [http://pubmed2rss.appspot.com/rss/pubmed/string=%22PLoS%20One%22[jour]&feeds=20](http://pubmed2rss.appspot.com/rss/pubmed/string=%22PLoS%20One%22[jour]&feeds=20)

*   /rss/pubmed/&lt;string&gt;
*   /rss/pubmed/string=&lt;string&gt;
*   /rss/pubmed/&lt;string&gt;&&lt;feeds&gt;
*   /rss/pubmed/string=&lt;string&gt;&feeds=&lt;feeds&gt;


##### Consumes a Pubmed rss feed (rss_guid) and tweets the new entries. If rss_guid is not provided uses the last one in the db.  
Example [http://pubmed2rss.appspot.com/twitter_bot&rss_guid=10KSIBP312BFu5ZtZWGihbGEZXh4IK2Q9I44Hvc1UXvWiIeEp5](http://pubmed2rss.appspot.com/twitter_bot&rss_guid=10KSIBP312BFu5ZtZWGihbGEZXh4IK2Q9I44Hvc1UXvWiIeEp5)

*   /twitter_bot
*   /twitter_bot&&lt;rss_guid&gt;
*   /twitter_bot&rss_guid=&lt;rss_guid&gt;


### Licensing
See [LICENSE](LICENSE.txt)
