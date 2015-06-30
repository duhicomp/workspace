import os
import sys
isWindows = sys.platform[0:3] == 'win'

from ExecEngine import ExecEngine
from Connector import SmdClientError

# Parameter Exception is used to managed Error in parameteres
# Those error can be due to concistancy, missing parameter or overmuch parameter
class ExecutionException(Exception):
    
    def __init__(self, errorMessage):
        self.__errorMessage = errorMessage
   
    def getErrorDetail(self):
        return self.__errorMessage
    
class Backstage:

    def __init__(self, logger = None):
        """ constructor just store provided object information """
        self.__logging = logger
        self._execEngineClient = None
        self._smdHostName = None 
        self._smdPort = None
        self.__engineCommandLineInited = False
        self.__lastEngineCommandLine = None
        
        self.__initFromEnv()

    def __initFromEnv(self):
        self._encoding = "UTF8" 
        # SMD configuration information
        self._smdHostName = os.environ.get('SMD_HOST','localhost') 
        self._smdPort = os.environ.get('SMD_PORT','29100')
        self._closeExecEngine()

    def _log(self,msg):
        if self.__logging is not None:
            self.__logging.log(msg)
        else:
            print msg

    def _err(self,msg,exceptionType=None, exceptionValue=None):
        self._log(msg)
        if self.__logging is not None:
            self.__logging.err(msg,exceptionType,exceptionValue)
        else:
            print msg
            if exceptionValue is not None:
                raise exceptionValue
        
    def _closeExecEngine(self):
        # close the database connection and the connection to SMD
        # this method is always called if we change a default parameter (encoding, SMD or Database
        if self._execEngineClient is not None:
             self._execEngineClient.disconnect()
             self._execEngineClient = None

    def _initExecEngine(self):
        # open the connection to SMD and to the Database if there is not still existing
        if self._execEngineClient is None:
            self._execEngineClient = ExecEngine(self._encoding,self._smdHostName,int(self._smdPort))
            # Connect to SMD
            self.checkOk(self._execEngineClient,self._execEngineClient.connect())
            if isWindows:
                producerHome = os.environ.get('PRODUCER_HOME','c:\\producer')
                osType = 'windows'
                self.addEnv('opInstallDir', os.environ.get('opInstallDir',"%s\\bin\\backstage\\%s" % (producerHome,osType)))
                self.addEnv('opWD', os.environ.get('opWD',"%s\\opWD" % producerHome))
            else:
                producerHome = os.environ.get('PRODUCER_HOME','/home/producer')
                osNameType = os.environ.get('PRODUCER_OS','LNX')
                if osNameType == 'LNX':
                    osType = 'linux'
                elif osNameType == 'SUN':
                    osType = 'solaris'
                elif osNameType == 'AIX':
                    osType = 'aix'
                else:
                    osType = 'linux'
                self.addEnv('opInstallDir', os.environ.get('opInstallDir',"%s/bin/backstage/%s" % (producerHome,osType)))
                self.addEnv('opWD', os.environ.get('opWD',"%s/opWD" % producerHome))

            self.addEnv('opFam', os.environ.get('opFam','.'))
            self.addEnv('opAppli', os.environ.get('opAppli','.'))
            
            if isWindows:
                backstageDir = os.environ.get('BACKSTAGE_CONFIG_DIRECTORY','c:\\producer\\home\\config\\backstage')
                self.loadEnvProp("%s\\env_win.prop" % backstageDir, True)
                self.loadEnginesProp("%s\\engines_win.prop" % backstageDir, True)
            else:
                backstageDir = os.environ.get('BACKSTAGE_CONFIG_DIRECTORY','/home/producer/home/config/backstage')
                self.loadEnvProp("%s/env_unix.prop" % backstageDir, True)
                self.loadEnginesProp("%s/engines_unix.prop" % backstageDir, True)

    def close(self):
        self._closeExecEngine()
        
    def changeEncoding(self, encoding):
        self._closeExecEngine()
        # change the default value set by pdcservice to execute on an other SMD than the default one
        self._encoding = encoding 
        self._indexingClient = None
        
    def changeSmd(self, hostname, port):
        self._closeExecEngine()
        # change the default value set by pdcservice to execute on an other SMD than the default one
        self._smdHostName = hostname 
        self._smdPort = port             
    
    def checkOk(self, myclient, ret, message = None):
        if ret == None:
            self._log("Execution (%s) return is None" %(message))
            return            
        retWithoutTag = myclient._connection.unmarshall( ret )
        if retWithoutTag is None or retWithoutTag == '':
            if ret == '<OK/>\r\n':
                retWithoutTag = '0'
            else:
                retWithoutTag = '-1'
        returned = int(retWithoutTag)
        if returned != 0:
            if message != None:
                self._log("Execution (%s) return code not 0 : %d" %(message, returned))
            raise ExecutionException(myclient.getReturnDetail())
        if message != None:
            self._log("Execution (%s) ok" %(message))

    def addEnv (self, envVarName, envVarValue):
        self._log("addEnv %s=%s" % (envVarName, envVarValue))
        self._initExecEngine()
        self.checkOk(self._execEngineClient,self._execEngineClient.addEnv(envVarName, envVarValue))
        
    def addParam (self, paramVarName, paramVarValue):
        self._log("addParam %s=%s" % (paramVarName, paramVarValue))
        self._initExecEngine()
        self.checkOk(self._execEngineClient,self._execEngineClient.addParam(paramVarName, paramVarValue))

    def loadEnvProp (self, envPropertiesFileName, onlyIfExist = False):
        if onlyIfExist and not os.path.exists(envPropertiesFileName):
            return
        self._initExecEngine()
        self.checkOk(self._execEngineClient,self._execEngineClient.loadEnvProp(envPropertiesFileName))

    def loadEnginesProp (self, enginesPropertiesFileName, onlyIfExist = False):
        self.__lastEngineCommandLine = enginesPropertiesFileName
        if onlyIfExist and not os.path.exists(enginesPropertiesFileName):
            return
        self._initExecEngine()
        self.checkOk(self._execEngineClient,self._execEngineClient.loadEnginesProp(enginesPropertiesFileName))
        self.__engineCommandLineInited = True
    
    def start(self, engineKey, message = None):
        self._initExecEngine()
        if not self.__engineCommandLineInited:
            msg = []
            msg.append("WARNING : Engines Command Lines not inited !!!")
            msg.append("\t%s not loaded" % self.__lastEngineCommandLine)
            msg.append("\tSet BACKSTAGE_CONFIG_DIRECTORY environement variable to the directory where engines_unix.prop exists" )
            self._log("\n".join(msg))
        self.checkOk(self._execEngineClient,self._execEngineClient.start(engineKey),message)

    def startAssembly(self, inputDataFile = None, outputSgmlFile = None, templateId = None):
        self._initExecEngine()
        if inputDataFile != None:
            self.addParam('data', inputDataFile)
        if outputSgmlFile != None:
            self.addParam('sgml', outputSgmlFile)
        if templateId != None:
            self.addParam("assembly_opt", "-V STD5_TEMPLATE=%s.xml -V STD5_WITHDATA=YES -V STD5_OUTMODE=SGML" %(templateId))
        self.start("ENG_ASM_NAMED", 'Execute assembly engine')

    def startCodrCompo(self, inputSgmlFile = None, outputVpfFile = None, inputSgmlIdx = None, outputVpfIndex = None):
        self._initExecEngine()
        if inputSgmlFile != None:
            self.addParam('sgml', inputSgmlFile)
        if inputSgmlIdx != None:
            self.addParam('SGML_IndexFile', inputSgmlIdx)
        if outputVpfFile != None:
            self.addParam('vpf', outputVpfFile)
        if outputVpfIndex != None:
            self.addParam('VPF_IndexFile', outputVpfIndex)
        self.start("ENG_CODR_COMPO", 'Execute composition engine')
        
    def startCodrDrv(self, inputVpfFile, outputProtFile, driverType):
        self._initExecEngine()
        self.addParam('vpf', inputVpfFile)
        self.addParam('prot', outputProtFile)
        self.addParam('DriverType', driverType)
        self.start("ENG_CODR_DRV", 'Execute protocole engine')
        
    def startSort(self, inputVpfFile, inputComand):
        self._initExecEngine()
        self.addParam('vpf_in', inputVpfFile)
        self.addParam('cmd', inputComand)
        self.start("ENG_SORT_SINGLE", 'Execute protocole engine')

    def startSortList(self, inputList, inputComand):
        self._initExecEngine()
        self.addParam('lst', inputList)
        self.addParam('cmd', inputComand)
        self.start("ENG_SORT_LIST",'Execute protocole engine')

if __name__ == '__main__':
    
    backstage = Backstage()
    try :
        os.environ["PRODUCER_HOME"] = "G:\\SefasProducts\\mo61"
        os.environ["BACKSTAGE_CONFIG_DIRECTORY"] = "G:\\SefasProducts\\mo61\\home\\config"

        # os.environ["opInstallDir"] = "c:/oprint";
        backstage.addEnv("opWD","G:\\SefasProducts\\mo61\\home\\opWD")
        backstage.addEnv("opFam","default")
        backstage.addEnv("opAppli","client")
        backstage.addEnv("SystemRoot", "c:\\WINNT")
        
        backstage.addParam("opAppliNamed", "G:\\SefasProducts\\mo61\\home\\opWD\\default\\client\\program\\client")

        backstage.startAssembly("client.xml","toto.sgml","323")
        backstage.startCodrCompo("toto.sgml","toto.vpf")
        backstage.startCodrDrv("toto.vpf","toto.pdf","pdf")
        
        # myclient.manageExecReturn(myclient.start("ENG_GILLES"))
        backstage.close()

    except ExecutionException , e :
        print "service instanciation error : " , e.getErrorDetail()
    except SmdClientError , e :
        print "service instanciation error : " , str(e)

