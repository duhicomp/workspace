'''
Created on Feb 2, 2011

@author: jymen
'''

_JSON_ = 'json'
_ACCEPT_LANGUAGE_ = 'Accept-language'
_CONTENT_TYPE_ = 'Content-type'
_ACCEPT_ = 'Accept'
_LANGUAGE_ = 'en'
_POST_ = 'POST'

GOOD_HTTP =200
DEBUG=False

class AjaxClientError(StandardError):
    """ Provide a clean and lean exception class """
    pass



class HttpConnector(object):


    def __init__(self , url , servlet):
        '''
        Constructor
        '''
        if ( url[0:7] == 'http://') :
            self._url = url[7:]
        else :
            self._url = url
        self._servlet = servlet

    def ajaxCall(self , args ):
        import json
        jsonParams = json.dumps(args) # just convert to json
        import httplib , urllib
        httpParams = urllib.urlencode( { _JSON_ : jsonParams } )
        headers = {  _CONTENT_TYPE_ : "application/x-www-form-urlencoded" ,
                    _ACCEPT_LANGUAGE_ : _LANGUAGE_ ,
                    _ACCEPT_ :"text/plain"  }
        connection = httplib.HTTPConnection(self._url)
        connection.request(_POST_  , self._servlet , httpParams , headers )
        response = connection.getresponse()
        # only acceptable http return here is 200 OK
        if response.status != GOOD_HTTP :
            raise AjaxClientError("Ajax call bad http return : %i : %s" % response.status , response.reason )
        data = response.read()
        connection.close()
        if DEBUG :
            print "DATA= %s" % data
        return json.loads(data)


if __name__ == '__main__':
    print "sample ajaxCall test on getVersion"
    connector = HttpConnector("http://myubuntu:9080" , "/sefasajax/jsonapi" )
    returned = connector.ajaxCall( { 'fx' : 'GetVersion' } )
    if ( returned.get('error') != None ) :
        print"ERROR :" + returned['error']
    else :
        print "VERSION:" + returned['version']

