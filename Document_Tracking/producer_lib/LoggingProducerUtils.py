#!/opt/vgi/openprint/python2.4/bin/python

###!/opt/sefas/product/openprint/python2.4/bin/python

import datetime
import os,sys
import traceback
import log4py
from log4py import Logger

PARAM_DIR="-DIR"
# FOR REMOTE SERVER (Ex. VNG PRISMA INT
PARAM_DIRORA="-DIRORA"
TMP_DIR="-TMP"
PRINTER_TYPE="-PRINTER_TYPE"
PRINTER_NAME="-NAME"
LOGGER_JOBS_DIR="JOBS"
LOGGER_PRODUCER_LOG_DIR="PRODUCER_LOG"
FMT_SEFAS="%T %L %x%M"
LOG_DIRECTORY=os.environ.get('LOG_DIRECTORY', '.')

"""
    PRODUCER Logging Utilities For Scripts is a class to manage the le logging of the scripts
"""
class LoggingProducerUtils:
    
    def __init__(self,parameterContainer, logLevel=log4py.LOGLEVEL_DEBUG, logTarget=LOGGER_PRODUCER_LOG_DIR):
        
        if parameterContainer.getParamValue(PRINTER_TYPE) is not None:
            self.__errorFileName = "%s" % (parameterContainer.getErrorFileName())
            self.__logFileName = "%s/%s-%s.log" % (parameterContainer.getParamValue(TMP_DIR),parameterContainer.getParamValue(PRINTER_TYPE), parameterContainer.getParamValue(PRINTER_NAME))
        else:
            if parameterContainer.getParamValue(PARAM_DIR) is not None:
                if os.access(parameterContainer.getFullPathJobDir(), os.W_OK) :
                    # Error/Log directory locally
                    self.__errorFileName = "%s/%s" % (parameterContainer.getFullPathJobDir(), parameterContainer.getErrorFileName())
                    self.__logFileName = "%s/%s.log" % (parameterContainer.getFullPathJobDir(), parameterContainer.getJobID())
                else:
                    # Error/Log directory remotely
                    self.__errorFileName = "%s/%s" % (parameterContainer.getInputDir(), parameterContainer.getErrorFileName())
                    self.__logFileName = "%s/%s.log" % (parameterContainer.getInputDir(), parameterContainer.getJobID())
            else:
                self.__errorFileName = "%s/%s" % (LOG_DIRECTORY, parameterContainer.getErrorFileName())
                self.__logFileName = "%s/%s.log" % (LOG_DIRECTORY, parameterContainer.getJobID())
        
        ### LOG4PY ###
        self._log4py = Logger().get_instance(self)
        self._jobid = parameterContainer.getJobID()
        
        # Set target(s) according to configuration
        if logTarget == LOGGER_JOBS_DIR and self.__logFileName is not None:
            self.__log4pyFile = self.__logFileName
        else:
            # Log to the producer log directory using the OsEnv variable from producerjavastarter.py
            #self.__log4pyFile = '/prod_data/sefas/data/traffic/log/producer_log4py_' + self.getLogFileTimestamp() +'.log'
            self.__log4pyFile = LOG_DIRECTORY+'/producer_log4py_' + self.getLogFileTimestamp() +'.log'
            
        self._log4py.set_target(self.__log4pyFile)
        
        # Set time format
        timeformat = "%Y-%m-%d %H:%M:%S "
        self._log4py.set_time_format(timeformat)
        # Set log format
        self._log4py.set_formatstring(FMT_SEFAS)
        # Set level from configuration file?
        self._log4py.set_loglevel(logLevel)
        # Set rotation
        self._log4py.set_rotation(log4py.ROTATE_DAILY)
        ### END LOG4PY ###
    
    def getLogFileTimestamp(self):
        t = datetime.datetime.now();
        return t.strftime("%Y%m%d")
    
    # Wrap the log4py methods  
    def info(self, msg):
        if self._jobid is not None:
            self._log4py.info("[JOB_ID=" + self._jobid + "] %s" % msg)
        else:
            self._log4py.info("[NO JOB_ID] %s" % msg)
        
    def error(self, msg, exceptionType=None, exceptionValue=None):
        self._log4py.set_target(self.__errorFileName)
        if self._jobid is not None:
            self._log4py.error("[JOB_ID=" + self._jobid +  "] %s" % msg)
        else:
            self._log4py.error("[NO JOB_ID] %s" % msg)
        if exceptionType != None and exceptionValue != None:
            type, values, tb = sys.exc_info()
            traceback.print_exception(exceptionType, exceptionValue, tb)
            if self._jobid is not None:
                self._log4py.error("[JOB_ID=" + self._jobid + "] %s" % tb)
            else:
                self._log4py.error("[NO JOB_ID] %s" % tb)
        
        # Finally write to regular log
        self._log4py.set_target(self.__log4pyFile)
        self._log4py.error(msg)
        
    def debug(self, msg):
        if self._jobid is not None:
            self._log4py.debug("[JOB_ID=" + self._jobid + "] %s" % msg)
        else:
            self._log4py.debug("[NO JOB_ID] %s" % msg)
        
    def warn(self, msg):
        if self._jobid is not None:
            self._log4py.warn("[JOB_ID=" + self._jobid + "] %s" % msg)
        else:
            self._log4py.warn("[NO JOB_ID=] %s" % msg)
        
    def getFormatString(self):
        self._log4py.get_formatstring()
        
    def setFormatString(self, format):
        self._log4py.set_formatstring(format)
        
    # Wrap the loglevel and target
    def setLogLevel(self, level):
        self._log4py.set_loglevel(level)
        
    def setLogTarget(self, target):
        self._log4py.set_target(target)
    
    # Deprecated?
    def getLogTime(self):
        t = datetime.datetime.now();
        return t.strftime("%Y-%m-%d %H:%M:%S ")
    
    def err(self, msg, exceptionType=None, exceptionValue=None):
        # do print before write in log (if file does not exist the message is dispayed)
        print "%s%s"%(self.getLogTime(),msg)
        f = open(self.__errorFileName,"a")
        f.writelines("%s%s\n"%(self.getLogTime(),msg))
        if exceptionType != None and exceptionValue != None:
            type, value, tb = sys.exc_info()
            traceback.print_exception(exceptionType, exceptionValue, tb)
            traceback.print_exception(exceptionType, exceptionValue, tb, None, f)
        f.close()
        self.log(msg)
    # Deprecated?
    def log(self, msg):
        f = open(self.__logFileName,"a")
        f.writelines("%s%s\n"%(self.getLogTime(),msg))
        f.close()
