#!/usr/bin/env python
import producerjavastarter 
import sys 
import os

_VERSION_ = "1.00.000"

_SERVICES_ = { \
               'jjd'  :'Java Jes Daemon Producer Service' , \
               'mon'  :'Java Producer Monitoring Service minimal' , \
               'allmon'  :'Java Producer Monitoring Service FULL' , \
               'psrv'  :'Java Producer Service' , \
               'smd'  :'Java Smd Service JRE 1.4' , \
               'traps':'Java SNMP traps service' , \
               'jjcstarter':'Java JES Client stored proc starter'
            }
_STATUS_ = '-status'
_LSTATUS_ = '-lstatus'
_DEBUG_ = '-debug'
_KILL_ = '-kill'
_LOG4J_ = 'Log4J.properties'

#
# Developpers : PLEASE USE THE TWO CONSTANT BELOW TO SETUP YOUR PRODUCER DIRECTORIES 
#               AT DEVELOPMENT TIME ; this two variable are not use in production
#
_DEVELOPMENT_PRODUCER_HOME_PATH_ = 'D:\\producercurrentinstallation\\SetUP_producer_1_0_Beta3_Build4\\setup\\installer\\producer-scripts-build\\producer'
_DEVELOPMENT_PRODUCER_JAVALIB_PATH_ = 'D:\\producercurrentinstallation\\SetUP_producer_1_0_Beta3_Build4\\setup\\installer\\lib'

class ProducerStatusStarter :
    """ 
      this class usage is starting all kind of producer status
      (Jjd , MonitoringServices ....) using the semantics defined inside
      producerjavastarter module and the simplest possible syntax
      pdcstatus daemonname [-status | -lstatus ]
    """

    def __init__( self ) : 
        self.hasInited = False
        if len( sys.argv ) < 2 :
            print "missing argument requested service name expected : %s " % (str(_SERVICES_.keys()))
        else :
            self._svcName = sys.argv[1].lower()
            if len( sys.argv ) > 2  :
                self._action  = sys.argv[2]
                if self._action != '-status' and self._action != '-lstatus' and self._action != '-debug' and self._action != '-kill' :
                    print 'ERROR : %s is invalid : -status, -lstatus, -kill or -debug expected' % (self._action)
            else :
                self._action = '-status'
                print 'WARNING : no action specified => assuming -status'

            try :
                description = _SERVICES_ [self._svcName]
                print 'Service = %s' % (description) 
                self._conf    = None 
                self._javalibPath = None
                self._producerHome = None
                self._producerConfPath = None
                self._jjdConfPath = None
                self._logdir = '${LOG_DIRECTORY}'
                if self._logdir[0] != '$' :
                    os.environ['LOG4J'] = '%s/%s' %(self._logdir,_LOG4J_)
                self._smdHost = 'localhost'
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
        if self._action == _LSTATUS_ :
            myAction = producerjavastarter.LSTATUS
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
        #print 'JAVA_HOME="%s' %( javaHome)    
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
        #print 'PRODUCER_HOME="%s' %( self._producerHome)
        if not self._sanityCheck() : # directory checking
            return                           
        #     
        if self._svcName == 'jjd' :
            producerjavastarter.jjdStatus(self._producerHome, javaHome, self._javalibPath, self._jjdConfPath , myAction )
            pass
        elif self._svcName == 'smd' :
            producerjavastarter.smdStatus(self._producerHome, javaHome, self._javalibPath, self._smdHost, self._smdPort , myAction )
            pass
        else :
            if self._svcName == 'allmon' :
                producerjavastarter.producerStatus(self._producerHome, javaHome, self._javalibPath, self._producerConfPath, 'pmon', myAction)
                pass
            elif self._svcName == 'jjcstarter' :
                producerjavastarter.producerStatus(self._producerHome, javaHome, self._javalibPath, self._producerConfPath, 'jjc', myAction)
                pass
            else :
                producerjavastarter.producerStatus(self._producerHome, javaHome, self._javalibPath, self._producerConfPath, self._svcName, myAction)
                pass

if __name__ == '__main__':
    print "Producer Status version : %s " %(_VERSION_)
    starter = ProducerStatusStarter()
    if starter.hasInited :
        starter.launch()
