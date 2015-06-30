import os
import DbIndexingClient

"""
    Producer document tracking integration library
    This library provide the function required to manage information on a database
    oriented for document tracking feature
    It use DbIndexingClient.DbIndexingClient to provide database command throw SMD
"""

FILE_TYPE_CSV=DbIndexingClient.FILE_TYPE_CSV
FILE_TYPE_VPF_IDX=DbIndexingClient.FILE_TYPE_VPF_IDX
FILE_TYPE_TSM_VPF_IDX=DbIndexingClient.FILE_TYPE_TSM_VPF_IDX

COLTYPE_STR = DbIndexingClient.COLTYPE_STR
COLTYPE_INT = DbIndexingClient.COLTYPE_INT

_MSG_DOC_TACK_NOT_ACTIVATED_ = 'Document tracking not activated.'
PADD_NOT_ACTIVE = 'notActivePadd'
PADD_ACTIVE = 'activePadd'

class DataStruct:
    def __init__(self, docTrack, isUpdateKey, dataType, inputValue, isConstant):
        self.__isUpdate = isUpdateKey
        self.__dataType = dataType
        self.__previousInputValue = None
        if inputValue is None:
            docTrack._err("'None' value not allowed for The DocumentTracking requested function")
        if dataType == COLTYPE_STR:
            self.__inputValue = str(inputValue)
        elif  dataType == COLTYPE_INT:
            self.__inputValue = int(inputValue)
        else:
            self.__inputValue = inputValue
        self.__isConstant = isConstant

    def _getDatabaseType(self):
        if self.__isUpdate and self.__previousInputValue == None:
            return DbIndexingClient.DBTABLE_UPDATE_KEY
        else:
            return DbIndexingClient.DBTABLE_DEF_COL
    
    def _setPreviousValue(self, previousValue):
        """
            previous value is used to manage Update for premary key
        """
        self.__previousInputValue = previousValue
    
    def _getPreviousInputValue(self):
        return self.__previousInputValue
    
    def _isUpdateKeyChanged(self):
        return self.__previousInputValue != None
    
    def _isUpdate(self):
        return self.__isUpdate

    def setIsUpdate(self, value):
        self.__isUpdate = value
        if value:
            self._setPreviousValue( None )

    def _getDataType(self):
        return self.__dataType

    def _getInputValue(self):
        return self.__inputValue

    def _isConstant(self):
        return self.__isConstant
    
    def __str__(self):
        return 'DataStruct(self,%s,"%s","%s",%s)' % (str(self.__isUpdate),str(self.__dataType),str(self.__inputValue),str(self.__isConstant))

    def __repr__(self):
        return str(self)
  
class DocumentTracking:
    
    def __init__(self, isActivated=True, logger = None):
        """ constructor just store provided object information """
        self.__logging = logger
        self._indexingClient = None
        self._indexingClient_db = None
        self._productionLine = DataStruct(self,False,COLTYPE_STR,"Fixed Production  Line",True)
        
        self.activate(isActivated)
        self.__initFromEnv()

    def __initFromEnv(self):
        self._encoding = "UTF8" 
        # SMD configuration information
        self._smdHostName = os.environ.get('SMD_HOST','localhost') 
        self._smdPort = os.environ.get('SMD_PORT','29100')
        # database configuration information get from pdcservice
        self._dbJdbcDriver = os.environ.get('JDBC_DRIVER','oracle.jdbc.driver.OracleDriver')
        self._dbJdbcString = os.environ.get('JDBC_STRING','jdbc:oracle:thin:@figaro:1521:FIGARODB') 
        self._dbUser = os.environ.get('PRODUCER_DB_USER_','producer') 
        self._dbPasswd = os.environ.get('PRODUCER_DB_PASSWRD_','producer')
        # init the main communication objects
        self._closeSmdAndDb()
            
    def activate(self,isActivated):
        self._closeSmdAndDb()
        self.__isActivated = isActivated

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

    def changeEncoding(self, encoding):
        self._closeSmdAndDb()
        # change the default value set by pdcservice to execute on an other SMD than the default one
        self._encoding = encoding 
        self._indexingClient = None
        
    def changeSmd(self, hostname, port):
        self._closeSmdAndDb()
        # change the default value set by pdcservice to execute on an other SMD than the default one
        self._smdHostName = hostname 
        self._smdPort = port 

        
    def changeDatabase(self, dbJdbcDriver, dbJdbcString, dbUser, dbPasswd):
        self._closeSmdAndDb()
        # change the default value set by pdcservice to execute on an other DATABASE than the default one
        self._dbUser = dbUser
        self._dbPasswd = dbPasswd
        self._dbJdbcDriver = dbJdbcDriver 
        self._dbJdbcString = dbJdbcString

    def _closeSmdAndDb(self):
        # close the database connection and the connection to SMD
        # this method is always called if we change a default parameter (encoding, SMD or Database
        if self._indexingClient is not None:
             if self._indexingClient_db is not None:
                 self._indexingClient.sqlClose(self._indexingClient_db) 
             self._indexingClient.disconnect()
             self._indexingClient = None
             self._indexingClient_db = None

    def _initSmdAndDb(self):
        # open the connection to SMD and to the Database if there is not still existing
        if self.__isActivated:
            if self._indexingClient is None:
                 self._indexingClient = DbIndexingClient.DbIndexingClient(self._encoding,self._smdHostName,int(self._smdPort))
                 # Connect to SMD
                 self._indexingClient.connect()
                 # load the JdbcDriver 
                 self._indexingClient.sqlInit(self._dbJdbcDriver) 
                 # connect the database 
                 self._indexingClient_db = self._indexingClient.sqlOpen(self._dbJdbcString ,self._dbUser , self._dbPasswd ) 
        else:
            if self._indexingClient is None:
                self._indexingClient = DbIndexingClient.DbIndexingClient(self._encoding,self._smdHostName,int(self._smdPort))
            self._log(_MSG_DOC_TACK_NOT_ACTIVATED_)
             
    def __writeDescriptionInFileForDebug(self, outputDir, prefixFileName, inputFileDescription, databaseTableDescription):
        self._initSmdAndDb()
        fTst = open('%s/%s.input.xml' % (outputDir, prefixFileName),'w')
        fTxtContent = self._indexingClient.arrayToXml('INPUT',inputFileDescription)
        fTst.writelines(fTxtContent)
        fTst.close()
        fTst = open('%s/%s.database.xml' % (outputDir, prefixFileName),'w')
        fTxtContent = self._indexingClient.arrayToXml('DB',databaseTableDescription)
        fTst.writelines(fTxtContent)
        fTst.close()

    def _buildDescriptionOne(self, inputFileDescription, databaseTableDescription , inputField, dbColName, inputColName):
        if inputField is not None:
            if inputField._isConstant():
                databaseTableDescription.append([inputField._getDatabaseType(),inputField._getDataType(),dbColName,inputField._getInputValue(), DbIndexingClient.COLCONST])
                if inputField._isUpdateKeyChanged():
                    databaseTableDescription.append([DbIndexingClient.DBTABLE_UPDATE_KEY,inputField._getDataType(),dbColName,inputField._getPreviousInputValue(), DbIndexingClient.COLCONST])
            else:
                if inputFileDescription is not None:
                    inputFileDescription.append([DbIndexingClient.INPUT_DEF_COLUMN,inputField._getInputValue(),inputColName])
                    databaseTableDescription.append([inputField._getDatabaseType(),inputField._getDataType(),dbColName,inputColName, DbIndexingClient.COLINPUT])
        
    def __buildDescription(self , BusinessID, DocumentID, JobID=None, FileID=None, DocumentStage=None, DocumentStatus=None, paddValue=None):
        databaseTableDescription = [[DbIndexingClient.DBTABLE_DEF,'DOCUMENT_TRACKING']]
        # databaseTableDescription.append([DbIndexingClient.DBTABLE_DEF_COL,DbIndexingClient.COLTYPE_STR,'BUSINESS_ID',BusinessID, DbIndexingClient.COLCONST])
        self._buildDescriptionOne(None, databaseTableDescription, BusinessID, 'BUSINESS_ID', None)

        inputFileDescription = [[DbIndexingClient.INPUT_CSV_DELIMITER,'\t']]
        
        self._buildDescriptionOne(inputFileDescription, databaseTableDescription, DocumentID,'DOCUMENT_ID','DOCUMENTID')
        self._buildDescriptionOne(inputFileDescription, databaseTableDescription, JobID,'JOB_ID','JOBID')
        self._buildDescriptionOne(inputFileDescription, databaseTableDescription, FileID,'FILE_NUMBER','FILEID')
        self._buildDescriptionOne(inputFileDescription, databaseTableDescription, DocumentStage,'DOCUMENT_STAGE','DOCUMENTSTAGE')
        self._buildDescriptionOne(inputFileDescription, databaseTableDescription, DocumentStatus,'DOCUMENT_STATUS','DOCUMENTSTATUS')
        
        self._buildDescriptionOne(inputFileDescription, databaseTableDescription, self._productionLine,'PRODUCTION_LINE',None)
        self._buildDescriptionOne(inputFileDescription, databaseTableDescription, paddValue,'tech_field_padd_key',None)
        
        # self.__writeDescriptionInFileForDebug("H:/dbg/DocumentTaching/tst_indexer_data", BusinessID, inputFileDescription, databaseTableDescription)
        
        return inputFileDescription, databaseTableDescription
             
    def insertNewDocumentList( self , inputFile, inputType, inputFileDescription, databaseTableDescription):
        if self.__isActivated:
            self._initSmdAndDb()
            self._indexingClient.indexCsv(self._indexingClient_db,inputFile, inputType, inputFileDescription, databaseTableDescription)
        else:
            self._log(_MSG_DOC_TACK_NOT_ACTIVATED_)
        
    def updateExistingDocumentList( self , inputFile, inputType, inputFileDescription, databaseTableDescription):
        if self.__isActivated:
            self._initSmdAndDb()
            self._indexingClient.updateIndexCsv(self._indexingClient_db,inputFile, inputType, inputFileDescription, databaseTableDescription)
        else:
            self._log(_MSG_DOC_TACK_NOT_ACTIVATED_)

    def updateDocumentTrackingInfo(self, databaseTableDescription):
        if self.__isActivated:
            self._initSmdAndDb()
            self._indexingClient.updateDatabase(self._indexingClient_db,databaseTableDescription)
        else:
            self._log(_MSG_DOC_TACK_NOT_ACTIVATED_)
        

    def _getDataStruct(self, isUpdateKey, dataType, inputValue, isConstant, isNullable = True):
        if inputValue.__class__ is DataStruct:
            return inputValue
        elif inputValue is None and isNullable:
            return None
        else:
            return DataStruct(self, isUpdateKey, dataType, inputValue, isConstant)
        
    def insertStatusDocumentLevel(self , businessID, documentColID, inputFile, inputFileType, documentStageValue, documentStatusValue):
        business = self._getDataStruct(False, COLTYPE_STR, businessID, True)
        document = self._getDataStruct(False, COLTYPE_STR, documentColID, False, False)
        stage = self._getDataStruct(False, COLTYPE_STR, documentStageValue, True)
        status = self._getDataStruct(False, COLTYPE_STR, documentStatusValue, True)
        padd = self._getDataStruct(False, COLTYPE_STR, PADD_NOT_ACTIVE, True)

        inputFileDescription , databaseTableDescription = self.__buildDescription(business, document, None, None, stage, status, padd)
        self.insertNewDocumentList(inputFile, inputFileType, inputFileDescription, databaseTableDescription)

    def updateStatusDocumentLevel(self , businessID, documentColID, inputFile, inputFileType, documentStageValue, documentStatusValue):
        business = self._getDataStruct(True, COLTYPE_STR, businessID, True)
        document = self._getDataStruct(True, COLTYPE_STR, documentColID, False, False)
        stage = self._getDataStruct(False, COLTYPE_STR, documentStageValue, True)
        status = self._getDataStruct(False, COLTYPE_STR, documentStatusValue, True)

        if stage is not None or status is not None:
            inputFileDescription , databaseTableDescription = self.__buildDescription(business, document, None, None, stage, status)
            self.updateExistingDocumentList(inputFile, inputFileType, inputFileDescription, databaseTableDescription)
        
    def insertJobDocumentLevel(self , businessID, documentColID, inputFile, inputFileType, jobIDValue, fileIDValue):
        business = self._getDataStruct(False, COLTYPE_STR, businessID, True)
        document = self._getDataStruct(False, COLTYPE_STR, documentColID, False, False)
        job = self._getDataStruct(False, COLTYPE_INT, jobIDValue, True)
        file = self._getDataStruct(False, COLTYPE_INT, fileIDValue, True)
        if jobIDValue is not None:
            paddValue = DataStruct(self,False,COLTYPE_STR,PADD_ACTIVE,True)
        else:
            paddValue = DataStruct(self,False,COLTYPE_STR,PADD_NOT_ACTIVE,True)
            
        inputFileDescription , databaseTableDescription = self.__buildDescription(business, document, job, file, None, None, paddValue)
        self.insertNewDocumentList(inputFile, inputFileType, inputFileDescription, databaseTableDescription)

    def updateJobDocumentLevel(self , businessID, documentColID, inputFile, inputFileType, jobIDValue, fileIDValue):
        business = self._getDataStruct(True, COLTYPE_STR, businessID, True)
        document = self._getDataStruct(True, COLTYPE_STR, documentColID, False, False)
        job = self._getDataStruct(False, COLTYPE_INT, jobIDValue, True)
        file = self._getDataStruct(False, COLTYPE_INT, fileIDValue, True)
        if jobIDValue is not None:
            paddValue = DataStruct(self,False,COLTYPE_STR,PADD_ACTIVE,True)
        else:
            paddValue = None

        if job is not None or file is not None:
            inputFileDescription , databaseTableDescription = self.__buildDescription(business, document, job, file, None, None, paddValue)
            self.updateExistingDocumentList(inputFile, inputFileType, inputFileDescription, databaseTableDescription)

    def __updateStatus(self , whereStr, DocumentStage, DocumentStatus):
        if self.__isActivated:
            setStr = None
            if DocumentStage is not None and DocumentStatus is not None:
                setStr = "DOCUMENT_STAGE='%s', DOCUMENT_STATUS='%s'" % (DocumentStage, DocumentStatus)
            elif DocumentStage is not None:
                setStr = "DOCUMENT_STAGE='%s'" % (DocumentStage) 
            elif DocumentStatus is not None:
                setStr = "DOCUMENT_STATUS='%s'" % (DocumentStatus)
                 
            if whereStr is not None and setStr is not None:
                self._initSmdAndDb()
                mycursor = self._indexingClient.execSql(self._indexingClient_db , "update DOCUMENT_TRACKING set %s where %s" % (setStr, whereStr))
            else:
                self._err('Cant update will None parameters')
        else:
            self._log(_MSG_DOC_TACK_NOT_ACTIVATED_)

    def updateStatusBusinessLevel(self , BusinessID, DocumentStage, DocumentStatus):
        whereStr = "BUSINESS_ID='%s'" % (BusinessID)
        self.__updateStatus(whereStr, DocumentStage, DocumentStatus)

    def updateStatusJobFileLevel(self , BusinessID, JobID, FileID, DocumentStage, DocumentStatus):
        whereStr = "BUSINESS_ID='%s' and JOB_ID=%s" % (BusinessID, JobID)
        if FileID is not None:
            whereStr = whereStr + " and FILE_NUMBER=%s" % (FileID)
        self.__updateStatus(whereStr, DocumentStage, DocumentStatus)
            
    def updateJobBusinessLevel(self , BusinessID, JobID, FileID):
        if self.__isActivated:
            setStr = None
            whereStr = "BUSINESS_ID='%s'" % (BusinessID)
            if JobID is not None and FileID is not None:
                setStr = "JOB_ID=%s, FILE_NUMBER=%s, tech_field_padd_key=%s" % (JobID,FileID,PADD_ACTIVE)
            elif JobID is not None:
                setStr = "JOB_ID=%s, tech_field_padd_key=%s" % (JobID,PADD_ACTIVE)
            elif FileID is not None:
                setStr = "FILE_NUMBER=%s" % (FileID)
                
            if whereStr is not None and setStr is not None:
                self._initSmdAndDb()
                mycursor = self._indexingClient.execSql(self._indexingClient_db , "update DOCUMENT_TRACKING set %s where %s" % (setStr, whereStr))
            else:
                self._err('Cant update will None parameters')
        else:
            self._log(_MSG_DOC_TACK_NOT_ACTIVATED_)

    def updateFileJobLevel(self , BusinessID, JobID, FileID):
        if self.__isActivated:
            setStr = None
            whereStr = "BUSINESS_ID='%s' and JOB_ID=%s" % (BusinessID, JobID)
            if FileID is not None:
                setStr = "FILE_NUMBER=%s" % (FileID)
                
            if whereStr is not None and setStr is not None:
                self._initSmdAndDb()
                mycursor = self._indexingClient.execSql(self._indexingClient_db , "update DOCUMENT_TRACKING set %s where %s" % (setStr, whereStr))
            else:
                self._err('Cant update will None parameters')
        else:
            self._log(_MSG_DOC_TACK_NOT_ACTIVATED_)

    """
        the deleteBusinessJobFileLevel function delete document
    """
    def deleteBusinessJobFileLevel(self , BusinessID, JobID=None, FileID=None):
        if self.__isActivated:
            setStr = None
            whereStr = "BUSINESS_ID='%s'" % (BusinessID)
            if JobID is not None:
                setStr = " and JOB_ID=%s" % (JobID)
                if FileID is not None:
                    setStr = " and FILE_NUMBER=%s" % (FileID)
                
            if whereStr is not None:
                self._initSmdAndDb()
                mycursor = self._indexingClient.execSql(self._indexingClient_db , "delete from DOCUMENT_TRACKING where %s" % (whereStr))
            else:
                self._err('Cant delete will BusinessID with None value')
        else:
            self._log(_MSG_DOC_TACK_NOT_ACTIVATED_)
        
def getBusinessIdFromFile(busOrigFile):
    if False:
        fBus = open(busOrigFile,'r')
        businessID = fBus.readline()
        fBus.close()
        return businessID
    return 'NotKnownYet'

""" TEST PART """
def _initEnvOutSmdCall():
    # os.environ['SMD_HOST'] = 'figaro'
    # os.environ['SMD_PORT'] = '29110'
    os.environ['SMD_HOST'] = os.environ.get('SMD_HOST','localhost')
    os.environ['SMD_PORT'] = os.environ.get('SMD_PORT','29100')
    # database configuration information get from pdcservice
    if False :
        os.environ['JDBC_DRIVER'] =os.environ.get('JDBC_DRIVER','oracle.jdbc.driver.OracleDriver')
        os.environ['JDBC_STRING'] = os.environ.get('JDBC_STRING','jdbc:oracle:thin:@figaro:1521:FIGARODB')
        os.environ['PRODUCER_DB_USER_'] = os.environ.get('PRODUCER_DB_USER_','producer_1_1a')
        os.environ['PRODUCER_DB_PASSWRD_'] = os.environ.get('PRODUCER_DB_PASSWRD_','producer')
    else:
        os.environ['JDBC_DRIVER'] =os.environ.get('JDBC_DRIVER','com.mysql.jdbc.Driver')
        os.environ['JDBC_STRING'] = os.environ.get('JDBC_STRING','jdbc:mysql://localhost:3306/python')
        os.environ['PRODUCER_DB_USER_'] = os.environ.get('PRODUCER_DB_USER_','python')
        os.environ['PRODUCER_DB_PASSWRD_'] = os.environ.get('PRODUCER_DB_PASSWRD_','python')
    
    print os.environ

def __tstDevWithoutDocumentLevel():
    docTrack = DocumentTracking()
    ### 
    BusinessId = 1
    JobID = 3
    FileId = 0
    docTrack.updateJobBusinessLevel(BusinessId, JobID, None)
    docTrack.updateJobBusinessLevel(BusinessId, None, FileId)
    
    BusinessId = 2
    JobID = 4
    docTrack.updateJobBusinessLevel(BusinessId, JobID, FileId)
    
    ###    
    BusinessId = 1
    Stage = 'PyhtonTest'
    Level = 'start'
    docTrack.updateStatusBusinessLevel(BusinessId,Stage,None)
    docTrack.updateStatusBusinessLevel(BusinessId, None, Level)

    BusinessId = 2
    Stage = 'PyhtonTestSecondStage'
    docTrack.updateStatusBusinessLevel(BusinessId,Stage,Level)

    ###
    BusinessId = 1
    JobID = 3
    FileId = 1
    docTrack.updateFileJobLevel(BusinessId, JobID, FileId)
    ###
    BusinessId = 1
    JobID = 3
    FileId = 1
    Stage = 'PyhtonTestThird'
    Level = 'end'
    docTrack.updateStatusJobFileLevel(BusinessId, JobID, FileId,Stage,Level)
    
    docTrack.deleteBusinessJobFileLevel(BusinessId)
    
if __name__ == '__main__':
    try :
        __tstDevWithoutDocumentLevel()
    except Exception , e :
        print "service instanciation error : " , str(e)
        