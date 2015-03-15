'''
Created on Feb 18, 2015

@author: Duhi
'''
import urllib
import logging
def get_new_file(rss_feed_file):
    #txt_file = urlopen('http://feeds.thisamericanlife.org/talpodcast')
    
    try:
        print("Just IN the trye")    
        win_nu_fd=open(rss_feed_file, "a") #TODO:write the file in a tempdir, calc hash, if different than one already exist, update exisiting file
        print("Step 1")
        url = "http://feeds.thisamericanlife.org/talpodcast"
        print("Step 2")
        request = urllib.request.Request(url)
        print("Step 3")
        response = urllib.request.urlopen(request)
        print("Step 4")
        buffer=response.read().decode('utf-8')
        print("Step 5")
        print (buffer)
        print('writing buffer')
        
        win_nu_fd.write(buffer.replace("\r\n","\n"))
        
        win_nu_fd.close()
        del request
    except:
        print("Something wrong happened in get_new_file")
    
if __name__ == "__main__":
    rss_feed_file = '../resources/rss_feed_1.txt'
    try:
        get_new_file(rss_feed_file)
    except:
        print("Error somewhere up there")