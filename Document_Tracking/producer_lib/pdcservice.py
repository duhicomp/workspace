#!/usr/bin/env python
import producerjavastarter 
import sys 
import os

_VERSION_ = "1.00.007"

_SERVICES_ = { \
               'jjd'  :'Java Jes Daemon Producer Service' , \
               'mon'  :'Java Producer Monitoring Service minimal' , \
               'allmon'  :'Java Producer Monitoring Service FULL' , \
               'smd'  :'Java Smd Service JRE 1.4' , \
               'traps':'Java SNMP traps service' , \
               'jjcstarter':'Java JES Client stored proc starter' , \
               'smdjmx'  :'Java Smd Service JMX monitored => JRE 1.5' , \
               'jjdjmx'  :'Java Jes Daemon Producer Service' , \
               'monjmx'  :'Java Producer Monitoring Service minimal' , \
               'allmonjmx'  :'Java Producer Monitoring Service FULL' , \
               'trapsjmx':'Java SNMP traps service' , \
               'jjcstarterjmx':'Java JES Client stored proc starter' , \
               'jesentryupdate':'Java JES entry update service' , \
               'encrypt':'Java Encrypt Utility' , \
               'psrv':'Java Producer Service', \
               'dlauncher':'dlauncher' \
            }
_STOP_ = '-stop'
_START_ = '-start'
_DEBUG_ = '-debug'
_KILL_ = '-kill'
_LOG4J_ = 'Log4J.properties'

#
# Developpers : PLEASE USE THE TWO CONSTANT BELOW TO SETUP YOUR PRODUCER DIRECTORIES 
#               AT DEVELOPMENT TIME ; this two variable are not use in production
#
_DEVELOPMENT_PRODUCER_HOME_PATH_ = 'D:\\producercurrentinstallation\\SetUP_producer_1_0_Beta3_Build4\\setup\\installer\\producer-scripts-build\\producer'
_DEVELOPMENT_PRODUCER_JAVALIB_PATH_ = 'D:\\producercurrentinstallation\\SetUP_producer_1_0_Beta3_Build4\\setup\\installer\\lib'

class ProducerServiceStarter :
    """ 
      this class usage is starting all kind of producer dameon 
      (Jjd , MonitoringServices ....) using the semantics defined inside
      producerjavastarter module and the simplest possible syntax
      pdcservice daemonname [-start | -stop ]    
    """

    def __init__( self ) : 
        self.hasInited = False
        if len( sys.argv ) < 2 :
            print "missing argument requested service name expected : %s " % (str(_SERVICES_.keys()))
        else :
            self._svcName = sys.argv[1].lower()
            if len( sys.argv ) > 2  :
                self._action  = sys.argv[2]
                if self._action != '-start' and self._action != '-stop' and self._action != '-status' and self._action != '-debug' and self._action != '-kill' :
                    print 'ERROR : %s is invalid : -start, -stop, -debug, -kill or -status expected' % (self._action)
            else :
                if self._svcName != 'encrypt' :
                    self._action = '-status'
                    print 'WARNING : no -start -stop -status actions specified => assuming -status'
        
            try :
                description = _SERVICES_ [self._svcName] 
                print 'identified service = %s' % (description) 
                self._conf    = None 
                self._javalibPath = None
                self._producerHome = None
                self._producerConfPath = None
                self._jjdConfPath = None
                self._logdir = '${LOG_DIRECTORY}'
                if self._logdir[0] != '$' :
                    os.environ['LOG4J'] = '%s/%s' %(self._logdir,_LOG4J_)
                self._smdPort = '${SMD_PORT_NUMBER}'
                # defaut to 29100 if not substituted
                if self._smdPort[0] == '$' :
                    self._smdPort = '29100'
                    self._javalibPath = _DEVELOPMENT_PRODUCER_JAVALIB_PATH_
                self.hasInited = True
            except KeyError :
                print 'FATAL : resquested %s service is an undefined service' % (self._svcName)
            
    def _validDirectory( self , dire ) :        
        if os.path.exists(  dire )  and  os.path.isdir(  dire ) :
            return True
        return False

    def _sanityCheck( self ) :
        """ check for expected directories and other similar stuff """
        if not self._validDirectory ( self._producerHome )   :
            print 'inexisting or invalid PRODUCER_HOME '
            return False
        if self._javalibPath == None : # production case     
            self._javalibPath = "%s/lib" % ( self._producerHome )       
        if not self._validDirectory ( self._javalibPath  )  :
            print 'inexisting or invalid PRODUCER java lib : %s ' % (self._javalibPath)
            return False
        self._producerConfPath = "%s/home/config/producer" % ( self._producerHome )
        if not self._validDirectory ( self._producerConfPath  )  :
            print 'inexisting or invalid PRODUCER configuration : %s ' % (self._producerConfPath)
            return False
        self._jjdConfPath = "%s/home/jjd" % ( self._producerHome )       
        if not self._validDirectory ( self._jjdConfPath  )  :
            print 'inexisting or invalid PRODUCER configuration : %s ' % (self._jjdConfPath)
            return False
        # check the Logging stuff
        destLog4j = os.environ['LOG4J'] ;
        srcLog4j  = "%s/%s" % ( self._producerConfPath , _LOG4J_ )
        import shutil
        if not os.path.isfile(srcLog4j) :
            if os.path.isfile(destLog4j) :
                # dest is there (initial) save it in safe place
                shutil.copyfile(destLog4j,srcLog4j)
            else :
                print 'inexisting or invalid PRODUCER Log4J configuration file : %s ' % (srcLog4j)
                return False
        if not os.path.isfile(destLog4j) :
            # Log4J not there populate from home/config/producer
            shutil.copyfile(srcLog4j,destLog4j)
        # finally provide Log4J write to oracle for logging  
        logger = "%s/producerlog4jServices.log" % (self._logdir)
        if not os.access( logger , os.F_OK ) :
            os.system("touch %s" % (logger) )
        os.system( "chmod 666 %s" % (logger) )
        return True

    def launch( self ) :
        """ launch the daemon """
        myAction = producerjavastarter.STATUS # defaulted
        if self._action == _STOP_ :
            myAction = producerjavastarter.STOP
        elif self._action == _START_ :
            myAction = producerjavastarter.START
        elif self._action == _DEBUG_ :
            myAction = producerjavastarter.DEBUG
        elif self._action == _KILL_ :
            myAction = producerjavastarter.KILL
        # check some system expectation
        javaHome = os.environ['JAVA_HOME']
        if javaHome != None :
            javaHome = "%s/bin" % (javaHome)
        else :
            print 'FATAL : the JAVA_HOME environment variable has not been set'
            return
        print 'JAVA_HOME="%s' %( javaHome)    
        self._producerHome = '${DIRECTOR_ROOT_DIRECTORY}'  # <=== SUBSTITUTION HERE
        ### the test below is for local machine development testing
        if self._producerHome[0] == '$' : # <= not changed assume standalone launch
             # put your DVP TEST path    
            self._producerHome = _DEVELOPMENT_PRODUCER_HOME_PATH_   
        os.environ['PRODUCER_HOME'] = self._producerHome
        # CAVEAT  CAVEAT  CAVEAT  CAVEAT  CAVEAT  CAVEAT  CAVEAT  CAVEAT  CAVEAT    
        # CAVEAT : ${DIRECTOR_ROOT_DIRECTORY} IS SUBSTITUTED BY SETUP PROCESS 
        #          with the producer server home directory
        #
        print 'PRODUCER_HOME="%s' %( self._producerHome)
        if not self._sanityCheck() : # directory checking
            return                           
        #     
        if self._svcName == 'mon':
            producerjavastarter.monitoringDaemon(self._producerHome, javaHome, self._javalibPath, self._producerConfPath , myAction ) 
            pass
        elif self._svcName == 'allmon':
            producerjavastarter.monitoringDaemon(self._producerHome, javaHome, self._javalibPath, self._producerConfPath , myAction , all=True) 
            pass
        elif self._svcName == 'psrv':
            producerjavastarter.producerService(self._producerHome, javaHome, self._javalibPath, self._producerConfPath , myAction , all=True) 
            pass
        elif self._svcName == 'jjd' :
            producerjavastarter.jjdDaemon(self._producerHome, javaHome, self._javalibPath, self._jjdConfPath , myAction ) 
            pass
        elif self._svcName == 'smd' :
            producerjavastarter.smdDaemon(self._producerHome, javaHome, self._javalibPath, self._producerConfPath, self._smdPort , myAction ) 
            pass
        elif self._svcName == 'traps' :
            producerjavastarter.trapDaemon(self._producerHome, javaHome, self._javalibPath, self._producerConfPath , myAction ) 
            pass
        elif self._svcName == 'jjcstarter' :
            producerjavastarter.jjcstarter( self._producerHome, javaHome, self._javalibPath, self._producerConfPath , myAction ) 
            pass
        elif self._svcName == 'smdjmx' :
            producerjavastarter.smdDaemon(self._producerHome, javaHome, self._javalibPath, self._producerConfPath, self._smdPort , myAction , jmx=True) 
            pass
        elif self._svcName == 'monjmx':
            producerjavastarter.monitoringDaemon(self._producerHome, javaHome, self._javalibPath, self._producerConfPath , myAction, jmx=True ) 
            pass
        elif self._svcName == 'allmonjmx':
            producerjavastarter.monitoringDaemon(self._producerHome, javaHome, self._javalibPath, self._producerConfPath , myAction , all=True, jmx=True) 
            pass
        elif self._svcName == 'jjdjmx' :
            producerjavastarter.jjdDaemon(self._producerHome, javaHome, self._javalibPath, self._jjdConfPath , myAction, jmx=True ) 
            pass
        elif self._svcName == 'trapsjmx' :
            producerjavastarter.trapDaemon(self._producerHome, javaHome, self._javalibPath, self._producerConfPath , myAction, jmx=True ) 
            pass
        elif self._svcName == 'encrypt' :
            producerjavastarter.encrypt(javaHome, self._javalibPath, self._producerConfPath  ) 
            pass
        elif self._svcName == 'jesentryupdate' :
            producerjavastarter.jesentryupdate(self._producerHome, javaHome, self._javalibPath, self._producerConfPath  ) 
            pass
        elif self._svcName == 'jjcstarterjmx' :
            producerjavastarter.jjcstarter( self._producerHome, javaHome, self._javalibPath, self._producerConfPath, myAction, jmx=True ) 
            pass
        elif self._svcName == 'dlauncher' :
            producerjavastarter.dlauncher( self._producerHome, javaHome, self._javalibPath, self._producerConfPath, myAction, jmx=True ) 
            pass

if __name__ == '__main__':
    print "Welcome to Producer Service Daemon python starter Version : %s " %(_VERSION_)
    starter = ProducerServiceStarter()
    if starter.hasInited :
        starter.launch()
