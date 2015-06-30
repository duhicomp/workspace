#
# Python client class to start Workflow SMD service
#
__revision__ = '$Revision: 1.12 $'
__date__ ='$Date: 2012-11-19 09:44:30 $'


from JsonEnginesJsApi import JsonEnginesJsApi
from HttpConnector import AjaxClientError
from Connector import Connector
import json

def checkArgs( pos , defaultValue ):
    import sys
    if pos < len(sys.argv) :
        return sys.argv[pos]
    else :
        return defaultValue

class CompatibilityMode_702 :
    """Use this class for old 702 Stubs compatibility only """
    FETCH_ALL = -1 # get all results in one call (USE CAUTIOUSLY)
    
    CLASSFACTORY         = "com.sefas.workflowservice.WorkflowFactory"
    
    METHOD_INIT_CONTEXT = "initContext"
    METHOD_TERMINATE_CONTEXT = "terminateContext"
    METHOD_START_WORKFLOW = "startWorkflow"
    METHOD_STOP_WORKFLOW = "stopWorkflow"
    METHOD_KILL_WORKFLOW = "killWorkflow"
    METHOD_CLEAN_JOB_TICKET_MONITORING = "cleanJobTicketMonitoring"
    METHOD_WAIT_WORKFLOW_END = "waitWorkflowEnd"
    ARGS = "args"


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
        """ connect to Smd Service """
        if (self._connection == None):
            self._connection = Connector(self._host , self._port , self._encoding, CompatibilityMode_702.CLASSFACTORY)
        return self._connection

    def disconnect(self):
        """ Disconnect from Smd Service """
        if (self._connection != None):
            self._connection.close() 
            self._connection = None
        return

    def initContext (self, workflowName):
        """ execute the command on the smd server """
        self._connection.marshall(Connector.SET_METHOD, CompatibilityMode_702.METHOD_INIT_CONTEXT)
        # populate parameters
        self._connection.marshall(Connector.DEF_STRING, CompatibilityMode_702.ARGS)
        self._connection.marshall(Connector.SET_VALUE, CompatibilityMode_702.ARGS, workflowName)
        # proceed with call
        # return a workflow loader context id
        return self._connection.unmarshall(self._connection.marshall(Connector.CALL))

    def terminateContext (self, workflowContextId):
        """ execute the command on the smd server """
        self._connection.marshall(Connector.SET_METHOD, CompatibilityMode_702.METHOD_TERMINATE_CONTEXT)
        # populate parameters
        self._connection.marshall(Connector.DEF_STRING, CompatibilityMode_702.ARGS)
        self._connection.marshall(Connector.SET_VALUE, CompatibilityMode_702.ARGS, workflowContextId)
        # proceed with call
        self._connection.marshall(Connector.CALL)

    def startWorkFlow (self, workflowContextId, xpdl, jobTicketData):
        """ execute the command on the smd server """
        self._connection.marshall(Connector.SET_METHOD, CompatibilityMode_702.METHOD_START_WORKFLOW)
        # populate parameters
        self._connection.marshall(Connector.DEF_STRING, CompatibilityMode_702.ARGS)
        self._connection.marshall(Connector.SET_VALUE, CompatibilityMode_702.ARGS, workflowContextId)
        # populate parameters
        self._connection.marshall(Connector.DEF_STRING, CompatibilityMode_702.ARGS)
        self._connection.marshall(Connector.SET_VALUE, CompatibilityMode_702.ARGS, xpdl)
        # populate parameters
        if jobTicketData != None:
            self._connection.marshall(Connector.DEF_STRING, CompatibilityMode_702.ARGS)
            self._connection.marshall(Connector.SET_VALUE, CompatibilityMode_702.ARGS, jobTicketData)
        # proceed with call
        # return a workflow running context id
        return self._connection.unmarshall(self._connection.marshall(Connector.CALL))

    def cleanJobTicketMonitoring (self, jobTicketId):
        """ execute the command on the smd server """
        self._connection.marshall(Connector.SET_METHOD, CompatibilityMode_702.METHOD_CLEAN_JOB_TICKET_MONITORING)
        if jobTicketId != None:
            self._connection.marshall(Connector.DEF_STRING, CompatibilityMode_702.ARGS)
            self._connection.marshall(Connector.SET_VALUE, CompatibilityMode_702.ARGS, jobTicketId)
        # proceed with call
        # return a workflow running context id
        return self._connection.unmarshall(self._connection.marshall(Connector.CALL))
        

    def stopWorkFlow (self, workflowContextId):
        """ execute the command on the smd server """
        self._connection.marshall(Connector.SET_METHOD, CompatibilityMode_702.METHOD_STOP_WORKFLOW)
        # populate parameters
        self._connection.marshall(Connector.DEF_STRING, CompatibilityMode_702.ARGS)
        self._connection.marshall(Connector.SET_VALUE, CompatibilityMode_702.ARGS, workflowContextId)
        # populate parameters
        # proceed with call
        # return a workflow running context id
        return self._connection.unmarshall(self._connection.marshall(Connector.CALL))

    def killWorkFlow (self, workflowContextId):
        """ execute the command on the smd server """
        self._connection.marshall(Connector.SET_METHOD, CompatibilityMode_702.METHOD_KILL_WORKFLOW)
        # populate parameters
        self._connection.marshall(Connector.DEF_STRING, CompatibilityMode_702.ARGS)
        self._connection.marshall(Connector.SET_VALUE, CompatibilityMode_702.ARGS, workflowContextId)
        # populate parameters
        # proceed with call
        # return a workflow running context id
        return self._connection.unmarshall(self._connection.marshall(Connector.CALL))

    def waitWorkFlowEnd (self, workflowRunningContextId, timeOut=50000):
        """ execute the command on the smd server """
        self._connection.marshall(Connector.SET_METHOD, CompatibilityMode_702.METHOD_WAIT_WORKFLOW_END)
        # populate parameters
        self._connection.marshall(Connector.DEF_STRING, CompatibilityMode_702.ARGS)
        self._connection.marshall(Connector.SET_VALUE, CompatibilityMode_702.ARGS, workflowRunningContextId)
        # populate parameters
        self._connection.marshall(Connector.DEF_STRING, CompatibilityMode_702.ARGS)
        self._connection.marshall(Connector.SET_VALUE, CompatibilityMode_702.ARGS, timeOut)
        # proceed with call
        return self._connection.marshall(Connector.CALL)


class Smd_703(CompatibilityMode_702 ) :
  
    METHOD_ALLOCATE_MESSAGEHANDLER = "allocateMessageHandler"
    METHOD_FREE_MESSAGEHANDLER = "freeMessageHandler"
    METHOD_GETJOBTICKETEVENTS = "getJobTicketEvents"
    ENDOFTRANSMISSION = "eot"
    EVENT = "event"

    ABENDED = 3
  
    """
    703 SMD EXTENSIONS to support same API as HTTP connection through SMD  
    """
    def __init__ (self , 
                   encoding="UTF8" , # default encoding to UTF8
                   hostName="localhost" , 
                   port=29100 
                 ):
        """ constructor just store provided object information """
        CompatibilityMode_702.__init__(self, encoding, hostName, port)    

    def startWorkFlow(self, workflowSession,workflowContextId, xpdl, jobTicketData):
        return CompatibilityMode_702.startWorkFlow(self,workflowContextId, xpdl, jobTicketData)
        
    def allocateMessageHandler(self , unused , jobTicket ) :
        self._connection.marshall(Connector.SET_METHOD, self.METHOD_ALLOCATE_MESSAGEHANDLER)
        # populate parameters
        self._connection.marshall(Connector.DEF_STRING, CompatibilityMode_702.ARGS)
        self._connection.marshall(Connector.SET_VALUE, CompatibilityMode_702.ARGS, jobTicket)
        # proceed with call
        return self._connection.unmarshall(self._connection.marshall(Connector.CALL))
    

    def getJobticketEvents(self , unused , handler , timeout ) :
        """ execute the command on the smd server """
        self._connection.marshall(Connector.SET_METHOD, self.METHOD_GETJOBTICKETEVENTS)
        # populate parameters
        self._connection.marshall(Connector.DEF_INTEGER, CompatibilityMode_702.ARGS)
        self._connection.marshall(Connector.SET_VALUE, CompatibilityMode_702.ARGS, handler)
        # populate parameters
        self._connection.marshall(Connector.DEF_INTEGER, CompatibilityMode_702.ARGS)
        self._connection.marshall(Connector.SET_VALUE, CompatibilityMode_702.ARGS, timeout)
        # proceed with call
        returned = self._connection.unmarshall(self._connection.marshall(Connector.CALL))
        # print returned ;
        return json.loads(returned)

    def isSmdOverStressed(self , msg ) :
        """ execute the command on the smd server """
        self._connection.marshall(Connector.SET_METHOD, self.METHOD_ISSMDOVERSTRESSED)
        # proceed with call
        return self._connection.unmarshall(self._connection.marshall(Connector.CALL))

    def freeMessageHandler(self , unused , msgHandler ) :
        self._connection.marshall(Connector.SET_METHOD, self.METHOD_FREE_MESSAGEHANDLER)
        # populate parameters
        self._connection.marshall(Connector.DEF_INTEGER, CompatibilityMode_702.ARGS)
        self._connection.marshall(Connector.SET_VALUE, CompatibilityMode_702.ARGS, msgHandler)
        # proceed with call
        self._connection.marshall(Connector.CALL)

    def hasWorkflowEnded(self , msg ):
        if msg != None :
            if msg.get(self.ENDOFTRANSMISSION) == None :
                return False
            else :
                return True
        return False

    def isErrorMessage(self , msg ):
        if msg.get(self.EVENT) == self.ABENDED :
            return True
        return False

    def initWorkflowSession(self,workflowSession) :
        self._connection= self.connect()
        return self._connection

    def stopWorkFlow (self, workflowSession,workflowContextId):
        return CompatibilityMode_702.stopWorkflow(self, workflowContextId)

    def killWorkFlow (self, workflowSession,workflowContextId):
        return CompatibilityMode_702.killWorkFlow(self,workflowContextId)

    def listJobTickets (self, workflowSession,workflowContextId):
        return CompatibilityMode_702.listJobTickets(self,workflowContextId)
    
    def terminateWorkflowContext(self,workflowSession , workflowContextId):
        return CompatibilityMode_702.terminateContext(self,workflowContextId)
    
    def cleanJobTicketMonitoring(self,workflowSession , workflowContextId):
        return CompatibilityMode_702.cleanJobTicketMonitoring(self,workflowContextId)

    def terminateWorkflowSession(self,workflowSession) :
        return CompatibilityMode_702.disconnect(self)

class WorkflowUtils:
    """
    Python Client interface to the Workflow AJAX API service 
    STARTING WITH 7.0.3 this API MUST BE THE PREFFERED ONE
    """

    def __init__ (self ,
                   encoding="UTF8" , # default encoding to UTF8
                   hostName="localhost" ,
                   smdPort=39900 ,
                   httpPort=None,
                   mode=False):
        """ constructor just store provided object information """
        self._host = hostName
        self._encoding = encoding
        self._smdPort=smdPort
        self._httpPort=None
        if httpPort != None : # through http
          self._api = JsonEnginesJsApi("%s:%s" % (hostName,str(httpPort)))
        self._smdUrl = "smd://%s:%s" % (hostName,str(smdPort))
        self._workflowSession = None
        self._msgHandler = None
        self._compatConnector = None
        self._702mode=mode
        self._hasWorkflowEnded=False
        if ( httpPort == None ) :
          # Initialize 702 COMPATIBILITY MODE
          print "WARNING : stub is running in SMD direct connection mode"
          self._compatConnector = Smd_703(encoding,hostName,smdPort)
          self._api = self._compatConnector 

    def connect(self) :
        """ connect to API Service """
        if self._702mode == True :
          self._compatConnector.connect()
        else :
          if (self._workflowSession != None):
            return
          self._workflowSession = self._api.initWorkflowSession(self._smdUrl)

    def disconnect(self):
        """ Disconnect from WORKFLOW API Service """
        if self._702mode == True :
          self._compatConnector.disconnect() 
        else :   
          if (self._workflowSession != None):
            self._api.terminateWorkflowSession(self._workflowSession)
            self._workflowSession = None

    def initContext (self , context=None ):
        """ Old deprecated API maintained for compatibility 
            (context is unused but may be provided to comply with 7.0.2 API
        """
        if self._702mode == True :
          return self._compatConnector.initContext(context)
        else :
          if (self._workflowSession != None):
             return self._api.initContext(self._workflowSession)

    def terminateContext(self, workflowContextId , myJobTicket = None ):
        """ execute the command on the smd server """
        if self._702mode == True :
          self._compatConnector.terminateContext(workflowContextId)
          if ( myJobTicket != None ):
            self._compatConnector.cleanJobTicketMonitoring(myJobTicket)
        else :  
          if (self._workflowSession != None and workflowContextId != None ):
            self._api.terminateWorkflowContext(self._workflowSession , workflowContextId)
          if (self._workflowSession != None and myJobTicket != None ):
            # avoid memory leaks by cleaning memory jobticket stats    
            self._api.cleanJobTicketMonitoring(self._workflowSession, myJobTicket)
        return

    def listWorkFlowXpdls(self, workflowContextId):
        """ list available public xpdls on server side """
        if (self._workflowSession != None and workflowContextId != None ):
            return self._api.listXpdls(self._workflowSession, workflowContextId)

    def startWorkFlow(self, workflowContextId, xpdl, jobTicketData):
        """ execute the command through standard API """
        if self._702mode == True :
          return self._compatConnector.startWorkFlow(workflowContextId, xpdl, jobTicketData)
        else :  
          if (self._workflowSession != None and workflowContextId != None ):
            return self._api.startWorkFlow(self._workflowSession, workflowContextId, xpdl, jobTicketData)

    def stopWorkFlow (self, workflowContextId):
        """ execute the command through standard API """
        if self._702mode == True :
          return self._compatConnector.stopWorkFlow(workflowContextId)
        else :  
          if (self._workflowSession != None and workflowContextId != None ):
            return self._api.stopWorkflow(self._workflowSession, workflowContextId)

    def killWorkFlow (self, workflowContextId):
        """ execute the command through standard API """
        if self._702mode == True :
          return self._compatConnector.killWorkFlow(workflowContextId)
        else :  
          if (self._workflowSession != None and workflowContextId != None ):
            return self._api.killWorkFlow(self._workflowSession, workflowContextId)

    def listJobTickets (self, workflowContextId):
        """ list running jobtickets ('*' in workflowCoontextId will look at all contexts) """
        if (self._workflowSession != None and workflowContextId != None ):
            return self._api.listJobTickets(self._workflowSession, workflowContextId)

    def waitForWorkflowEvent(self , jobTicket ):
        if ( self._msgHandler == None ) :
            # proceed with allocation
            self._msgHandler = self._api.allocateMessageHandler(self._workflowSession, jobTicket)
            print "handler : %s"  %   (self._msgHandler)
        return self._api.getJobticketEvents(self._workflowSession,self._msgHandler,500)

    def hasWorkflowEnded(self , msg ) :
        if (self._hasWorkflowEnded== False) :
           self._hasWorkflowEnded=self._api.hasWorkflowEnded(msg)
           if  (self._hasWorkflowEnded ==True) :
               # cleanup MshHandler
               self._api.freeMessageHandler(self._workflowSession, self._msgHandler)
               self._msgHandler = None
        return self._hasWorkflowEnded

    def waitWorkFlowEnd ( self , workflowRunningContextId, timeOut=-1 ) :
      """ OLD 7.0.2 compatibility API maintained for compatibility purposes """
      if self._702mode == True :
          return self._compatConnector.waitWorkFlowEnd(workflowRunningContextId,timeOut)
      else :
        msg = self.waitForWorkflowEvent(workflowRunningContextId)
        retCode = "<OK>0</OK>" 
        while (not self.hasWorkflowEnded(msg)) :
          if ( msg.get("activityID") != None) :
          # ignore all non activity messages
            if self.isWorkflowActivityInError(msg) :
               print " Workflow activity %s SEVERE PROBLEM =%s" % (msg["activityID"],msg["message"])
               retCode = "<KO>-1</KO>"
            else :
               print " Workflow activity %s : %s" % (msg["activityID"],msg["message"])
          try:
            msg = self.waitForWorkflowEvent(workflowRunningContextId)
          except Exception as e :
            print "error when trying to get a msg " + str(e)
            msg = self.waitForWorkflowEvent(workflowRunningContextId)
        # avoid memory leaks by cleaning memory jobticket volatile tracker    
        self._api.cleanJobTicketMonitoring(self._workflowSession, workflowRunningContextId)
        return retCode   

    def waitForWorkFlowEnd ( self , workflowRunningContextId, timeOut=-1 ) :
      """ OLD 7.0.2 compatibility API maintained for compatibility purposes """
      if self._702mode == True :
          return self._compatConnector.waitWorkFlowEnd(workflowRunningContextId,timeOut)
      else :
        msg = self.waitForWorkflowEvent(workflowRunningContextId)
        retCode = 0
        while (not self.hasWorkflowEnded(msg)) :
          if ( msg.get("activityID") != None) :
          # ignore all non activity messages
            if self.isWorkflowActivityInError(msg) :
               print " Workflow activity %s SEVERE PROBLEM =%s" % (msg["activityID"],msg["message"])
               retCode = -1
            else :
               print " Workflow activity %s : %s" % (msg["activityID"],msg["message"])
          msg = self.waitForWorkflowEvent(workflowRunningContextId)
        # avoid memory leaks by cleaning memory jobticket volatile tracker    
        self._api.cleanJobTicketMonitoring(self._workflowSession, workflowRunningContextId)
        return retCode   

    def isWorkflowActivityInError(self , msg):
        return self._api.isErrorMessage(msg)

    def isSmdOverStressed(self , msg):
        return self._api.isSmdOverStressed(msg)

 #   def getSessionContextDirectory (self, workflowRunningContextId):
 #       """ execute the command on the smd server """
 #       self._connection.marshall(Connector.SET_METHOD, WorkflowUtils.METHOD_GET_SESSION_CONTEXT_DIR)
 #       # populate parameters
 #       self._connection.marshall(Connector.DEF_STRING, WorkflowUtils.ARGS)
 ##       self._connection.marshall(Connector.SET_VALUE, WorkflowUtils.ARGS, workflowRunningContextId)
 #       # proceed with call
 #       return self._connection.marshall(Connector.CALL)

 #   def getWRFCTX (self, workflowRunningContextId):
 #       """ execute the command on the smd server """
 #       self._connection.marshall(Connector.SET_METHOD, WorkflowUtils.METHOD_GET_WRFCTX)
 #       # populate parameters
 #       self._connection.marshall(Connector.DEF_STRING, WorkflowUtils.ARGS)
 #       self._connection.marshall(Connector.SET_VALUE, WorkflowUtils.ARGS, workflowRunningContextId)
 #       # proceed with call
 #       return self._connection.marshall(Connector.CALL)
#
# module main is just a practical sample test
#
if __name__ == '__main__':
    myencoding = "UTF-8"
    host = checkArgs(1,'jymen-newbook')
    httpPort = int(checkArgs(2,'9080'))
    smdPort = int(checkArgs(3,'39900'))

    xpdlFile = "/home/jymen/Downloads/minimaltimer.xpdl"
    xpdlFile = "/home/jymen/Downloads/threerunatsametime.xpdl"
    jobTicketDataFile = None

    myclient = WorkflowUtils(myencoding, host , smdPort )
    try :
        myclient.connect()
        workflowContextId = myclient.initContext()
        print "Worflow Context ID = %s" % (workflowContextId)
        workflowRunningContextId = myclient.startWorkFlow(workflowContextId,xpdlFile,jobTicketDataFile)
        print "Worflow Running Context ID = %s" % (workflowContextId)
        msg = myclient.waitForWorkflowEvent(workflowRunningContextId)
        retCode = 0
        while not myclient.hasWorkflowEnded(msg) :
            if ( msg.get("activityID") != None) :
                # ignore all non activity messages
                if myclient.isWorkflowActivityInError(msg) :
                    print " Workflow activity %s SEVERE PROBLEM =%s" % (msg["activityID"],msg["message"])
                    retCode = -1
                else :
                    print " Workflow activity %s (%s) : %s" % (msg["activityID"], msg["description"] , msg["message"])
            msg = myclient.waitForWorkflowEvent(workflowRunningContextId)
        print "Worflow Run Ended retCode=%i" % (retCode)
        myclient.terminateContext(workflowContextId,workflowRunningContextId)
        myclient.disconnect()


    except AjaxClientError , e :
        print "service instanciation error : " , str(e)