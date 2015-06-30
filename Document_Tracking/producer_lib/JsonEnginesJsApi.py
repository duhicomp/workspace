'''
Created on Feb 2, 2011

@author: jymen
'''
from HttpConnector import HttpConnector , AjaxClientError

_JSON_SERVLET_ = "/sefasajax/jsonapi"

_FUNCTION_ = 'fx'
_GETVERSION_ = 'GetVersion'
_WORKFLOW_INITSESSION_ = "initWorkflowSession"
_WORKFLOW_TERMINATESESSION_ = "terminateWorkflowSession"
_WORKFLOW_INITCONTEXT_ = "initWorkflowContext"
_WORKFLOW_STARTWORKFLOW_ = "startWorkflow"
_WORKFLOW_STOPWORKFLOW_ = "stopWorkflow"
_WORKFLOW_KILLWORKFLOW_ = "killWorkflow"
_WORKFLOW_LISTXPDLS_ = "listXpdls"
_WORKFLOW_TERMINATECONTEXT_ = "terminateWorkflowContext"
_WORKFLOW_LISTJOBTICKETDATAS_ = "listJobticketDatas"
_WORKFLOW_GETXPDLSOURCE_ = "getXpdlSource"
_WORKFLOW_SCANOPWDWORKFLOW_ = "scanOpwdWorkflow"
_WORKFLOW_GETFULLPATHFILE_ = "getFullPathFile"
_WORKFLOW_EXISTSFILEONSERVER_ = "existsFileOnServer"
_WORKFLOW_EXISTSOPWDONSERVER_ = "existsOpwdOnServer"
_WORKFLOW_GETSERVERSIDEFILTER_ = "getServerSideFilter"
_WORKFLOW_LOADUSERCONTEXT_ = "loadUserContext"
_WORKFLOW_STOREUSERCONTEXT_ = "storeUserContext"
_WORKFLOW_ALLOCATEMESSAGEHANDLER_ = "allocateMessageHandler"
_WORKFLOW_FREEMESSAGEHANDLER_ = "freeMessageHandler"
_WORKFLOW_GETJOBTICKETEVENTS_ = "getJobticketExecutionEvents"
_WORKFLOW_LISTJOBTICKETS_ = "listJobtickets"
_WORKFLOW_LISTJOBTICKETS_ = "listJobtickets"
_WORKFLOW_CLEANJOBTICKETMONITORING_ = "cleanJobticketMonitoring" 

VERSION = 'version'
ERROR = 'error'
SMDURI = "smdUri"
WORKFLOWSESSION = "workflowSession"
WORKFLOWCONTEXT = "workflowContext"
XPDLS = "xpdls"
JOBTICKETS = "jobtickets"
JOBTICKET = "jobticket"
XPDL = "xpdl"
JOBTICKETDATA = "jobticketData"
MESSAGEHANDLER = "messageHandler"
TIMEOUT = "timeout"
ENDOFTRANSMISSION = "eot"
EVENT = "event"

ABENDED = 3



class _AJAX_CALL_(object):

    def __init__(self , url ) :
        self._in = {}
        self._url = url

    def _ajaxCall(self  ):
        connector = HttpConnector(self._url , _JSON_SERVLET_)
        returned = connector.ajaxCall(self._in)
        if ( returned.get('error') != None ) :
            raise AjaxClientError("Sefas Python Ajax failure :" + returned[ERROR])
        return returned


    def putArg(self , key , value ):
        if value != None :
            self._in[key] = value

    def call(self):
        return self._ajaxCall()

class JsonEnginesJsApi(object):

    def __init__(self , url):
        '''
        Constructor
        '''
        self._url = url

    def getVersion(self) :
        '''
        JSON getVersion call
        '''
        ajax = _AJAX_CALL_(self._url)
        ajax.putArg(_FUNCTION_, _GETVERSION_)
        returned = ajax.call()
        return returned[VERSION]

    def initWorkflowSession(self , uriSmd ):
        '''
        JSON Workflow session initer call
        '''
        ajax = _AJAX_CALL_(self._url)
        ajax.putArg(_FUNCTION_, _WORKFLOW_INITSESSION_)
        ajax.putArg(SMDURI, uriSmd)
        returned = ajax.call()
        return returned[WORKFLOWSESSION]


    def initWorkflowContext(self , sessionId ):
        '''
        JSON Workflow context initer call
        '''
        ajax = _AJAX_CALL_(self._url)
        ajax.putArg(_FUNCTION_, _WORKFLOW_INITCONTEXT_)
        ajax.putArg(WORKFLOWSESSION, sessionId)
        returned = ajax.call()
        return returned[WORKFLOWCONTEXT]


    def listXpdls(self , sessionId , contextId ):
        '''
        JSON Workflow list server side public xpdls
        '''
        ajax = _AJAX_CALL_(self._url)
        ajax.putArg(_FUNCTION_, _WORKFLOW_LISTXPDLS_)
        ajax.putArg(WORKFLOWSESSION, sessionId)
        ajax.putArg(WORKFLOWCONTEXT, contextId)
        returned = ajax.call()
        return returned[XPDLS]


    def listJobtickets(self , sessionId , contextId ):
        '''
        JSON Workflow start a workflow run
        '''
        ajax = _AJAX_CALL_(self._url)
        ajax.putArg(_FUNCTION_, _WORKFLOW_LISTJOBTICKETS_)
        ajax.putArg(WORKFLOWSESSION, sessionId)
        ajax.putArg(WORKFLOWCONTEXT, contextId)
        returned = ajax.call()
        return returned[JOBTICKETS]



    def startWorkflow(self , sessionId , contextId , myXpdl, myJobticketData ):
        '''
        JSON Workflow  start workflow on server side
        '''
        ajax = _AJAX_CALL_(self._url)
        ajax.putArg(_FUNCTION_, _WORKFLOW_STARTWORKFLOW_)
        ajax.putArg(WORKFLOWSESSION, sessionId)
        ajax.putArg(WORKFLOWCONTEXT, contextId)
        ajax.putArg(XPDL, myXpdl)
        ajax.putArg(JOBTICKETDATA, myJobticketData)
        returned = ajax.call()
        return returned[JOBTICKET]

    def stopWorkflow(self , sessionId , contextId  ):
        '''
        JSON Workflow  start workflow on server side
        '''
        ajax = _AJAX_CALL_(self._url)
        ajax.putArg(_FUNCTION_, _WORKFLOW_STOPWORKFLOW_)
        ajax.putArg(WORKFLOWSESSION, sessionId)
        ajax.putArg(WORKFLOWCONTEXT, contextId)
        returned = ajax.call()
        return returned[JOBTICKET]

    def killWorkflow(self , sessionId , contextId  ):
        '''
        JSON Workflow  start workflow on server side
        '''
        ajax = _AJAX_CALL_(self._url)
        ajax.putArg(_FUNCTION_, _WORKFLOW_KILLWORKFLOW_)
        ajax.putArg(WORKFLOWSESSION, sessionId)
        ajax.putArg(WORKFLOWCONTEXT, contextId)
        returned = ajax.call()
        return returned[JOBTICKET]


    def allocateMessageHandler(self , sessionId , myJobticket ):
        '''
        JSON request a message handler for supervising provided jobticket
        '''
        ajax = _AJAX_CALL_(self._url)
        ajax.putArg(_FUNCTION_, _WORKFLOW_ALLOCATEMESSAGEHANDLER_)
        ajax.putArg(WORKFLOWSESSION, sessionId)
        ajax.putArg(JOBTICKET, myJobticket)
        returned = ajax.call()
        return returned[MESSAGEHANDLER]


    def getJobticketEvents (self , sessionId , myHandler , timeOut ):
        '''
        JSON receive running workflow event messages through this API
        '''
        ajax = _AJAX_CALL_(self._url)
        ajax.putArg(_FUNCTION_, _WORKFLOW_GETJOBTICKETEVENTS_)
        ajax.putArg(WORKFLOWSESSION, sessionId)
        ajax.putArg(MESSAGEHANDLER, myHandler)
        ajax.putArg(TIMEOUT, timeOut)
        returned = ajax.call()
        return returned # return the full message back


    def freeMessageHandler(self , sessionId , myHandler ):
        '''
        JSON request a message handler for supervising provided jobticket
        '''
        ajax = _AJAX_CALL_(self._url)
        ajax.putArg(_FUNCTION_, _WORKFLOW_FREEMESSAGEHANDLER_)
        ajax.putArg(WORKFLOWSESSION, sessionId)
        ajax.putArg(MESSAGEHANDLER, myHandler)
        ajax.call()



    def terminateWorkflowContext(self , sessionId , contextId ):
        '''
        JSON Workflow context termination call
        '''
        ajax = _AJAX_CALL_(self._url)
        ajax.putArg(_FUNCTION_, _WORKFLOW_TERMINATECONTEXT_)
        ajax.putArg(WORKFLOWSESSION, sessionId)
        ajax.putArg(WORKFLOWCONTEXT, contextId)
        ajax.call()


    def cleanJobTicketMonitoring(self , sessionId , myJobTicket ):
        '''
        JSON Workflow session monitoring call
        '''
        ajax = _AJAX_CALL_(self._url)
        ajax.putArg(_FUNCTION_, _WORKFLOW_CLEANJOBTICKETMONITORING_)
        ajax.putArg(WORKFLOWSESSION, sessionId)
        ajax.putArg(JOBTICKET, myJobTicket)
        ajax.call()

    def terminateWorkflowSession(self , sessionId ):
        '''
        JSON Workflow session termination call
        '''
        ajax = _AJAX_CALL_(self._url)
        ajax.putArg(_FUNCTION_, _WORKFLOW_TERMINATESESSION_)
        ajax.putArg(WORKFLOWSESSION, sessionId)
        ajax.call()

    def hasWorkflowEnded(self , msg ):
        if msg != None :
            if msg.get(ENDOFTRANSMISSION) == None :
                return False
            else :
                return True
        return False

    def isErrorMessage(self , msg ):
        if msg.get(EVENT) == ABENDED :
            return True
        return False

if __name__ == '__main__':
    print "Sample JSONAPI test "
    api = JsonEnginesJsApi("http://myubuntu:9080")
    # let's try a getVersion first
    print api.getVersion()
    # next let's allocate a workflow session
    workflowSession = api.initWorkflowSession("smd://myubuntu:39900")
    # then a context for workflow execution
    workflowContext = api.initWorkflowContext(workflowSession)

    availableXpdls = api.listXpdls(workflowSession, workflowContext)
    for xpdl in availableXpdls :
        print "public server xpdl :" + xpdl

    # start a workflow
    jobTicket = api.startWorkflow(workflowSession, workflowContext, "crashtest.xpdl", None)
    print "jobticket workflow %s started " % jobTicket

    # and then request supervision on it
    msgHandler = api.allocateMessageHandler(workflowSession, jobTicket)
    print "msgHandler %s allocated " % msgHandler

    msg = api.getJobticketEvents(workflowSession, msgHandler, 500 )
    print "msg= %s " % str(msg)
    while( not api.hasWorkflowEnded(msg) ) :
        #
        if ( msg.get("activityID") != None) :
            if ( api.isErrorMessage(msg) ) :
                print "ACTIVITY %s IN ERROR : %s" % (msg["activityID"],msg["message"])
            else :
                print " Workflow activity : %s MESSAGE=%s" % (msg["activityID"],msg["message"])
        else :
            print " MESSAGE=%s" % msg["message"]
        # next message
        msg = api.getJobticketEvents(workflowSession, msgHandler, 500 )
    print "jobticket workflow %s ended " % jobTicket
    api.cleanJobTicketMonitoring(workflowSession, jobTicket)
    api.freeMessageHandler(workflowSession, msgHandler)
    api.terminateWorkflowContext(workflowSession,workflowContext)

    # finally terminate the allocated Workflow session
    api.terminateWorkflowSession(workflowSession)

