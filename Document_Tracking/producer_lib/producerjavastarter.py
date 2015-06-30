#!/usr/bin/env python
import os

_JAVAHOME_='C:/j2sdk1.4.2_11/bin'
_DBG_JAVA_PORT_='18001'
_DBG_ORACLE_HOST_='10.0.4.17'
_DBG_ORACLE_PORT_='4000'

_JMX_SMD_PORT_ = '38004'
_JMX_JJD_PORT_ = '38005'
_JMX_JJC_PORT_ = '38006'
_JMX_MONSERVICE_PORT_ = '38007'
_JMX_TRAPV1_PORT_ = '38008'

_PRODUCER_HOME_='C:/PRODUCER'

_JMX_MARSHALLER_DAEMON_='com.sefas.jmx.smd.JmxMarshallerDaemon'
_JMX_MONITORING_SERVICE_='com.sefas.jmx.monservice.JmxMonitoringService'
_JMX_JJD_SERVER_='com.sefas.jmx.jjd.JmxJjdServer'
_JMX_JJC_SERVICE_='com.sefas.jmx.jjc.JmxJjcService'
_JMX_TRAP_RECEIVER_V1='com.sefas.jmx.trap.JmxTrapReceiverV1'

_MARSHALLER_DAEMON_='com.sefas.gridclient.MarshallerDaemon'
_MONITORING_SERVICE_='com.sefas.monservice.MonitoringService'
_JJD_SERVER_='com.sefas.jjd.JjdServer'
_JJC_SERVICE_='com.sefas.monservice.process.JjcService'
_TRAP_RECEIVER_V1='com.sefas.monservice.snmp.TrapReceiverV1'
_PRODUCER_SERVICE_='com.sefas.monservice.ProducerService'
_JES_SERVICE_='com.sefas.monservice.JESService'

_PRODUCER_STATUS_='com.sefas.monservice.status.ProducerStatus'
_SMD_STATUS_='com.sefas.monservice.status.SmdStatus'
_JJD_STATUS_='com.sefas.monservice.status.JjdStatus'

_CLEANUP_SCRIPT_='cleanup.sh'

_SMD_JAVALIB_PATH_='D:/producercurrentinstallation/SetUP_producer_1_0_Beta3_Build4/setup/installer/lib'
_SMD_JAR_LIST_= [ "sfsmdlware.jar" , \
                  "sefas-commons.jar" , \
                  "sfssrvbeans.jar" , \
                  "grid.jar" , \
                  "gridjmx.jar" , \
                  "log4j-1.2.16.jar" , \
                  "activemq-all-5.4.2.jar" , \
                  "flexjson.jar" , \
                  "frontoffice.jar" , \
                  "jobticket.jar" , \
                  "json.jar" , \
                  "jython.jar" , \
                  "workflow.jar" , \
                  "workflowserver.jar" , \
                  "xerces.jar" , \
                  "classes12.jar" , \
                  "mysql-connector-java-3.1.12-bin.jar", \
                  "sqljdbc4.jar", \
                  "commons-codec-1.4.jar", \
                  "db2jcc4.jar" ]

_ANT_JAVALIB_PATH_='D:/producercurrentinstallation/SetUP_producer_1_0_Beta3_Build4/setup/installer/lib-ant'
_ANT_JAR_LIST_= [ "ant.jar" , \
                  "xerces.jar" , \
                  "xml-apis.jar" , \
                  "optional.jar" ]
                  
_ANT_JAVALIB_PATH_='D:/producercurrentinstallation/SetUP_producer_1_0_Beta3_Build4/setup/installer/lib'
_PRODUCER_JAR_LIST_= [ "monservice.jar" , \
                       "producer-tools.jar" , \
                       "producersqlservices.jar" , \
                       "sefas-commons.jar" , \
                       "sfant.jar"  ,\
                       "sfssrvbeans.jar"  , \
                       "xerces.jar"  , \
                       "snmp4_13.jar"  , \
                       "commons-net-1.0.0.jar"  , \
                       "jce.jar"  , \
                       "reports.jar"  , \
                       "TechViewIII.jar"  , \
                       "hostconnect.jar"  , \
                       "jjd.jar"  , \
                       "classes12.jar"  , \
                       "commons-logging.jar"  , \
                       "log4j-1.2.16.jar"  , \
                       "jaxrpc.jar"  , \
                       "saaj.jar"  , \
                       "wsdl4j.jar"  , \
                       "sfsmdlware.jar"  , \
                       "activation.jar"  , \
                       "jasperreports-3.0.0.jar"  , \
                       "poi-3.0.1-FINAL-20070705.jar"  , \
                       "commons-collections-3.1.jar"  , \
                       "mail.jar"  , \
                       "mail-plugin.jar", \
                       "sefas-jmx.jar", \
                       "grid.jar", \
                       "mysql-connector-java-3.1.12-bin.jar", \
                       "sqljdbc4.jar", \
                       "commons-codec-1.4.jar", \
                       "db2jcc4.jar" ]
                  
START  = 0
STOP   = 1
STATUS = 2
DEBUG = 3
KILL = 4
LSTATUS = 5

import sys
isWindows = sys.platform[0:3] == 'win'

                  
class JavaLauncher :
    """ 
      launch the java interpretor and misc usefull Java dbtools 
      from a python shell
    """

    def __init__( self , javaloc ,  detach = False , debug = False , vmArgs = None  ) :
        self._javaloc = javaloc
        self._vmArgs = None
        self._curloc = None
        self._curArgs  = None
        if vmArgs != None :
            #  populate java System arguments
            self._vmArgs = []
            for  key in vmArgs :
                self._vmArgs.append( '-D%s=%s' % (key,vmArgs[key]) )
        if debug :
            if self._vmArgs is None:
                self._vmArgs = []
            #  self._vmArgs.append( '-D%s=%s' % ('DBG_ORACLE_HOST',_DBG_ORACLE_HOST_) )
            #  self._vmArgs.append( '-D%s=%s' % ('DBG_ORACLE_PORT',_DBG_ORACLE_PORT_) )
            self._vmArgs.append( '-Xdebug' )
            self._vmArgs.append( '-Xrunjdwp:transport=dt_socket,address=%s,server=y,suspend=n' % (_DBG_JAVA_PORT_) )
        if os.environ.get('PROFILE') != None :
            if self._vmArgs is None :
                self._vmArgs = []
            print 'profiling is on : ' , os.environ.get('PROFILE')
            self._vmArgs.append(os.environ.get('PROFILE'))
        if detach :
            self._detach   = os.P_NOWAIT
        else :
            self._detach = os.P_WAIT
            
    def checkJars( self , jars ) :
        """ check jars file existance and return None or non Existing jar list """
        succeeded = True
        for jar in jars :
            if not os.path.isfile(jar) :
                print  "ERROR : requested jar %s has not been found " % (jar) 
                succeeded = False
        return succeeded
        
    def getPluginJarLst(self, configDir, pluginLstKey):
        """ search jarPlugin.dict file to get the list of jar of the key pluginLstKey """
        resu = []
        jarDictFileName = "%s/%s" % (configDir, "jarPlugin.dict" )
        if os.path.isfile(jarDictFileName):
            f=open(jarDictFileName,'r')
            jarDict=eval(f.readline())
            f.close()
            if jarDict.get(pluginLstKey, None) is not None:
                resu.extend(jarDict[pluginLstKey])
        return resu

    def _setLog4j(self) :
        """ set remote debug mode if requested by REMOTEDBG=YES environment """
        if os.environ.get('LOG4J') != None :
            if self._vmArgs == None :
                self._vmArgs = []
            self._vmArgs.append('-Dlog4j.configuration=%s' % (os.environ.get('LOG4J') ) )
        pass    

    def _prepare( self , className , jars , args ) :
        """ prepare for execution """
        classep = os.pathsep
        self._setLog4j()
        self._curloc = "%s/%s" % (self._javaloc, "java" )
        if isWindows:
            self._curloc = "%s/%s" % (self._javaloc, "java.exe" )
        if self._vmArgs != None :    
            self._curArgs = self._vmArgs + [  '-cp', classep.join(jars) , className  ] + args
        else :
            self._curArgs = [  '-cp' , classep.join(jars) , className  ] + args
            
    def execute ( self , className , jars , args ) :
        """ start given class execution in spawn mode"""
        self._prepare(className , jars , args)
        # uncomment following line to debug spawned java command
        # print '%s %s' % ( self._curloc , ' '.join(self._curArgs) ) 
        if isWindows:
            # spawnv acts weird on windows. We don't want the executable first, but we need something innocuous
            self._curArgs.insert(0 , "-v" )
        else:
            # on Linux do the correct thing
            self._curArgs.insert(0 , self._curloc ) # insert executable as first arg
        
        # print "Detach: ", self._detach , " curloc: ", self._curloc , " curArgs: ", self._curArgs
        return os.spawnv( self._detach , self._curloc , self._curArgs )
        

    def popen ( self , className , jars , args ) :
        """ pipe current class execution """
        self._prepare(className , jars , args)
        # check for spaces in javaloc
        if self._javaloc.find(' ') != -1 :
            _curloc = '"%s"' % (self._curloc)
        else:
            _curloc = self._curloc
        print '%s %s' % ( _curloc , ' '.join(self._curArgs) ) 
        fi,foe = os.popen4( _curloc + ' ' +  ' '.join(self._curArgs) )
        fi.close()
        lines = foe.readlines()
        print ''.join(lines)
        foe.close()

class SmdLauncher  ( JavaLauncher ) :
    """ launch Smd ineriting from java """

    def __init__( self , javaloc , javaLibPath, myConfPath , port=None , detach = True , action = START , jmx = False) :
        JavaLauncher.__init__(self,javaloc,detach, action==DEBUG)
        if self._vmArgs == None :
            self._vmArgs = []
        self._vmArgs.append( '-Xms256m' )
        self._vmArgs.append( '-Xmx800m' )
        self._vmArgs.append( '-XX:+HeapDumpOnOutOfMemoryError' )
        if action == START and jmx :
            # enable remote JMX monitoring for SMD supervision
            self._vmArgs.append( '-Dcom.sun.management.jmxremote' )
            self._vmArgs.append( '-Dcom.sun.management.jmxremote.port=%s' % ( _JMX_SMD_PORT_ )  )
            self._vmArgs.append( '-Dcom.sun.management.jmxremote.authenticate=false'  )
            self._vmArgs.append( '-Dcom.sun.management.jmxremote.ssl=false'  )
        if action == START or action == DEBUG :
            self._vmArgs.append( '-Dpython.home=${PRODUCER_HOME_}/home/workflowlib'  )
            self._vmArgs.append( '-Dengines.envprop=${PRODUCER_HOME_}/home/config/backstage/env_unix.prop' )
            self._vmArgs.append( '-Dinittemplate=Startup.py'  )
        extJarLst = self.getPluginJarLst(myConfPath, 'PLUGIN_SERVICES_JARS')
        self._smdJarList =  _SMD_JAR_LIST_
        if extJarLst is not None:
            self._smdJarList.extend(extJarLst)
        wkList = [ ''.join([javaLibPath,'/',str(value)]) for value in self._smdJarList ] 
        self._smdJarList = wkList
        if jmx :
            self._javaClass = 'com.sefas.jmx.smd.JmxMarshallerDaemon' 
        else :    
            self._javaClass = 'com.sefas.gridclient.MarshallerDaemon' 
        self._args = []
        if os.environ.get('PRODUCER_HOME') is not None:
            self._args.append('-Home')
            self._args.append(os.environ.get('PRODUCER_HOME') + '/home/config/backstage')
            self._args.append('-Encoding')
            self._args.append('ISO-8859-1')
            self._args.append('-Load')
            self._args.append('com.sefas.gridclient.MProcessFactory')
        
        if port is not None:
            self._args.append('-P')
            self._args.append(str(port))
        if action == STOP :
            self._args.append('-kill')
        elif action == STATUS :
            self._args.append('-status')
            
    def launch ( self ) : 
        if self.checkJars(self._smdJarList) : 
            return self.execute( self._javaClass , self._smdJarList , self._args )
	return None
    def pipe ( self ) : 
        """ popen is mainly used by installer """
        if self.checkJars(self._smdJarList) : 
            return self.popen( self._javaClass , self._smdJarList , self._args )
        return None
	
class AntLauncher  ( JavaLauncher ) :
    """ launch Ant ineriting from java """

    def __init__( self , javaloc , javaLibPath , myAntScript , mytarget) :
        JavaLauncher.__init__(self,javaloc)
        self._antJarList = _ANT_JAR_LIST_
        wkList = [ ''.join([javaLibPath,'/',str(value)]) for value in self._antJarList ]          
        self._antJarList = wkList
        self._javaClass = 'org.apache.tools.ant.Main'                      
        self._args = []
        self._args.append('-buildfile')
        self._args.append(myAntScript)
        self._args.append(mytarget)
    

    def launch ( self ) : 
        if self.checkJars(self._antJarList)  :
            self.execute( self._javaClass , self._antJarList , self._args )
        
    def pipe ( self ) : 
        """ popen is mainly used by installer """
        if self.checkJars(self._antJarList) : 
            self.popen( self._javaClass , self._antJarList , self._args )
	
class ProducerLauncher( JavaLauncher ) :
    """ launch a Producer Java Daemon inheriting from java """

    def __init__( self , javaloc , javaLibPath , extJarLst , detach = False , debug = False , vmArgs = None) :
        JavaLauncher.__init__(self,javaloc,detach,debug,vmArgs)
        self._producerJarList = _PRODUCER_JAR_LIST_
        if extJarLst is not None:
            self._producerJarList.extend(extJarLst)
        wkList = [ ''.join([javaLibPath,'/',str(value)]) for value in self._producerJarList ]          
        self._producerJarList = wkList
        self._javaClass = None      
        self._args = []

    def launch ( self ) : 
        if self.checkJars(self._producerJarList)  :
            self._producerJarList.append('%s/reports/localization' % os.environ.get('PRODUCER_HOME'))
            self.execute( self._javaClass , self._producerJarList , self._args )
    
class JjdLauncher  ( ProducerLauncher ) :
    """ launch Jjd ineriting from ProducerLauncher """

    def __init__( self , javaloc , javaLibPath , myConfPath , action = START, jmx = False ) :
        detach=False
        ProducerLauncher.__init__(self, javaloc, javaLibPath, None, detach, action==DEBUG)
        if action == START and jmx :
            if self._vmArgs == None :
                self._vmArgs = []
            # enable remote JMX monitoring for SMD supervision
            self._vmArgs.append( '-Dcom.sun.management.jmxremote' )
            self._vmArgs.append( '-Dcom.sun.management.jmxremote.port=%s' % ( _JMX_JJD_PORT_ )  )
            self._vmArgs.append( '-Dcom.sun.management.jmxremote.authenticate=false'  )
            self._vmArgs.append( '-Dcom.sun.management.jmxremote.ssl=false'  )
        if jmx :
            self._javaClass = _JMX_JJD_SERVER_
        else :    
        	self._javaClass = _JJD_SERVER_                      
        if self._vmArgs is None:
            self._vmArgs = []
        # increase the memory for JJD service
        self._vmArgs.append( '-Xmx128m' )
        self._args.append('-conf')
        self._args.append('%s/jjd.conf' % (myConfPath) )
        if action == STOP :
            self._args.append('-stop')
        elif action == STATUS :
            self._args.append('-status')

class JjcLauncher  ( ProducerLauncher ) :
    """  launch Jjc ineriting from ProducerLauncher (no -stop no -start) """

    def __init__( self , javaloc , javaLibPath , myConfPath , action = START, jmx = False ) :
        ProducerLauncher.__init__(self, javaloc, javaLibPath, None, detach=False)
        if action == START and jmx :
            if self._vmArgs == None :
                self._vmArgs = []
            # enable remote JMX monitoring for SMD supervision
            self._vmArgs.append( '-Dcom.sun.management.jmxremote' )
            self._vmArgs.append( '-Dcom.sun.management.jmxremote.port=%s' % ( _JMX_JJC_PORT_ )  )
            self._vmArgs.append( '-Dcom.sun.management.jmxremote.authenticate=false'  )
            self._vmArgs.append( '-Dcom.sun.management.jmxremote.ssl=false'  )
        if jmx :
            self._javaClass = _JMX_JJC_SERVICE_
        else :    
        	self._javaClass = _JJC_SERVICE_
        self._args.append('-cfg')
        self._args.append('%s/mservice.xml' % (myConfPath) )
        self._args.append('-ps')
        self._args.append('JJC')
        if action == STOP :
            self._args.append('-stop')
        elif action == STATUS :
            self._args.append('-status')

class EncryptLauncher  ( ProducerLauncher ) :
    """ launch Encrypt inheriting from ProducerLauncher """

    def __init__( self , javaloc , javaLibPath , myConfPath ) :
        ProducerLauncher.__init__(self, javaloc, javaLibPath, None, detach=False)
        self._javaClass = 'com.sefas.monservice.config.Encrypt'                      
        self._args.append('-g')
        self._args.append('-k')
        self._args.append('%s/security/httpbeancrypt128' % (myConfPath) )
        self._args.append('-p')
        self._args.append('AES/CBC/PKCS5Padding'  )

class MonitoringServiceLauncher  ( ProducerLauncher ) :
    """ launch MonitoringService inheriting from ProducerLauncher """

    def __init__( self , javaloc , javaLibPath , myConfPath , action = START , all = False, jmx = False ) :
        # build monitorig requested vmArgs
        myvmArgs = {}
        jaasConfig = '%s/security/jaasserver.conf' % (myConfPath)
        myvmArgs['java.security.auth.login.config'] = jaasConfig
        myvmArgs['PRODUCER_HOME'] = os.environ['PRODUCER_HOME']
        detach=False
        jarPluginLst = self.getPluginJarLst(myConfPath, 'PLUGIN_SERVICES_JARS')
        ProducerLauncher.__init__(self, javaloc, javaLibPath, jarPluginLst, detach, action==DEBUG, vmArgs=myvmArgs )
        if action == START and jmx :
            if self._vmArgs == None :
                self._vmArgs = []
            # enable remote JMX monitoring for SMD supervision
            self._vmArgs.append( '-Dcom.sun.management.jmxremote' )
            self._vmArgs.append( '-Dcom.sun.management.jmxremote.port=%s' % ( _JMX_MONSERVICE_PORT_ )  )
            self._vmArgs.append( '-Dcom.sun.management.jmxremote.authenticate=false'  )
            self._vmArgs.append( '-Dcom.sun.management.jmxremote.ssl=false'  )
        if jmx :
            self._javaClass = _JMX_MONITORING_SERVICE_
        else :    
	        self._javaClass = _MONITORING_SERVICE_
        # increase the memory for monitoring service
        self._vmArgs.append( '-Xmx256m' )
        if action == STOP :
            self._args.append('-stop')
        elif action == STATUS :
            self._args.append('-status')
        # self._args.append('-profile')
        # self._args.append('1')
        self._args.append('-cfg')
        self._args.append( '%s/mservice.xml' % (myConfPath) ) ;
        #self._args.append('-nodaemon')
        self._args.append('-notrap')
        self._args.append('-psrvcfg')
        self._args.append( '%s/jservices.properties' % (myConfPath) ) ;
        if all :
            self._args.append('-psrv')
            # self._args.append('-dv4srv')
            # self._args.append('-psrvctl')
        self._args.append('-rdir')
        self._args.append( '%s/reports' % os.environ.get('PRODUCER_HOME') ) ;

class ProducerServiceLauncher  ( ProducerLauncher ) :
    """ launch ProducerService inheriting from ProducerLauncher """

    def __init__( self , javaloc , javaLibPath , myConfPath , action = START , all = False ) :
        detach=False
        ProducerLauncher.__init__(self, javaloc, javaLibPath, None, detach, action==DEBUG )
        self._javaClass = _PRODUCER_SERVICE_
        if action == STOP :
            self._args.append('-stop')
        elif action == START :
            self._args.append('-start')
        elif action == STATUS :
            self._args.append('-status')
        self._args.append('-cfg')
        self._args.append( '%s/mservice.xml' % (myConfPath) ) ;

class ProducerStatusLauncher  ( ProducerLauncher ) :
    """ launch ProducerStatus inheriting from ProducerLauncher """

    def __init__( self , javaloc , javaLibPath , myConfPath , daemonName, action = STATUS ) :
        detach=False
        ProducerLauncher.__init__(self, javaloc, javaLibPath, None, detach, action==DEBUG )
        if action == LSTATUS :
            self._args.append('-lstatus')
        elif action == STATUS :
            self._args.append('-status')
            self._args.append('-nologo')
        self._javaClass = _PRODUCER_STATUS_
        self._args.append('-cfg')
        self._args.append( '%s/mservice.xml' % (myConfPath) ) ;
        self._args.append('-d')
        self._args.append('%s' % (daemonName))

class JjdStatusLauncher  ( ProducerLauncher ) :
    """ launch JjdStatus inheriting from ProducerLauncher """

    def __init__( self , javaloc , javaLibPath , myConfPath , action = START ) :
        detach=False
        ProducerLauncher.__init__(self, javaloc, javaLibPath, None, detach, action==DEBUG )
        if action == LSTATUS :
            self._args.append('-lstatus')
        elif action == STATUS :
            self._args.append('-status')
            self._args.append('-nologo')
        self._javaClass = _JJD_STATUS_
        self._args.append('-cfg')
        self._args.append('%s/jjd.conf' % (myConfPath) )

class SmdStatusLauncher  ( ProducerLauncher ) :
    """ launch SmdStatus inheriting from ProducerLauncher """

    def __init__( self , javaloc , javaLibPath , host, port, action = START ) :
        detach=False
        ProducerLauncher.__init__(self, javaloc, javaLibPath, None, detach, action==DEBUG )
        if action == LSTATUS :
            self._args.append('-lstatus')
        elif action == STATUS :
            self._args.append('-status')
            self._args.append('-nologo')
        self._javaClass = _SMD_STATUS_
        self._args.append('-host')
        self._args.append('%s' % (host) )
        self._args.append('-port')
        self._args.append('%s' % (port) )
            
class JesEntryUpdateLauncher  ( ProducerLauncher ) :
    """ launch JesEntryUpdate inheriting from ProducerLauncher """

    def __init__( self , javaloc , javaLibPath , myConfPath , action = START ) :
        # build monitorig requested vmArgs
        myvmArgs = {}
        jaasConfig = '%s/security/jaasserver.conf' % (myConfPath)
        myvmArgs['java.security.auth.login.config'] = jaasConfig
        myvmArgs['PRODUCER_HOME'] = os.environ['PRODUCER_HOME']
        detach=False
        ProducerLauncher.__init__(self, javaloc, javaLibPath, None ,detach, action==DEBUG )
        self._javaClass = 'com.sefas.monservice.JESService'                      
        if action == STOP :
            self._args.append('-resetjesentryupdate')
        elif action == STATUS :
            self._args.append('-getjesentryupdatestatus')
        else :
            self._args.append('-startjesentryupdate')
        self._args.append('-cfg')
        self._args.append( '%s/mservice.xml' % (myConfPath) ) ;
            

class TrapServiceLauncher  ( ProducerLauncher ) :
    """ launch TrapServiceLauncher inheriting from ProducerLauncher """

    def __init__( self , javaloc , javaLibPath , myConfPath , action = START, jmx = False ) :
        self._vmArgs = {}
        detach=False
        ProducerLauncher.__init__(self, javaloc, javaLibPath, None, detach, action==DEBUG )
        if action == START and jmx :
            if self._vmArgs == None :
                self._vmArgs = []
            # enable remote JMX monitoring for SMD supervision
            self._vmArgs.append( '-Dcom.sun.management.jmxremote' )
            self._vmArgs.append( '-Dcom.sun.management.jmxremote.port=%s' % ( _JMX_TRAPV1_PORT_ )  )
            self._vmArgs.append( '-Dcom.sun.management.jmxremote.authenticate=false'  )
            self._vmArgs.append( '-Dcom.sun.management.jmxremote.ssl=false'  )
        if jmx :
        	self._javaClass = _JMX_TRAP_RECEIVER_V1
        else :    
        	self._javaClass = _TRAP_RECEIVER_V1
        if action == STOP :
            self._args.append('-stop')
        elif action == STATUS :
            self._args.append('-status')
        self._args.append('-cfg')
        self._args.append('%s/mservice.xml' % (myConfPath) )
        self._args.append('-sp')
        self._args.append('4001')
        if action != STOP and action != STATUS :
            self._args.append('-ts')
            self._args.append('TRAPV1')
            
class OsLauncher :
    """ 
    launch Unix script from a python shell
    """

    def __init__( self , producerHome ) :
        self._curloc = None
        self._producerHome = producerHome
        self._detach = os.P_WAIT
   
    def kill ( self , scriptName , serviceName ) : 
        """ start given unix script in spawn mode"""
        self._curloc = "%s/bin/%s" % (self._producerHome, scriptName )
        args = []
        args.append(self._curloc)
        args.append(serviceName)
        print self._detach , self._curloc , args
        return os.spawnv( self._detach , self._curloc , args )
		

def startSmd(producerHome, javaHome, javaLibPath, myConfPath, port=None , detach = False , action = START ) :
    if action == KILL :
        osl = OsLauncher(producerHome)
        return osl.kill(_CLEANUP_SCRIPT_ , _MARSHALLER_DAEMON_ )
    else :
        smd = SmdLauncher(javaHome,javaLibPath, myConfPath, port ,detach,action)
        smd.launch()

def startAnt(javaHome, javaLibPath, myantScript, mytarget) :
    """ this entry is mainly used by installer """
    ant = AntLauncher(javaHome,javaLibPath, myantScript, mytarget)
    return ant.pipe()
    
def jjdDaemon(producerHome, javaHome, javaLibPath, myConf , action = START, jmx = False  ) :
    if action == KILL :
        osl = OsLauncher(producerHome)
        if jmx :
            return osl.kill(_CLEANUP_SCRIPT_ , _JMX_JJD_SERVER_ )
        else :
        	return osl.kill(_CLEANUP_SCRIPT_ , _JJD_SERVER_ )
    else :
        jjd = JjdLauncher(javaHome,javaLibPath, myConf , action, jmx )
        return jjd.launch()
    

def smdDaemon(producerHome, javaHome, javaLibPath, myConfPath, myport , action = START , jmx = False ):
    if action == KILL :
        osl = OsLauncher(producerHome)
        if jmx :
            return osl.kill(_CLEANUP_SCRIPT_ , _JMX_MARSHALLER_DAEMON_ )
        else :
            return osl.kill(_CLEANUP_SCRIPT_ , _MARSHALLER_DAEMON_ )
    else :
        if myport.isdigit() :
            initEnvVariables()
            smd = SmdLauncher(javaHome,javaLibPath, myConfPath, int(myport) , False , action, jmx)
            print os.environ
            return smd.launch()
        else :
            print "smd port must be numerical found : %s" % (myport)

    
def monitoringDaemon(producerHome, javaHome, javaLibPath, myConfPath , action = START , all = False, jmx = False) :
    if action == KILL :
        osl = OsLauncher(producerHome)
        if jmx :
            return osl.kill(_CLEANUP_SCRIPT_ , _JMX_MONITORING_SERVICE_ )
        else :
        	return osl.kill(_CLEANUP_SCRIPT_ , _MONITORING_SERVICE_ )
    else :
        mon = MonitoringServiceLauncher(javaHome,javaLibPath, myConfPath , action , all, jmx )
        return mon.launch()

def producerService(producerHome, javaHome, javaLibPath, myConfPath , action = START , all = False) :
    if action == KILL :
        osl = OsLauncher(producerHome)
        return osl.kill(_CLEANUP_SCRIPT_ , _PRODUCER_SERVICE_ )
    else :
        mon = ProducerServiceLauncher(javaHome,javaLibPath, myConfPath , action , all )
        return mon.launch()
    
def trapDaemon(producerHome, javaHome, javaLibPath, myConfPath , action = START, jmx = False) :
    if action == KILL :
        osl = OsLauncher(producerHome)
        if jmx :
            return osl.kill(_CLEANUP_SCRIPT_ , _JMX_TRAP_RECEIVER_V1 )
        else :
        	return osl.kill(_CLEANUP_SCRIPT_ , _TRAP_RECEIVER_V1 )
    else :
        trap = TrapServiceLauncher(javaHome,javaLibPath, myConfPath , action, jmx )
        return trap.launch()

def producerStatus(producerHome, javaHome, javaLibPath, myConfPath , daemonName, action = STATUS) :
    if action == KILL :
        osl = OsLauncher(producerHome)
       	return osl.kill(_CLEANUP_SCRIPT_ , _PRODUCER_STATUS_ )
    else :
        status = ProducerStatusLauncher(javaHome,javaLibPath, myConfPath , daemonName, action )
        return status.launch()

def jjdStatus(producerHome, javaHome, javaLibPath, myConfPath, action = STATUS) :
    if action == KILL :
        osl = OsLauncher(producerHome)
       	return osl.kill(_CLEANUP_SCRIPT_ , _JJD_STATUS_ )
    else :
        status = JjdStatusLauncher(javaHome,javaLibPath, myConfPath, action )
        return status.launch()

def smdStatus(producerHome, javaHome, javaLibPath, host, port, action = STATUS) :
    if action == KILL :
        osl = OsLauncher(producerHome)
       	return osl.kill(_CLEANUP_SCRIPT_ , _SMD_STATUS_ )
    else :
        status = SmdStatusLauncher(javaHome,javaLibPath, host, port, action )
        return status.launch()

def encrypt(javaHome, javaLibPath, myConfPath  ) :
    crypt = EncryptLauncher(javaHome,javaLibPath, myConfPath  )
    return crypt.launch()
    
def jesentryupdate(producerHome, javaHome, javaLibPath, myConfPath  ) :
    jeu = JesEntryUpdateLauncher(javaHome,javaLibPath, myConfPath  )
    return jeu.launch()
    
def jjcstarter(producerHome, javaHome, javaLibPath, myConfPath , action = START, jmx = False ) :
    if action == KILL :
        osl = OsLauncher(producerHome)
        if jmx :
            return osl.kill(_CLEANUP_SCRIPT_ , _JMX_JJC_SERVICE_ )
        else :
        	return osl.kill(_CLEANUP_SCRIPT_ , _JJC_SERVICE_ )
    else :
        jjc = JjcLauncher(javaHome,javaLibPath, myConfPath , action, jmx  )
        return jjc.launch()
        
def dlauncher(producerHome, javaHome, javaLibPath, myConfPath , action = START, jmx = False ) :
    initEnvVariables()
    os.system('${PRODUCER_HOME_}/bin/backstage/${DATABASE_OS_TYPE_LOWER}/dlauncher -p 29802 & echo $! > ${PRODUCER_HOME_}/bin/backstage/${DATABASE_OS_TYPE_LOWER}/dlauncher.pid')    

def initOsEnv(varName,varValue,defaultVarValue):
    if varValue[0] == '$' : # <= not changed assume standalone launch
        os.environ[varName] = defaultVarValue
    else:
        os.environ[varName] = varValue
    
    
def initEnvVariables():
    # init Producer environment variable to make them available for scripts called by SMD
    initOsEnv('PRODUCER_HOME','${PRODUCER_HOME_}','/home/producer')
    initOsEnv('PRODUCER_HOST','${PRODUCER_HOST_}','localhost')
    initOsEnv('PRODUCER_NFS','${PRODUCER_NFS_}','')
    initOsEnv('REMAKEHOST','${REMAKEHOST}','localhost')
    initOsEnv('LOGGING_DIRECTORY','${LOGGING_DIRECTORY}','/home/producer/data/traffic/log')
    initOsEnv('LOG_DIRECTORY','${LOG_DIRECTORY}','/home/producer/data/traffic/log')
    initOsEnv('TEMPORARY_DIRECTORY','${TEMPORARY_DIRECTORY}','/home/producer/data/traffic/temp')
    initOsEnv('TRAFFIC_DIRECTORY','${TRAFFIC_DIRECTORY}','/home/producer/data/traffic')
    initOsEnv('TRANSFER_DIRECTORY','${TRANSFER_DIRECTORY}','/home/producer/data/traffic/transfer')
    initOsEnv('TRANSFER_OUT_DIRECTORY','${TRANSFER_OUT_DIRECTORY}','/home/producer/data/traffic/jobs')
    initOsEnv('LOGGING_FILE','${LOGGING_FILE}','/home/producer/data/traffic/log/pythonScript.log')
    initOsEnv('ORACLE_HOST','${ORACLEHOST}','localhost')
    initOsEnv('DATABASE_TYPE','${DATABASE_TYPE_}','oracle')
    initOsEnv('JDBC_DRIVER','${JDBCDRIVER_}','oracle.jdbc.driver.OracleDriver')
    initOsEnv('JDBC_STRING','${DATABASE_}','jdbc:oracle:thin:@figaro:1521:FIGARODB')
    initOsEnv('PRODUCER_DB_USER_','${PRODUCER_DB_USER_}','producer')
    initOsEnv('PRODUCER_DB_PASSWRD_','${PRODUCER_DB_PASSWRD_}','producer')
    initOsEnv('SMD_HOST','${SMD_HOST_}','localhost')
    initOsEnv('SMD_PORT','${SMD_PORT_NUMBER}','29110') 
    initOsEnv('BACKSTAGE_CONFIG_DIRECTORY','${PRODUCER_HOME_}/home/config/backstage','/home/producer/home/config/backstage')
    initOsEnv('PRODUCER_OS','${PRODUCER_OS_}','LNX')
    initOsEnv('PROCESSING_SCRIPTS_DIRECTORY','${PROCESSING_SCRIPTS_DIRECTORY}','/home/producer/scripts/job_scripts')
    # init Producer environment variable to make them available for scripts called by SMD 
    initOsEnv('LD_LIBRARY_PATH','PYTHONHOME/lib/python2.6/lib-dynload','${PRODUCER_HOME_}') 
    initOsEnv('LIBPATH','PYTHONHOME/lib/python2.6/lib-dynload','${PRODUCER_HOME_}') 
    
    if os.environ.get('PYTHONPATH') != None:
        initOsEnv('PYTHONPATH','${DIRECTOR_ROOT_DIRECTORY}/lib/ProducerPythonLibrary.zip:${DIRECTOR_ROOT_DIRECTORY}/lib/ProjectorPythonLibrary.zip:%s' % (os.environ.get('PYTHONPATH')),os.environ.get('PYTHONPATH'))
    else:
        initOsEnv('PYTHONPATH','${DIRECTOR_ROOT_DIRECTORY}/lib/ProducerPythonLibrary.zip:${DIRECTOR_ROOT_DIRECTORY}/lib/ProjectorPythonLibrary.zip',None)

if __name__ == '__main__':
    """ main is used for testing purposes only """
    pid = startSmd(None, _JAVAHOME_, _PRODUCER_HOME_, _SMD_JAVALIB_PATH_)
    print "pid = %s" % (pid)
    os.environ['DEST_DIR']='D:/producercurrentinstallation/SetUP_producer_1_0_Beta3_Build4'
    os.environ['SOURCE_DIR']='D:/producercurrentinstallation/SetUP_producer_1_0_Beta3_Build4'
    os.environ['LOCAL_DIR']='D:/producercurrentinstallation/SetUP_producer_1_0_Beta3_Build4/setup/installer'
    os.environ['PRODUCER_DIR']='D:/producercurrentinstallation/SetUP_producer_1_0_Beta3_Build4/setup'
    antScript ='D:/producercurrentinstallation/SetUP_producer_1_0_Beta3_Build4/producer/installer/producer-scripts-build/build-producer-package.xml'
    target = 'only-make-war-file'
    print "PID =",startAnt(_JAVAHOME_, _ANT_JAVALIB_PATH_, antScript, target)
