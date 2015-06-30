#
# Python client class to OsCommand OsCommandFactory SMD service
#
__revision__ = '$Revision$'
__date__ ='$Date$'


from Connector import Connector, SmdClientError


class ExecEngine:
    """Python Client interface to the SqlFactory SMD service """

    FETCH_ALL = -1 # get all results in one call (USE CAUTIOUSLY)
    CLASSFACTORY         = "com.sefas.EngineStarter.SmdEngineStarter"
    
    METHOD_ADD_ENV = "addEnv"
    METHOD_ADD_PARAM = "addParam"
    METHOD_LOAD_ENV_PROP = "loadEnvProp"
    METHOD_LOAD_ENGINES_PROP = "loadEnginesProp"
    METHOD_LOCK = "lock"

    METHOD_START = "start"
    METHOD_START_ASSEMBLY = "startAssembly"
    METHOD_START_CODR = "startCodr"
    METHOD_START_COMPO = "startCompo"
    METHOD_START_DRV = "startDrv"
    METHOD_START_SORT = "startSort"

    METHOD_RESULT_LOG        = "resultLog"
    METHOD_RESULT_EXIT_CODE  = "resultExitCode"
    METHOD_RESULT_ERR        = "resultErr"
    METHOD_RESULT_MESSAGE    = "resultMessage"
    METHOD_RESULT_VERSION    = "resultVersion"
    
    METHOD_PARAM_VARNAME = "paramVarName"
    METHOD_PARAM_VARVALUE = "paramVarValue"
    METHOD_PARAM_FILENAME = "paramFileName"
    METHOD_PARAM_LOCK     = "paramLock"
    METHOD_PARAM_ENGINE_KEY     = "engineKey"

    def __init__ (self , 
                   encoding="UTF8" , # default encoding to UTF8
                   hostName="localhost" , 
                   port=29100 
                 ):
        """ constructor just store provided object information """
        self._host = hostName 
        self._port = port
        self._connection = None
        self._encoding = encoding
        self._param = {} 
        self._env = {} 
        self._paramSended = {} 
        self._envSended = {} 
        self._engineProp = None 
        self._envProp = None 
        self._islock = True 
        
    def connect(self) :
        """ connect to SqlFactory Service """
        if (self._connection != None):
            return
        self._connection = Connector(self._host , self._port , self._encoding, self.CLASSFACTORY)
        self.lock(True)

    def disconnect(self):
        """ Disconnect from SqlFactory Service """
        if (self._connection != None):
            self._connection.close() 
            self._connection = None

    def addEnv (self, envVarName, envVarValue):
        """ add an environment variable to the call """
        self._env[envVarName] = envVarValue
        """ execute the command on the smd server """
        self._connection.marshall(Connector.SET_METHOD, self.METHOD_ADD_ENV)
        # populate parameters
        self._connection.marshall(Connector.DEF_STRING, self.METHOD_PARAM_VARNAME)
        self._connection.marshall(Connector.SET_VALUE, self.METHOD_PARAM_VARNAME, envVarName)
        self._connection.marshall(Connector.DEF_STRING, self.METHOD_PARAM_VARVALUE)
        self._connection.marshall(Connector.SET_VALUE, self.METHOD_PARAM_VARVALUE, envVarValue)
        # proceed with call
        return self._connection.marshall(Connector.CALL)

    def addParam (self, paramVarName, paramVarValue):
        """ add a parameter to the call """
        self._param[paramVarName] = paramVarValue
        """ execute the command on the smd server """
        self._connection.marshall(Connector.SET_METHOD, self.METHOD_ADD_PARAM)
        # populate parameters
        self._connection.marshall(Connector.DEF_STRING, self.METHOD_PARAM_VARNAME)
        self._connection.marshall(Connector.SET_VALUE, self.METHOD_PARAM_VARNAME, paramVarName)
        self._connection.marshall(Connector.DEF_STRING, self.METHOD_PARAM_VARVALUE)
        self._connection.marshall(Connector.SET_VALUE, self.METHOD_PARAM_VARVALUE, paramVarValue)
        # proceed with call
        return self._connection.marshall(Connector.CALL)

    def loadEnvProp (self, envPropertiesFileName):
        """ set the environement properties file name to be used on the server """
        self._envProp = envPropertiesFileName 
        """ execute the command on the smd server """
        self._connection.marshall(Connector.SET_METHOD, self.METHOD_LOAD_ENV_PROP)
        # populate parameters
        self._connection.marshall(Connector.DEF_STRING, self.METHOD_PARAM_FILENAME)
        self._connection.marshall(Connector.SET_VALUE, self.METHOD_PARAM_FILENAME, envPropertiesFileName)
        # proceed with call
        return self._connection.marshall(Connector.CALL)

    def loadEnginesProp (self, enginesPropertiesFileName):
        """ set the propertie file name of the server to be used """
        self._engineProp = enginesPropertiesFileName 
        """ execute the command on the smd server """
        self._connection.marshall(Connector.SET_METHOD, self.METHOD_LOAD_ENGINES_PROP)
        # populate parameters
        self._connection.marshall(Connector.DEF_STRING, self.METHOD_PARAM_FILENAME)
        self._connection.marshall(Connector.SET_VALUE, self.METHOD_PARAM_FILENAME, enginesPropertiesFileName)
        # proceed with call
        return self._connection.marshall(Connector.CALL)

    def lock (self, synchronizedCall):
        """ management of the sychroneous or asynchroneus call """
        self._islock = synchronizedCall 
        """ execute the command on the smd server """
        self._connection.marshall(Connector.SET_METHOD, self.METHOD_LOCK)
        # populate parameters
        self._connection.marshall(Connector.DEF_STRING, self.METHOD_PARAM_LOCK)
        if synchronizedCall:
            self._connection.marshall(Connector.SET_VALUE, self.METHOD_PARAM_LOCK, "true")
        else :
            self._connection.marshall(Connector.SET_VALUE, self.METHOD_PARAM_LOCK, "false")
        # proceed with call
        return self._connection.marshall(Connector.CALL)

    def start (self, engineKey):
        """ execute the command on the smd server """
        self._connection.marshall(Connector.SET_METHOD, self.METHOD_START)
        # populate parameters
        self._connection.marshall(Connector.DEF_STRING, self.METHOD_PARAM_ENGINE_KEY)
        self._connection.marshall(Connector.SET_VALUE, self.METHOD_PARAM_ENGINE_KEY, engineKey)
        # proceed with call
        return self._connection.marshall(Connector.CALL)

    def getReturnDetail (self):
        self._connection.marshall(Connector.SET_METHOD, self.METHOD_RESULT_EXIT_CODE)
        exitCode = self._connection.unmarshall(self._connection.marshall(Connector.CALL))
        self._connection.marshall(Connector.SET_METHOD, self.METHOD_RESULT_VERSION)
        version = self._connection.unmarshall(self._connection.marshall(Connector.CALL))
        self._connection.marshall(Connector.SET_METHOD, self.METHOD_RESULT_MESSAGE)
        message = self._connection.unmarshall(self._connection.marshall(Connector.CALL))
        self._connection.marshall(Connector.SET_METHOD, self.METHOD_RESULT_LOG)
        log = self._connection.unmarshall(self._connection.marshall(Connector.CALL))
        self._connection.marshall(Connector.SET_METHOD, self.METHOD_RESULT_ERR)
        err = self._connection.unmarshall(self._connection.marshall(Connector.CALL))
        return "Exit Code = %s\nVersion = %s\nMessage = %s\nLog = %s\nError = %s" %(exitCode,version,message,log,err) 

    def printReturnDetail (self):
        print self.getReturnDetail()
        
    def manageExecReturn (self, ret):
        """ execute the command on the smd server """
        returned = int(self._connection.unmarshall( ret ))
        if returned != 0:
            print "Execution return code not 0 : "
            self.printReturnDetail()

#
# module main is just a practical sample test
# of JdbcClient usage
#
if __name__ == '__main__':
    myencoding = "ISO-8859-1" 
    
    # myclient = OsCommandClient(myencoding,'figaro',29110)
    # myclient = OsCommandClient(myencoding,'10.2.1.100',29100)
    myclient = ExecEngine(myencoding, '127.0.0.1', 29100)
    # D:\dev\test\MO\mo61\home\config
    try :
        myclient.connect()
        ret = myclient.loadEnvProp('D:\\dev\\test\MO\\mo61\\home\\config\\env_win.prop')
        ret = myclient.loadEnginesProp('D:\\dev\\test\MO\\mo61\\home\\config\\engines_win.prop')
        # myclient.addEnv("opInstallDir", "c:/oprint");
        myclient.addEnv("opWD", "E:/Reports/auto/opWD")
        myclient.addEnv("SystemRoot", "c:/WINNT")
        myclient.addEnv("opFam", "rightnow2_7.1")
        myclient.addEnv("opAppli", "SimpleReport_901_1.55")
        myclient.addParam("opAppliNamed", "rightnow2")
        # myclient.addParam("MacroTab", "calender.tab")
        myclient.addParam("DriverType", "vpf")
        myclient.addParam("data", "rightnow2.xml")
        myclient.addParam("sgml", "toto.sgml")
        myclient.addParam("vpf", "toto.vpf")
        myclient.manageExecReturn(myclient.start("ENG_ASM_NAMED"))
        myclient.manageExecReturn(myclient.start("ENG_CODR"))
        # myclient.manageExecReturn(myclient.start("ENG_GILLES"))
        myclient.disconnect()

    except SmdClientError , e :
        print "service instanciation error : " , str(e)
  
