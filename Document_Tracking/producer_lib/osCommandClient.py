#
# Python client class to OsCommand OsCommandFactory SMD service
#
__revision__ = '$Revision$'
__date__ = '$Date$'


from Connector import Connector, SmdClientError

PRIORITY_LOW = 0 
PRIORITY_MEDIUM = 500  
PRIORITY_HIGH = 1000 
# Used for standard legacy Queue compatibility
PRIORITY_UNUSED = -1  


class OsCommandClient:
    """Python Client interface to the SqlFactory SMD service """

    FETCH_ALL = -1 # get all results in one call (USE CAUTIOUSLY)
    CLASSFACTORY         = "com.sefas.gridclient.osservices.OsCommandFactory"
    STRCR = "\\n" 
    CR = "\n" 
    
    COMMAND           = "command"
    GETSTDOUT         = "getStdOut"
    GETSTDERR         = "getStdErr"
  
    _ENCODING_PROPERTY_ = "file.encoding"
    _ARGS_              = "args"

    def __init__ ( self , 
                   encoding="UTF8" , # default encoding to UTF8
                   hostName="localhost" ,
                   port=29100 
                 ):
        """ constructor just store provided object information """
        self._host = hostName 
        self._port = port
        self._connection = None
        self._encoding = encoding 

    def connect( self ) :
        """ connect to SqlFactory Service """
        if ( self._connection != None ):
            return
        self._connection = Connector( self._host , self._port , self._encoding,  self.CLASSFACTORY )

    def disconnect( self ):
        """ Disconnect from SqlFactory Service """
        if ( self._connection != None ):
            self._connection.close() 
            self._connection = None

    def command ( self, commandLine, priority=PRIORITY_UNUSED):
        """ execute the command on the smd server """
        self._connection.marshall( Connector.SET_METHOD, self.COMMAND)
        # populate parameters
        self._connection.marshall( Connector.DEF_STRING, self._ARGS_)
        self._connection.marshall( Connector.SET_VALUE, self._ARGS_, commandLine)
        self._connection.marshall( Connector.DEF_INTEGER, self._ARGS_)
        self._connection.marshall( Connector.SET_VALUE, self._ARGS_, priority)
        # proceed with call
        ret = self._connection.marshall( Connector.CALL )
        # marshall cursor id back or None if cursorId is -1
        returned = int(self._connection.unmarshall( ret ))
        if returned == -1 :
            return None
        return returned

    def getStd ( self, which):
        """ execute the command on the smd server """
        self._connection.marshall( Connector.SET_METHOD, which)
        # proceed with call
        ret = self._connection.marshall( Connector.CALL )
        returned = self._connection.unmarshall( ret )
        return returned

    def getStdOut ( self):
        return self.getStd(self.GETSTDOUT)

    def getStdErr ( self):
        return self.getStd(self.GETSTDERR)

#
# module main is just a practical sample test
# of JdbcClient usage
#
if __name__ == '__main__':
    myencoding = "ISO-8859-1" 
    
    myclient = OsCommandClient(myencoding, 'localhost', 29100)
    # myclient = OsCommandClient(myencoding,'10.2.1.100',29100)
    try :
        myclient.connect()
        myret = myclient.command('ls -a')
        print "(ls -a) ret = ", myret  , '\nStdOut = ' , myclient.getStdOut(), '\nStdErr = ', myclient.getStdErr()
        myclient.command('dir')
        print "(dir) ret = ", myret  , '\nStdOut = ' , myclient.getStdOut(), '\nStdErr = ', myclient.getStdErr()
        myclient.disconnect()

    except SmdClientError , e :
        print "service instanciation error : " , str(e)
  
