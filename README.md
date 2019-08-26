# Requests-ZipFile-Redis-Cherrypy-jQuery
A repo for basic usage of requests, zipfile, redis , jQuery and cherrypy.

There are two parts of this repository : 

1. download_bhavcopy_equity_files.py : a script to download, unzip, parse a CSV file and populate a REDIS instance according to the respective entries. 

Upon visiting the link "https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx" and examining the "Bhavcopy" CSV file link, we see that part of the link is actually the present date, or last working day (in case of weekends). We download a .zip archive from the link based on this rationale. We unzip and parse the entries in the CSV using native python libraries and update these entries in Redis DB using a "HASHES" , the key being a counter variable and value being the parsed dictionary. Lastly, we update the counter variable in the DB in case if required later.

2.web_app.py : Front-End Web application containing a Web App and a REST API to provide a layer of communication with the updated Redis DB

This is main logic behind the frontend of the project hosted at "http://ec2-18-220-250-1.us-east-2.compute.amazonaws.com/" (when this README was last updated). We create a REST service at "http://ec2-18-220-250-1.us-east-2.compute.amazonaws.com/generator" for interation with the REDIS DB. We return Top 10 entries on a "GET" request at "..../generator". If we append "..../generator?records=<some number n>" to the REST endpoint, we can get information for the respective n TOP entries in our REDIS DB. Upon doing a "POST" request with a search string, we get the entries in return whose name contain our seach string. We link the REST API and index view to our webapp. In our Index View, we use jQuery AJAX to do "GET" and "POST" requests, and populate the the TOP 10 and search tables in our index page accordingly.
  
I have provided a redis configuration file which should be used to start the redis DB with the command "redis-server redis.conf", If any other Redis DB is used (different address or port), the scripts need to be modified accordingly. The webapp starts on 0.0.0.0 ,i.e, localhost by default. If any changes are made here, same should be changes in the jQuery adresses as well.
