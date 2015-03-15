'''
Created on Feb 18, 2015

@author: Duhi
'''
import feedparser
import logging

try:
    print("In the try section")
    python_wiki_rss_url = "http://feeds.thisamericanlife.org/talpodcast"
    
    feed = feedparser.parse( python_wiki_rss_url )
    print(feed)
    
except:
    print("somehting happened up there")