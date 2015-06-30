import os.path

import DbIndexingClient
from DocumentTracking import DocumentTracking
from DocumentTracking import COLTYPE_STR
from DocumentTracking import COLTYPE_INT
from DocumentTracking import DataStruct
from DocumentTracking import FILE_TYPE_CSV

#
# This class is a stream manage. The stream is a set of document managed together
# the goal of the class is to optimize the insert and update management of document tracking information
#

__KEY_USER_INFO__      = 'USER_TABLE_INFORMATION'
__KEY_DOC_TRACK_INFO__ = 'DOC_TRACK_INFORMATION'

__TRACK_MODE_SIMPLE__  = False # 'SimpleTrackingMode'
__TRACK_MODE_HISTORY__ = True  # 'HistoryTrackingMode' # insert new line when PRODUCTION_LINE or JOB_ID change

__KEY_INSERTED__      = 'Inserted'
__KEY_TRACKING_MODE__ = 'HistoryMode'
__KEY_NEED_INSERT__   = 'NeedInsert'

# this constants describs the caracteristiques of each Database table
# The structure is [Column Name, need insert line in History Mode, isUpdateDefault, dataType, isConstant, isNullable, isForUpdateDocLevel, isUpdateForSteamLevel, alwaysUpdateDocLevel]
__PADD_KEY__                 = ['tech_field_padd_key' , False, False, COLTYPE_STR, True , False, False, False, False]
__BUSINESS_ID_KEY__          = ['BUSINESS_ID'         , False, False, COLTYPE_STR, True , True , True , True , False]
__DOCUMENT_ID_KEY__          = ['DOCUMENT_ID'         , True , True , COLTYPE_STR, False, False, True , False, True ]
__PRODUCTION_LINE__          = ['PRODUCTION_LINE'     , True , True , COLTYPE_STR, True , False, True , True , False]
__JOB_ID_KEY__               = ['JOB_ID'              , True , True , COLTYPE_INT, True , False, True , True , True ]
__FILE_NUMBER_KEY__          = ['FILE_NUMBER'         , False, False, COLTYPE_INT, True , True , True , True , True ]
__DOCUMENT_STAGE_KEY__       = ['DOCUMENT_STAGE'      , False, False, COLTYPE_STR, True , True , False, False, False]
__DOCUMENT_STATUS_KEY__      = ['DOCUMENT_STATUS'     , False, False, COLTYPE_STR, True , True , False, False, False]
__DOCUMENT_NAME_KEY__        = ['DOCUMENT_NAME'       , False, False, COLTYPE_STR, False, True , False, False, False]
__DOCUMENT_DESCRIPTION_KEY__ = ['DOCUMENT_DESCRIPTION', False, False, COLTYPE_STR, False, True , False, False, False]
__VPF_FILE__                 = ['TECH_FIELD_OPVPFPATH', False, False, COLTYPE_STR, True, True , False, False, False]
__VPF_OFFSET__               = ['OPOFFSET'            , False, False, COLTYPE_STR, False, True , False, False, False]

# 
class MetaDataStruct:
    
    def __init__(self, isChange, dataStruct, isForUpdateDocLevel = False, isUpdateForSteamLevel = False, alwaysUpdateAtDocLevel = False):
        self._isChanged = isChange
        self._dataStruct = dataStruct
        self.__isForUpdateDocLevel = isForUpdateDocLevel
        self.__isUpdateForSteamLevel = isUpdateForSteamLevel
        self.__alwaysUpdateAtDocLevel = alwaysUpdateAtDocLevel
        self.__forUpdate = None
    
    def setDataStruct(self, dataStruct, needNewDataStruct = False):
        isUpdateKey = dataStruct._isUpdate()
        dataType    = dataStruct._getDataType()
        inputValue  = dataStruct._getInputValue()
        isConstant  = dataStruct._isConstant()
        
        if not needNewDataStruct and self._dataStruct._isUpdate() != isUpdateKey:
            needNewDataStruct = True
            if self._isChanged:
                # the field is not yet inserted it must not be see as update
                dataStruct.setIsUpdate(False)
        if not needNewDataStruct and self._dataStruct._getDataType() != dataType:
            needNewDataStruct = True
        if not needNewDataStruct and self._dataStruct._getInputValue() != inputValue:
            needNewDataStruct = True
            if isUpdateKey:
                dataStruct._setPreviousValue(self._dataStruct._getInputValue())
        if not needNewDataStruct and self._dataStruct._isConstant() != isConstant:
            needNewDataStruct = True
        
            
        if needNewDataStruct :
            self._dataStruct = dataStruct
            self._isChanged = True
            
    def isChanged(self):
        return self._isChanged
    
    def getDataStruct(self):
        return self._dataStruct

    # function called after the insert/update of this value on the document tracking system.
    # the isChange is then false
    def _validated(self):
        self._isChanged = False
        if self.__isForUpdateDocLevel:
            self._dataStruct.setIsUpdate(True)
    
    def _isForUpdateDocLevel(self):
        return self.__isForUpdateDocLevel
    
    def _isUpdateForSteamLevel(self):
        return self.__isUpdateForSteamLevel and self._dataStruct._isConstant()
    
    def _isDocumentLevel(self):
        return not self._dataStruct._isConstant()

    def _isAlwaysUpdateAtDocLevel(self):
        return self.__alwaysUpdateAtDocLevel
    
    def setForUpdate(self, forUpdate):
        self.__forUpdate = forUpdate
    
    def __str__(self):
        return 'MetaDataStruct(%s,%s,%s,%s,%s)' % (str(self._isChanged),str(self._dataStruct),str(self.__isForUpdateDocLevel),str(self.__isUpdateForSteamLevel),str(self.__alwaysUpdateAtDocLevel))

    def __repr__(self):
        return str(self)

### TODO management of the merge / split of 2 DocumentTrackingStream

class DocumentTrackingStream(DocumentTracking):
    
    def __init__(self, filename, isActivated=True, logger = None):
        DocumentTracking.__init__(self, isActivated, logger)
        self.__initValueFileName = filename
        self.__isHistoryMode = False
        self.__alreadyInserted = False
        self.__needInsert = False
        self.__docTrackInformation  = {}
        self.__userTableInformation = None
        if self.__initValueFileName is not None:
            self._loadInitValue()

    def __str__(self):
        return str({__KEY_INSERTED__   :self.__alreadyInserted,
                __KEY_TRACKING_MODE__  :self.__isHistoryMode,
                __KEY_NEED_INSERT__    :self.__needInsert,
                __KEY_DOC_TRACK_INFO__ :self.__docTrackInformation,
                __KEY_USER_INFO__      :self.__userTableInformation})
        
    def _loadInitValue(self):
        if os.path.isfile(self.__initValueFileName) and os.path.exists(self.__initValueFileName):
            try:
                f = open(self.__initValueFileName,"r")
                strContent = ''.join(f.readlines())
                f.close()
                if len(strContent) > 0:
                        fileContent = eval(strContent)
                        self.__docTrackInformation  = fileContent.get(__KEY_DOC_TRACK_INFO__, {})
                        self.__userTableInformation = fileContent.get(__KEY_USER_INFO__     , None)
                        self.__alreadyInserted      = fileContent.get(__KEY_INSERTED__      , False)
                        self.__isHistoryMode        = fileContent.get(__KEY_TRACKING_MODE__ , False)
                        self.__needInsert           = fileContent.get(__KEY_NEED_INSERT__   , False)
            except Exception , e :
                self._err('Invalide input file for document tracking init [%s]' % (self.__initValueFileName))
                    

    def __check(self,key,defaultValue):
        keyName     = key[0]
        info = self.__docTrackInformation.get(keyName,None)
        if info is None:
            if defaultValue is None:
                raise Exception('%s Must be define' % (keyName))
            else:
                self.__manageInfo(key,defaultValue)
                self._log('"%s" set to default value "%s"' % (keyName,str(defaultValue)))
        
    def __checkDefaultInfo(self):
        self.__check(__PADD_KEY__,'defaultPadd')
        self.__check(__DOCUMENT_ID_KEY__,None)
        self.__check(__PRODUCTION_LINE__,'defaultProductionLine')
        self.__check(__JOB_ID_KEY__,-1)
            
    def save(self, useGeneratedFileName = False, removeOriginalFile = False):
        if useGeneratedFileName:
            newFileName = ['%s/' % (os.path.dirname(self.__initValueFileName))]
            if self.__docTrackInformation.get(__PRODUCTION_LINE__[0], None) is not None:
                newFileName.append(str(self.__docTrackInformation.get(__PRODUCTION_LINE__[0]).getDataStruct()._getInputValue()))
            if self.__docTrackInformation.get(__JOB_ID_KEY__[0], None) is not None:
                newFileName.append(str(self.__docTrackInformation.get(__JOB_ID_KEY__[0]).getDataStruct()._getInputValue()))
            if self.__docTrackInformation.get(__FILE_NUMBER_KEY__[0], None) is not None:
                newFileName.append(str(self.__docTrackInformation.get(__FILE_NUMBER_KEY__[0]).getDataStruct()._getInputValue()))
            newFileName.append(os.path.basename(self.__initValueFileName))
            if removeOriginalFile:
                os.remove(self.__initValueFileName)
            self.__initValueFileName = '_'.join(newFileName)
            
        f = open(self.__initValueFileName,"w")
        f.write(str(self))
        f.close()
        
    def setAlreadyInsert(self):
        self.__needInsert = False
        for key in self.__docTrackInformation.keys():
            info = self.__docTrackInformation[key]
            info._validated()
#
# __manageInfo function, add or update the information about the Key
#
    def __manageInfo(self, key, value, isConstantChange = None, forced = False):
        keyName                = key[0]
        keyHistory             = key[1]
        isUpdateKey            = key[2]
        dataType               = key[3]
        isConstant             = key[4]
        isNullable             = key[5]
        isForUpdateDocLevel    = key[6]
        isUpdateForSteamLevel  = key[7]
        alwaysUpdateAtDocLevel = key[8]
        if isConstantChange != None:
            isConstant = isConstantChange
        dataStruct = self._getDataStruct(isUpdateKey, dataType, value, isConstant, isNullable)
        curValue = self.__docTrackInformation.get(keyName, None)
        if curValue is None:
            # new Value
            if keyHistory:
                self.__needInsert = True
                dataStruct.setIsUpdate(False)
            curValue = MetaDataStruct(True,dataStruct,isForUpdateDocLevel,isUpdateForSteamLevel,alwaysUpdateAtDocLevel)
            self.__docTrackInformation[keyName] = curValue
        else:
            # management of the update of the curValue
            if keyHistory and self.__isHistoryMode:
                self.__needInsert = True
                dataStruct.setIsUpdate(False)
            curValue.setDataStruct(dataStruct, forced)
        return curValue
            
    def setDocumentID(self, value, isConstant = False, forUpdate = True):
        curValue = self.__manageInfo(__DOCUMENT_ID_KEY__, value, isConstant)
        curValue.setForUpdate(forUpdate)
            
    def setProductionLine(self, value, isConstant = True, forUpdate = True):
        curValue = self.__manageInfo(__PRODUCTION_LINE__, value, isConstant)
        curValue.setForUpdate(forUpdate)
            
    def setJobID(self, value, isConstant = True, forUpdate = True):
        curValue = self.__manageInfo(__JOB_ID_KEY__, value, isConstant)
        curValue.setForUpdate(forUpdate)
            
    def setPadd(self, value, isConstant = True, forced = False):
        self.__manageInfo(__PADD_KEY__, value, isConstant, forced)
            
    def setBusinessID(self, value, isConstant = True, forced = False):
        self.__manageInfo(__BUSINESS_ID_KEY__, value, isConstant, forced)
        
    def setFileNumber(self, value, isConstant = True, forced = False):
        self.__manageInfo(__FILE_NUMBER_KEY__, value, isConstant, forced)
        
    def setDocumentStage(self, value, isConstant = True, forced = False):
        self.__manageInfo(__DOCUMENT_STAGE_KEY__, value, isConstant, forced)
        
    def setDocumentStatus(self, value, isConstant = True, forced = False):
        self.__manageInfo(__DOCUMENT_STATUS_KEY__, value, isConstant, forced)
        
    def setDocumentName(self, value, isConstant = False, forced = False):
        self.__manageInfo(__DOCUMENT_NAME_KEY__, value, isConstant, forced)
        
    def setDocumentDescription(self, value, isConstant = False, forced = False):
        self.__manageInfo(__DOCUMENT_DESCRIPTION_KEY__, value, isConstant, forced)

    def setVpfFile(self, value, isConstant = True, forced = False):
        self.__manageInfo(__VPF_FILE__, value, isConstant, forced)

    def setVpfOffset(self, value, isConstant = False, forced = False):
        self.__manageInfo(__VPF_OFFSET__, value, isConstant, forced)
    
    def setFileName(self, fileName):
        self.__initValueFileName = fileName
        if self.__initValueFileName is not None:
            self._loadInitValue()

    # Put the document tracking information in the database
    def validateDocumentTracking(self, idxFileName, logDebug = False, forceDocumentLevel = False):
        # Generate Data
        needDatabaseUpdate = False
        needDocumentLevelUpdate = forceDocumentLevel
        databaseTableDescription = [[DbIndexingClient.DBTABLE_DEF,'DOCUMENT_TRACKING']]
        inputFileDescription = [[DbIndexingClient.INPUT_CSV_DELIMITER,'\t']]
        self.__checkDefaultInfo()
        for key in self.__docTrackInformation.keys():
            info = self.__docTrackInformation[key]
            self._log("validateDocumentTracking : Key [%s] Info [%s]" % (key,str(info)))
            if not needDatabaseUpdate and (self.__needInsert or info.isChanged()):
                needDatabaseUpdate = True
            # the changed values are managed to define if a standard request can be done or if a 'by document' request is needed
            # if there is only constant values must be updated a direct sql request is done
            # if one non constant value must be updated 
            ## TODO management of changed / update / isConstant values
            if info.isChanged() or self.__needInsert:
                self._buildDescriptionOne(inputFileDescription, databaseTableDescription, info.getDataStruct(),key,key)
                if info._isAlwaysUpdateAtDocLevel() or info._isDocumentLevel():
                    needDocumentLevelUpdate = True
        # the second path is to list the right update keys depending on needDocumentLevelUpdate
        if not self.__needInsert:
            for key in self.__docTrackInformation.keys():
                info = self.__docTrackInformation[key]
                if not info.isChanged():
                    if (needDocumentLevelUpdate and info._isForUpdateDocLevel()) or (not needDocumentLevelUpdate and info._isUpdateForSteamLevel()):
                        self._buildDescriptionOne(inputFileDescription, databaseTableDescription, info.getDataStruct(), key, key)
                    
            
        if needDatabaseUpdate:
            if logDebug :
                self._initSmdAndDb()
                self._log(self._indexingClient.arrayToXml('INPUT',inputFileDescription))
                self._log(self._indexingClient.arrayToXml('DB',databaseTableDescription))
            if needDocumentLevelUpdate:
                self._log('Indexing Document Level')
                self.updateExistingDocumentList(idxFileName, FILE_TYPE_CSV, inputFileDescription, databaseTableDescription)
            else:
                # TODO Blinder l'update au niveau Stream afin d'avoir la certitude que les critaire d'update sont bien discrimiants
                # sinon il faudra systematiquement faire un update niveau document
                self._log('Indexing JobID/FileNumber/ProductionLine Level')
                self.updateDocumentTrackingInfo(databaseTableDescription)
            self.__needInsert = False

        for info in self.__docTrackInformation.itervalues():
            info._validated()

def testAll(iniFileName,inputIndexFile, businessId):
    print 'start'
    print 'Init & Load'
    docTrack = DocumentTrackingStream(iniFileName, True)
    print 'set Document ID '
    docTrack.setDocumentID(0, False)
    docTrack.setDocumentID(0, False)
    print 'set Business ID '
    docTrack.setBusinessID(businessId, True)
    docTrack.validateDocumentTracking(inputIndexFile,True)
    print 'set Document Stage, '
    docTrack.setDocumentStage('StageTest (%s)' % (inputIndexFile), False)
    docTrack.validateDocumentTracking(inputIndexFile,True)
    print 'set Document Status, '
    docTrack.setDocumentStatus('StatusTest (%s)' % (inputIndexFile), False)
    docTrack.validateDocumentTracking(inputIndexFile,True)
    print 'set Document Name, '
    docTrack.setDocumentName(1, False, False)
    docTrack.validateDocumentTracking(inputIndexFile,True)
    print 'set Document Description, '
    docTrack.setDocumentDescription(2, False, False)
    docTrack.validateDocumentTracking(inputIndexFile,True)
    print 'Save'
    docTrack.save(False, False)
    print 'ok'
    
    return docTrack

def testAllOneValid(iniFileName,inputIndexFile, businessId):
    print 'start'
    print 'Init & Load'
    docTrack = DocumentTrackingStream(iniFileName, True)
    print 'set Document ID '
    docTrack.setDocumentID(0, False)
    docTrack.setDocumentID(0, False)
    print 'set Business ID '
    docTrack.setBusinessID(businessId, True)
    print 'set Document Stage, '
    docTrack.setDocumentStage('StageTest (%s)' % (inputIndexFile), False)
    print 'set Document Status, '
    docTrack.setDocumentStatus('StatusTest (%s)' % (inputIndexFile), False)
    print 'set Document Name, '
    docTrack.setDocumentName(1, False, False)
    print 'set Document Description, '
    docTrack.setDocumentDescription(2, False, False)
    docTrack.validateDocumentTracking(inputIndexFile,True)
    print 'Save'
    docTrack.save(False, False)
    print 'ok'
    
    return docTrack

def testMerge(iniFileName,inputIndexFile, jobID):
    print 'testMerge : start'
    docTrack = DocumentTrackingStream(iniFileName, True)
    docTrack.setDocumentID(0, False)
    docTrack.setAlreadyInsert()
    testChangeJobId(docTrack,jobID,inputIndexFile)
    print 'set Document Stage, '
    docTrack.setDocumentStage('StageTest (%s)' % (inputIndexFile), False)
    docTrack.validateDocumentTracking(inputIndexFile,True)
    print 'Save'
    docTrack.save(False, False)
    print 'ok'
    
    return docTrack
        
            
def testChangeJobId(docTrack,newJobID,inputIndexFile):
    print 'testChangeJobId : start'
    print 'testChangeJobId : set Job ID '
    docTrack.setJobID(newJobID, True)
    docTrack.validateDocumentTracking(inputIndexFile,True)
    print 'testChangeJobId : Save'
    docTrack.save(True, False)
    print 'testChangeJobId : ok'

if __name__ == '__main__':
    try :
        os.environ['SMD_HOST']             = os.environ.get('SMD_HOST','localhost')
        os.environ['SMD_PORT']             = os.environ.get('SMD_PORT','29100')
        os.environ['JDBC_DRIVER']          = os.environ.get('JDBC_DRIVER','com.mysql.jdbc.Driver')
        os.environ['JDBC_STRING']          = os.environ.get('JDBC_STRING','jdbc:mysql://localhost:3306/python')
        os.environ['PRODUCER_DB_USER_']    = os.environ.get('PRODUCER_DB_USER_','python')
        os.environ['PRODUCER_DB_PASSWRD_'] = os.environ.get('PRODUCER_DB_PASSWRD_','python')
        inputIndexFile1 = 'D:/Temp/producer/000023.vpf.ind1.dct'
        inputIndexFile2 = 'D:/Temp/producer/000023.vpf.ind2.dct'
        inputIndexFile3 = 'D:/Temp/producer/000023.vpf.ind3.dct'
        docTrack1 = testAll('D:/Temp/producer/docTrackStream1.ini',inputIndexFile1, '1')
        docTrack2 = testAll('D:/Temp/producer/docTrackStream2.ini',inputIndexFile2, '2')
        docTrack3 = testAllOneValid('D:/Temp/producer/docTrackStream3.ini',inputIndexFile3, '3')
        testChangeJobId(docTrack1,12,inputIndexFile1)
        testChangeJobId(docTrack2,57,inputIndexFile2)
        ## update of document comming from other index 
        inputIndexFile1_1 = 'D:/Temp/producer/000023-1.vpf.ind.dct'
        inputIndexFile1_2 = 'D:/Temp/producer/000023-2.vpf.ind.dct'
        docTrack1_1 = testMerge('D:/Temp/producer/docTrackStream1_1.ini',inputIndexFile1_1, 77)
        docTrack1_2 = testMerge('D:/Temp/producer/docTrackStream1_2.ini',inputIndexFile1_2, 88)
    except Exception , e :
        print "Error : " , str(e)
    print 'End'

