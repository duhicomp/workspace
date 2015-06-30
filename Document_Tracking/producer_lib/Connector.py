import codecs
import socket

class SmdClientError(StandardError):
    """ Provide a clean and lean exception class """ 
    pass

class Connector :
    """ Basic Low level service marshaller """
    
    ALLOCATE_CLASSLOADER = "ALC %s\n" 
    SET_METHOD = "MTH %s \n" 
    DEF        = "DPRM "
    DEF_STRING = "DPRM %s s\n" 
    DEF_STRING_ARRAY = "DPRM %s s(%i)\n" 
    DEF_INTEGER = "DPRM %s i\n" 
    SET_VALUE = "SPRM %s = '%s'\n" 
    SET_ARRAY_VALUE = "SPRM %s (%i) = '%s'\n" 
    CALL = "CALL\n"

    STRCR = "\\n" 
    CR = "\n" 
   
    _ENCODING_PROPERTY_ = "file.encoding"
    _ARGS_              = "args"

    def __send( self , command ):
        """ basic send / receive semantics"""
        # send the stuff to the server
        self._connection.send( command  ) 
        # receive result back 
        # wait for a 99999 numerical length header response
        strLen = self._connection.recv(5)
        if not strLen.isdigit() :
            if len(strLen) == 0 :
                raise SmdClientError, "Connector unexpected buffer end on read => check for server disconnection"
            raise SmdClientError, "Connector Bad buffer content numerical Length expected found :" + strLen  
        responseLength = int(strLen)
        # read the reminder back  
        response = self._connection.recv(responseLength)
        while len(response) != responseLength :
            response = response + self._connection.recv(responseLength-len(response))
        # check for Immediate SMD errors
        # and populate immediate exception back
        if response[0:7] == "<ERROR>" :
            raise SmdClientError , "SMD call failed :" + response[7:len(response)-10]
        # OK return content back
        return response

    def marshall( self , fx , *args ):
        """ proceed an allocate class loader command with provided name arg """
        command = fx % args 
        return self.__send( command )

    def unmarshall( self , content ):
        """ unmarshall the returned value back <OK>retval</OK>"""
        if content[0:5] == "<OK/>": 
            return None
        # <OK>blah...</OK> is assumed if offset 4 is '>' 
        return content[4:len(content)-7]   

    def close(self):
        """ close the Ip link with service """
        if self._connection != None :
            self._connection.close()      

    def __init__( self , hostName , port , encoding , classFactory):
        try:  
            # handle encoding first 
            self._encoder = codecs.getencoder(encoding)
            self._decoder = codecs.getdecoder(encoding)
            # connect to SMD first  
            self._connection = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
            self._connection.connect( ( hostName , port ) )
            # load the SqlFactory service 
            self.marshall( self.ALLOCATE_CLASSLOADER , "CLASS:/"+classFactory )
        except socket.error, (errno,strerror):
            raise SmdClientError , "Connector failed to connect requested Service on " + \
                  hostName + ":" + str(port) + "code=" + str(errno) +" message=" \
                  + strerror
      
