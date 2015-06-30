

import os.path
import log4py

from ParParser import ParParser
from LoggingProducerUtils import LoggingProducerUtils

"""
    PRODUCER Parameter Container is a class to manage the input argument of a srcipt
    When producer called a script, it give to him some parameters
    The list of parameters depend on the script type call
    This class check all of them in this context and provide methods to give the values
"""
# List of Param
PARAM_DIR="-DIR"    # Full path to Job Directory (/u/sefas/director/opd4512/traffic/jobs/CUST/DEPT/DOCT/001000)
PARAM_ORA="-DIRORA" # ???
PARAM_LST="-LIST"   # List containing jobs to concatenate (001000.tmp)
PARAM_JOB="-JOB"    # Job ID (001000)
PARAM_ERR="-ERR"    # Error Filename (001000_20011218093512.err)
PARAM_GRP="-GRP"    # Group Flag (Y or N)
PARAM_TST="-TST"    # Test Flag (TEST or PROD)
PARAM_TEST="-TEST"  # Dispatch Test Flag (TEST or PROD)
PARAM_PRT="-PRT"    # Print Filename (001000 (Script adds on -O01-0, -O02-0 etc.) )
PARAM_TYPE="-TYPE"  # Reprint Type (INT or REC)
                    # If Despatch Type is ONE then the print file corresponding to the -REP value should be despatched.
                    # If Despatch Type is ALL then all print files from 0 to the -REP value should be despatched.
PARAM_DAT="-DAT"    # Date Job Received (5/12/2001)
PARAM_JDE="-JDE"    # JDE Member (CLLU34)
PARAM_JNM="-JNM"    # Job Name (BPUT8485)
PARAM_RPF="-REPF"   # Source Reprint Cycle for Reprints (0-8)
PARAM_RPT="-REPT"   # Reprint Cycle to create (0-9)
PARAM_CFG="-CFG"    # Printer Configuration being used (REP (if Reprint Configuration is being used) / ORG (if Print Configuration is being used))
PARAM_MLA="-MLA"    # MLA Scripts Directory (/u/sefas/director/opd4512/mla_scripts)
PARAM_PDR="-PDIR"   # Printers Directory (scitex directories live under here) (/u/sefas/director/opd4512/printers)
PARAM_TAR="-TAR"    # SCITEX only - Sub Directory under Printers Directory (scitex01)
                    # DP_SERVER only - DP Server Target Directory (/u/opdd/dpserver)
                    # DFWORKS only - Directory to send Integrity files (/u/sefas/director/opd4512/traffic/original_integrity)
PARAM_HST="-HST"    # SCITEX only - Host Name of Scitex Controller (S220)
                    # DP_SERVER only - Form Scan Host (F40)
                    # Processing ???
PARAM_HST2="-HSTFNM"    # Processing ???
PARAM_PRQ="-PRQ"    # XEROX only - UNIX print queue to use (Xerox01)
                    # LISTINGS only - UNIX print queue to use (LIST1)
PARAM_FUN="-FUN"    # XEROX only - FunAsset WorkStation Host Name (FUN1)
PARAM_IPM="-IPM"    # LISTINGS only - InfoPrint Manager Host Name (39H)
PARAM_FRM="-FRM"    # DP_SERVER only - Form Scan Target Directory (/u/opdd/formscan)
PARAM_PID="-PID"    # DP_SERVER only - Printer ID (DP1)
PARAM_CAN="-CAN"    # Flag indicating whether or not job was cancelled rather than printed (Y or N)
PARAM_MLA="-MLA"    # MLA Scripts Directory (/u/sefas/director/opd4512/mla_scripts)
PARAM_IDF="-IDF"    # Print Filename (001000-O01-0) The updated IDF name will be <IDF Parameter>.IF0.complete
PARAM_STS="-STS"    # DFWORKS only - Status File Location (/u/sefas/director/opd4512ora/traffic/mailer_status/DC_OSI.DAT)
PARAM_TMP="-TMP"    # Full path to Temp Directory (/u/sefas/director/opd4512/traffic/temp)
PARAM_EXP="-EXP"    # Number of Mailpieces contained in the original IDF file (10000)
PARAM_MXP="-MXP"    # Number of Mailpieces contained in the original IDF file (10000)
PARAM_MSD="-MSD"    # Full path to Mailer Summary Directory 
PARAM_TYP="-TYP"    # Reprint Type (FILE or REPORT / If FILE then produce .reqm. / If REPORT then produce .reqm + an additional file .rpt containing an ascii report on reprints required. / (This parameter will always be FILE for Nationwide))
PARAM_RFP="-REFP"   # REFP Filename (001000-O01-1.refp)
PARAM_REP="-REP"    # Reprint Count - indicates which files need despatching (0-9)
PARAM_DST="-DEST"   # Despatch Directory (/u/columbus)
PARAM_TRN="-TRN"    # Transfer Out Directory (/u/sefas/director/opd4512/transfer_out)
PARAM_PC="-PC"      # Print Completion Directory
PARAM_OP="-OP"      # Inserter opertor name
PARAM_MRG="-MRG"    # Merge flag (N or Y)
PARAM_INT="-INT"    # Intergrity file name
PARAM_UPD="-UPD"    # Updated integrity directory
PARAM_FNO="-FNO"    # Output file number
PARAM_TFR="-TFR"    # Transfer in directory
PARAM_SRH="-SRH"    # Directory to search for files
PARAM_DEL="-DEL"    # Filename  delimiter
PARAM_MEMO="-MEMO"    # memo of job
PARAM_FNM = "-FNM" # probably file Number
PARAM_HFT = "-HFT"
PARAM_HC = "-HC"
PARAM_PR = "-PR"
PARAM_REL = "-REL"
PARAM_DES = "-DES"
PARAM_PPC = "-PPC"
PARAM_IN = "-IN"  
PARAM_OUT = "-OUT"  
PARAM_PRGP = "-PRGP"  
PARAM_MAN = "-MAN" # File Id for Manual Confirm 
PARAM_DJNM = "-DJNM" # Display Job Name
PARAM_SEL_UPD = "-SEL_UPD" # Select File Directory
PARAM_REP_UPD = "-REP_UPD" # Reprint File Directory
PARAM_LVL = "-LVL" # Level of count Page/Mailpieace required in reprint processing

PARAM_PREFIX = "-PREFIX"

PARAM_OMR = "-OMR"
PARAM_REG = "-REG"
PARAM_SERVICE_CLASS = "-SERVICE_CLASS"
PARAM_PRINTER_TYPE =  "-PRINTER_TYPE"
PARAM_NAME =  "-NAME"
PARAM_PTY = "-PTY"



LOGGER_JOBS_DIR="JOBS"
LOGGER_PRODUCER_LOG_DIR="PRODUCER_LOG"

RECEPTION_PLUGIN_PARAM_LST = [PARAM_DIR, PARAM_ERR]
RECEPTION_PLUGIN_OPTIONAL_PARAM_LST = [PARAM_TFR, PARAM_SRH, PARAM_DEL]

RECEPTION_PARAM_LST = [PARAM_DIR, PARAM_ERR]
RECEPTION_OPTIONAL_PARAM_LST = [PARAM_TMP]
# 
PROCESSING_PARAM_LST = [PARAM_DIR, PARAM_ORA, PARAM_JOB, PARAM_ERR, PARAM_GRP, PARAM_TST, PARAM_PRT, PARAM_DAT, PARAM_JNM]
PROCESSING_OPTIONAL_PARAM_LST = [PARAM_JDE, PARAM_MEMO, PARAM_HST, PARAM_HST2, PARAM_OMR, PARAM_REG]
# Test Param OK : -DIR /u/sefas/director/opd4512/traffic/jobs/CUST/DEPT/DOCT/001000 -JOB 001000 -ERR 001000_20011218093512.err -GRP N -TST TEST -PRT 001000-0 -DAT 5/12/2001 -JDE CLLU34 -JNM BPUT8485

PRE_MERGE_PROCESSING_PARAM_LST = [PARAM_DIR, PARAM_JOB, PARAM_ERR, PARAM_TST, PARAM_PRT, PARAM_DAT, PARAM_JNM]
PRE_MERGE_PROCESSING_OPTIONAL_PARAM_LST = [PARAM_JDE]

GROUP_PROCESSING_PARAM_LST = [PARAM_DIR, PARAM_LST, PARAM_ERR, PARAM_PRT]

JOINING_PARAM_LST = [PARAM_DIR, PARAM_ORA, PARAM_JOB, PARAM_ERR, PARAM_PRT, PARAM_LST]

RENDERING_PARAM_LST = [PARAM_DIR, PARAM_ORA, PARAM_JOB, PARAM_ERR, PARAM_IN, PARAM_OUT, PARAM_GRP]

REPRINT_PROCESSING_PARAM_LST = [PARAM_DIR, PARAM_JOB, PARAM_ERR, PARAM_PRT, PARAM_TYPE, PARAM_RPF, PARAM_RPT, PARAM_JNM, PARAM_MLA]
REPRINT_PROCESSING_OPTIONAL_PARAM_LST = [PARAM_JDE, PARAM_CFG, PARAM_FNO, PARAM_DAT, PARAM_LVL, PARAM_MEMO]

PRINTER_PARAM_LST = [PARAM_DIR, PARAM_JOB, PARAM_JNM, PARAM_ERR, PARAM_PRT]
PRINTER_OPTIONAL_PARAM_LST = [PARAM_PC, PARAM_TAR, PARAM_PDR, PARAM_HST, PARAM_PRQ, PARAM_FUN, PARAM_IPM, PARAM_FRM, PARAM_PID, PARAM_ORA, PARAM_FNM, PARAM_HC, PARAM_HFT, PARAM_JNM, PARAM_PR, PARAM_PRT, PARAM_OP, PARAM_MEMO, PARAM_DJNM ,PARAM_TMP, PARAM_OUT, PARAM_PTY]

POST_PRINT_PARAM_LST = [PARAM_DIR, PARAM_ORA, PARAM_JOB, PARAM_ERR, PARAM_CAN, PARAM_MLA, PARAM_OP, PARAM_PRQ, PARAM_HFT, PARAM_JNM, PARAM_PR, PARAM_PRT, PARAM_HC, PARAM_FNM]

PRINT_COMPLETION_PARAM_LST = [PARAM_TMP, PARAM_OUT, PARAM_ERR]
PRINT_COMPLETION_OPTIONAL_PARAM_LST = [PARAM_HST, PARAM_PC, PARAM_TAR, PARAM_PRT, PARAM_PRQ, PARAM_PRGP, PARAM_MAN, PARAM_SERVICE_CLASS, PARAM_PRINTER_TYPE, PARAM_NAME]

PRINTER_STATUS_PARAM_LST = [PARAM_TMP, PARAM_OUT, PARAM_ERR]
PRINTER_STATUS_OPTIONAL_PARAM_LST = [PARAM_HST, PARAM_TAR, PARAM_PRT, PARAM_PRGP, PARAM_PRQ, PARAM_SERVICE_CLASS, PARAM_PRINTER_TYPE, PARAM_NAME, PARAM_PC]

PRE_PRINT_QA_PARAM_LST = [PARAM_DIR, PARAM_JOB, PARAM_ERR, PARAM_PRT, PARAM_FNM, PARAM_HST, PARAM_ORA]
PRE_PRINT_QA_OPTIONAL_PARAM_LST = [PARAM_REL, PARAM_DES, PARAM_PPC]

MAILER_PARAM_LST = [PARAM_DIR, PARAM_JOB, PARAM_ERR, PARAM_IDF, PARAM_OP, PARAM_INT]
MAILER_OPTIONAL_PARAM_LST = [PARAM_TAR, PARAM_STS, PARAM_MXP, PARAM_MSD, PARAM_UPD, PARAM_HST2, PARAM_REP_UPD, PARAM_SEL_UPD]

POST_MAIL_PARAM_LST = [PARAM_DIR, PARAM_JOB, PARAM_ERR, PARAM_IDF, PARAM_TMP, PARAM_EXP, PARAM_TYP, PARAM_MLA, PARAM_OP, PARAM_MRG, PARAM_INT, PARAM_HST]
POST_MAIL_OPTIONAL_PARAM_LST = [PARAM_TAR, PARAM_STS, PARAM_MXP, PARAM_MSD, PARAM_UPD]

REPRINT_REQUEST_PARAM_LIST = [PARAM_DIR, PARAM_JOB, PARAM_ERR, PARAM_RFP, PARAM_IDF ]

DESPATCH_PARAM_LST = [PARAM_DIR, PARAM_JOB, PARAM_ERR, PARAM_PRT, PARAM_TYPE, PARAM_REP, PARAM_TEST, PARAM_DST, PARAM_PREFIX]

DELETION_PARAM_LST = [PARAM_DIR, PARAM_JOB, PARAM_ERR, PARAM_OUT]

class ParameterContainer:
    def __init__(self,InputArguments):
        self.__parametersDict = {}
        self.missingParametersDict = []
        self.overmuchParametersDict = []
        paramKey = None
        for param in InputArguments:
            if (paramKey is None) and (param[0]=="-") :
                paramKey = param
            else :
                if not paramKey is None:
                    self.__parametersDict[paramKey] = param
                    paramKey = None
        if not paramKey is None:
            self.__parametersDict[paramKey] = ''
            paramKey = None
        # Parse parameter file to get the list of parameters
        self.__parametersFileDict = None
        self.__extraParameters = None

    # !!!! Not a thread safe function : this function must be synchronized
    def initParameterFileDict(self):
        # PARAM_DIR
        # PARAM_ORA
        if self.__parametersFileDict is None:
            self.__parametersFileDict = {}
            self.__parametersParser = None
            jobId = self.getJobID()
            if jobId is not None:
                dirFile = self.getFullPathJobDir()
                if dirFile is not None:
                    xmlParFile = "%s/%s.par" % (str(dirFile),str(jobId))
                else:
                    xmlParFile = "%s.par" % (str(jobId))
                if not os.path.isfile(xmlParFile):
                    dirFile = self.getInputDir()
                    if dirFile is None:
                        # print("can't found parameter file in %s or %s" % (str(self.getFullPathJobDir()), str(self.getInputDir())))
                        return
                    xmlParFile = "%s/%s.par" % (str(dirFile),str(jobId))
                    if not os.path.isfile(xmlParFile):
                        # print("can't found parameter file %s" % (xmlParFile))
                        return
                self.__parametersParser = ParParser(self.__parametersFileDict, LoggingProducerUtils(self, log4py.LOGLEVEL_DEBUG, LOGGER_PRODUCER_LOG_DIR))
                self.__parametersParser.parse(self.__parametersParser, xmlParFile)
        
        
    # return the parametervalue from the parameter name               
    def getParamValue(self, paramKey):
        return self.__parametersDict.get(paramKey, None)
    
    def setExtraParameters(self, extraParameters):
        self.__extraParameters = extraParameters
        
     # this method verify that all main parameters are difined in __parametersDict and that all parameters in __parametersDict exists in mainParameters or optionalParameters
    def match(self, mainParameters, optionalParameters = None):
        # print"mainParameters",mainParameters
        # print"optionalParameters",optionalParameters
        # print"extraParameters",self.__extraParameters
        isMatched = True
        tmpParaDict = self.__parametersDict.copy()
        # print"************before**************"
        # for param in tmpParaDict.keys() :
        #     print"param1,",param
        #     print"value", tmpParaDict[param]
        # print"********************************"
        for param in mainParameters :
            try:
                # KeyError is raise if the param doesn't exist in tmpParaDict
                value = tmpParaDict[param]
                # print"param2",param
                # print"value",value
                del tmpParaDict[param]
            except KeyError:
                # print"problem1"
                isMatched = False
                self.missingParametersDict.append(param)
        # print"************after**************"
        # for param in tmpParaDict.keys() :
        #     print"param3,",param
        #     print"value", tmpParaDict[param]
        # print"********************************"
        
        if not tmpParaDict is None :
            if not (optionalParameters is None) :
                for param in optionalParameters :
                    if param in tmpParaDict.keys() :
                        # print"param4",param
                        # print"value",tmpParaDict[param]
                        del tmpParaDict[param]
                    else:
                        print"param not in optionalParameters :",param
            if not self.__extraParameters is None :
                    for param in self.__extraParameters :
                        if param in tmpParaDict.keys() :
                            # print"param5",param
                            # print"value",tmpParaDict[param]
                            del tmpParaDict[param]
                        # else:
                        #     print"param not in extraParameters :",param
            for param in tmpParaDict.keys() :
                # print"param not defined :",param
                # print"param6",param
                # print"value",tmpParaDict[param]
                del tmpParaDict[param]
                self.overmuchParametersDict.append(param)
                isMatched = False


            
        #if not optionalParameters is None :
        #    for param in tmpParaDict.keys() :
        #        try:
        #            if(param == extraParameters):
        #                    print"extraParameters1",extraParameters
        #            if(param != extraParameters):                            
        #                    # ValueError is raise if the param doesn't exist in optionalParameters
        #                    print"param2",param
        #                    print"value",value
        #                    value = optionalParameters.index(param)
                    
        #                    del tmpParaDict[param]
        #        except ValueError:
            #            print"problem2"
        #            isMatched = False
        #            self.overmuchParametersDict.append(param)
        
        #if not len(tmpParaDict) == 0:
            #print"problem3"
            #print "Some parameters are not defined for this type of scripts : "
            #self.overmuchParametersDict.append(tmpParaDict.keys())
            #isMatched = False
        return isMatched


    def matchReception(self):
        return self.match(RECEPTION_PARAM_LST,RECEPTION_OPTIONAL_PARAM_LST)
        
    def matchReceptionPlugIn(self):
        return self.match(RECEPTION_PLUGIN_PARAM_LST,RECEPTION_PLUGIN_OPTIONAL_PARAM_LST)


    def matchProcessing(self):
        return self.match(PROCESSING_PARAM_LST, PROCESSING_OPTIONAL_PARAM_LST)

    def matchPreMergeProcessing(self):
        return self.match(PRE_MERGE_PROCESSING_PARAM_LST, PRE_MERGE_PROCESSING_OPTIONAL_PARAM_LST)

    def matchGroupProcessing(self):
        return self.match(GROUP_PROCESSING_PARAM_LST)

    def matchJoining(self):
        return self.match(JOINING_PARAM_LST)

    def matchRendering(self):
        return self.match(RENDERING_PARAM_LST)

    def matchReprintProcessing(self):
        return self.match(REPRINT_PROCESSING_PARAM_LST,REPRINT_PROCESSING_OPTIONAL_PARAM_LST)
        
    def matchPrinter(self):
        return self.match(PRINTER_PARAM_LST,PRINTER_OPTIONAL_PARAM_LST)    

    def matchPrintCompletion(self):
        return self.match(PRINT_COMPLETION_PARAM_LST,PRINT_COMPLETION_OPTIONAL_PARAM_LST)    

    def matchPrinterStatus(self):
        return self.match(PRINTER_STATUS_PARAM_LST,PRINTER_STATUS_OPTIONAL_PARAM_LST)

    def matchPostPrint(self):
        return self.match(POST_PRINT_PARAM_LST) 

    def matchPrePrintQA(self):
        return self.match(PRE_PRINT_QA_PARAM_LST,PRE_PRINT_QA_OPTIONAL_PARAM_LST) 

    def matchMailer(self):
        return self.match(MAILER_PARAM_LST,MAILER_OPTIONAL_PARAM_LST)    

    def matchPostMail(self):
        return self.match(POST_MAIL_PARAM_LST,POST_MAIL_OPTIONAL_PARAM_LST)

    def matchReprintRequest(self):
        return self.match(REPRINT_REQUEST_PARAM_LIST) 

    def matchDespatch(self):
        return self.match(DESPATCH_PARAM_LST,None) 

    def matchDeletion(self):
        return self.match(DELETION_PARAM_LST) 
    
    # Common properties used for logging, error or return management
    def getFullPathJobDir(self):
        return self.getParamValue(PARAM_DIR)
                
    def getErrorFileName(self):
        return self.getParamValue(PARAM_ERR)
    
    def getJobID(self):
        return self.getParamValue(PARAM_JOB)
        
    def getInputDir(self):
        input = self.getParamValue(PARAM_ORA)
        if input == None:
            input = self.getFullPathJobDir()
        return input
        
    def getParametersFileParser(self):
        self.initParameterFileDict()
        return self.__parametersParser, self.__parametersFileDict


    # log the list of parameters of a script type
    # the script type com from parameters list
    def logAllParameters(self, logger, mainParameters, optionalParameters = None):
        for param in mainParameters :
            # CHANGING TO DEBUG USING log4py
            logger.info ( "%s = %s" % ( param, self.getParamValue(param)))
        if optionalParameters is not None:
            for param in optionalParameters :
                # CHANGING TO INFO USING log4py
                logger.info ( "%s = %s" % ( param, self.getParamValue(param)))

    ##############################################################
    # Get current JOB parameters
    ##############################################################
    def getJobParameters(self):
        self.initParameterFileDict()
        return self.__parametersParser.getJobParameters()
    
    ##############################################################
    # Get current ANADATA parameters
    ##############################################################
    def getAnadataParameters(self):
        self.initParameterFileDict()
        return self.__parametersParser.getAnadataParameters()
    
    ##############################################################
    # Get current REMAKE parameters
    ##############################################################
    def getRemakeParameters(self):
        self.initParameterFileDict()
        return self.__parametersParser.getRemakeParameters()     #IGNORE:E1101
    
    ##############################################################
    # Get current ADF_SPLIT parameters
    ##############################################################
    def getAdfSplitParameters(self):
        self.initParameterFileDict()
        return self.__parametersParser.getAdfSplitParameters()
    
    ##############################################################
    # Get current list of input files parameters
    ##############################################################
    def getInputFilesParameters(self):
        self.initParameterFileDict()
        return self.__parametersParser.getInputFilesParameters()
    
    ##############################################################
    # Get current list of output files parameters
    ##############################################################
    def getOutputFilesParameters(self):
        self.initParameterFileDict()
        return self.__parametersParser.getOutputFilesParameters()

    ##############################################################
    # Get current list of stock codes parameters
    ##############################################################
    def getStockCodesParameters(self):
        self.initParameterFileDict()
        return self.__parametersParser.getStockCodesParameters()
    
    def getExtraParameter(self, parameterName):
        resu = self.getParamValue(parameterName)
        if resu is None:
            self.initParameterFileDict()
            resu = self.__parametersParser.getExtraParameters(parameterName) #IGNORE:E1101
            if resu is None:
                resu = os.environ.get(parameterName, None)
        return resu
   
# Parameter Exception is used to managed Error in parameteres
# Those error can be due to concistancy, missing parameter or overmuch parameter
class ParameterException(Exception):
    
    def __init__(self, exceptionType, detailErrorParam):
        Exception.__init__(self,exceptionType)
        self.__exceptionType = exceptionType
        self.__detailErrorParam = detailErrorParam
   
    def getErrorDetail(self):
        resu = []
        resu.append(self.__exceptionType)
        resu.append('\n')
        if not self.__detailErrorParam is None:
            if self.__exceptionType == "MatchingError":
                missing = self.__detailErrorParam[0]
                if not missing is None and len(missing) > 0 :
                    resu.append(" \nmissing arguments list = ")
                    resu.append(str(missing))
                overmuch = self.__detailErrorParam[1]
                if not overmuch is None and len(overmuch) > 0 :
                    resu.append(" \nunexpected arguments list = ")
                    resu.append(str(overmuch))
        return ''.join(resu)


# Reception Script parameters class to help Reception Script Development
class ReceptionParameter(ParameterContainer):
    def __init__(self,inputArguments):
        ParameterContainer.__init__(self,inputArguments)
        
    def validateParameters(self):
        ok = self.matchReception()
        if not ok:
            raise ParameterException("MatchingError", [self.missingParametersDict, self.overmuchParametersDict])
        
    def getTMP(self):
        return self.getParamValue(PARAM_TMP)

    def logAllParameters(self, logger):
        ParameterContainer.logAllParameters(self,logger,RECEPTION_PARAM_LST, RECEPTION_OPTIONAL_PARAM_LST)

# Reception Script parameters class to help Reception Script Development
class ReceptionPlugInParameter(ParameterContainer):
    def __init__(self,inputArguments):
        ParameterContainer.__init__(self,inputArguments)
        
    def validateParameters(self):
        ok = self.matchReceptionPlugIn()
        if not ok:
            raise ParameterException("MatchingError", [self.missingParametersDict, self.overmuchParametersDict])
        
    def getTFR(self):
        return self.getParamValue(PARAM_TFR)

    def getSRH(self):
        return self.getParamValue(PARAM_SRH)

    def getDEL(self):
        return self.getParamValue(PARAM_DEL)

    def logAllParameters(self, logger):
        ParameterContainer.logAllParameters(self,logger,RECEPTION_PLUGIN_PARAM_LST, RECEPTION_PLUGIN_OPTIONAL_PARAM_LST)

# Processing Script parameters class to Help Processing Script Development
class ProcessingParameter(ParameterContainer):
    def __init__(self,inputArguments):
        ParameterContainer.__init__(self,inputArguments)
        
    def validateParameters(self):
        ok = self.matchProcessing()
        if not ok:
            raise ParameterException("MatchingError", [self.missingParametersDict, self.overmuchParametersDict])
        
    def getGroupFlag(self):
        return self.getParamValue(PARAM_GRP)
        
    def getTestFlag(self):
        return self.getParamValue(PARAM_TST)
        
    def getPrintFileName(self):
        return self.getParamValue(PARAM_PRT)
        
    def getDateJobReceive(self):
        return self.getParamValue(PARAM_DAT)
        
    def getJdeMember(self):
        return self.getParamValue(PARAM_JDE)
        
    def getJobName(self):
        return self.getParamValue(PARAM_JNM)
        
    def getHost(self):
        return self.getParamValue(PARAM_HST)
        
    def getOMR(self):
        return self.getParamValue(PARAM_OMR)
    
    def getREG(self):
        return self.getParamValue(PARAM_REG)
        
    def logAllParameters(self, logger):
        ParameterContainer.logAllParameters(self,logger,PROCESSING_PARAM_LST, PROCESSING_OPTIONAL_PARAM_LST)


#******************New Dispatch Class Begins
class DispatchParameter(ParameterContainer):
    def __init__(self,inputArguments):
        ParameterContainer.__init__(self,inputArguments)
        
    def validateParameters(self):
        ok = self.matchDespatch()
        if not ok:
            raise ParameterException("MatchingError", [self.missingParametersDict, self.overmuchParametersDict])
        
    def getTestFlag(self):
        return self.getParamValue(PARAM_TEST)
        
    def getPrintFileName(self):
        return self.getParamValue(PARAM_PRT)

    def getDispatchDestination(self):
        return self.getParamValue(PARAM_DST)

    def getReprintCount(self):
        return self.getParamValue(PARAM_REP)
    
    def getFilePrefix(self):
        return self.getParamValue(PARAM_PREFIX)
 
    def getType(self):
        return self.getParamValue(PARAM_TYPE)
    
    def logAllParameters(self, logger):
        ParameterContainer.logAllParameters(self,logger,DESPATCH_PARAM_LST)
        
#******************************************New Dispatch Interface class Ends

# Reprint Processing Script parameters class to Help Reprint Processing Script Development
class ReprintProcessingParameter(ParameterContainer):
    def __init__(self,inputArguments):
        ParameterContainer.__init__(self,inputArguments)
        
    def validateParameters(self):
        ok = self.matchReprintProcessing()
        if not ok:
            raise ParameterException("MatchingError", [self.missingParametersDict, self.overmuchParametersDict])
        
        
    def getType(self):
        return self.getParamValue(PARAM_TYPE)
        
    def getPrintFileName(self):
        return self.getParamValue(PARAM_PRT)
        
    def getREPT(self):
        return self.getParamValue(PARAM_RPT)

    def getREPF(self):
        return self.getParamValue(PARAM_RPF)
        
    def getJdeMember(self):
        return self.getParamValue(PARAM_JDE)
        
    def getJobName(self):
        return self.getParamValue(PARAM_JNM)
        
    def getCFG(self):
        return self.getParamValue(PARAM_CFG)

    def getMLA(self):
        return self.getParamValue(PARAM_MLA)

    def getFNO(self):
        return self.getParamValue(PARAM_FNO)

        
    def logAllParameters(self, logger):
        ParameterContainer.logAllParameters(self,logger,REPRINT_PROCESSING_PARAM_LST, REPRINT_PROCESSING_OPTIONAL_PARAM_LST)



# Pre Merge Processing Script parameters class to Help Pre Merge Processing Script Development
class PreMergeProcessingParameter(ParameterContainer):
    def __init__(self,inputArguments):
        ParameterContainer.__init__(self,inputArguments)
        
    def validateParameters(self):
        ok = self.matchPreMergeProcessing()
        if not ok:
            raise ParameterException("MatchingError", [self.missingParametersDict, self.overmuchParametersDict])
        
    def getGroupFlag(self):
        return self.getParamValue(PARAM_GRP)
        
    def getTestFlag(self):
        return self.getParamValue(PARAM_TST)
        
    def getPrintFileName(self):
        return self.getParamValue(PARAM_PRT)
        
    def getDateJobReceive(self):
        return self.getParamValue(PARAM_DAT)
        
    def getJdeMember(self):
        return self.getParamValue(PARAM_JDE)
        
    def getJobName(self):
        return self.getParamValue(PARAM_JNM)
        
    def getHost(self):
        return self.getParamValue(PARAM_HST)
        
    def logAllParameters(self, logger):
        ParameterContainer.logAllParameters(self,logger,PROCESSING_PARAM_LST, PROCESSING_OPTIONAL_PARAM_LST)

# Printer Script parameters class to Help Printer Script Development
class PrinterParameter(ParameterContainer):
    def __init__(self,inputArguments):
        ParameterContainer.__init__(self,inputArguments)
        
    def validateParameters(self):
        ok = self.matchPrinter()
        if not ok:
            raise ParameterException("MatchingError", [self.missingParametersDict, self.overmuchParametersDict])
        
    def getJNM(self):
        return self.getParamValue(PARAM_JNM)
        
    def getPrintFileName(self):
        return self.getParamValue(PARAM_PRT)
        
    def getPDR(self):
        return self.getParamValue(PARAM_PDR)

    def getOutputDirectory(self):
        return self.getParamValue(PARAM_TAR)

    def getHST(self):
        return self.getParamValue(PARAM_HST)

    def getPRQ(self):
        return self.getParamValue(PARAM_PRQ)

    def getFUN(self):
        return self.getParamValue(PARAM_FUN)

    def getIPM(self):
        return self.getParamValue(PARAM_IPM)

    def getFRM(self):
        return self.getParamValue(PARAM_FRM)

    def getPID(self):
        return self.getParamValue(PARAM_PID)

    def getHC(self):
        return self.getParamValue(PARAM_HC)

    def getHFT(self):
        return self.getParamValue(PARAM_HFT)

    def getPrinterName(self):
        return self.getParamValue(PARAM_PR)

    def getOperatorName(self):
        return self.getParamValue(PARAM_OP)

    def getPC(self):
        return self.getParamValue(PARAM_PC)

    def getTMP(self):
        return self.getParamValue(PARAM_TMP)

    def getOUT(self):
        return self.getParamValue(PARAM_OUT)
    
    def getPTY(self):
        return self.getParamValue(PARAM_PTY)

    def logAllParameters(self, logger):
        ParameterContainer.logAllParameters(self,logger,PRINTER_PARAM_LST, PRINTER_OPTIONAL_PARAM_LST)

# Print Completion Script parameters class to Help Print Completion Script Development
class PrintCompletionParameter(ParameterContainer):
    def __init__(self,inputArguments):
        ParameterContainer.__init__(self,inputArguments)
        
    def validateParameters(self):
        ok = self.matchPrintCompletion()
        if not ok:
            raise ParameterException("MatchingError", [self.missingParametersDict, self.overmuchParametersDict])
        
        
    def getPRT(self):
        return self.getParamValue(PARAM_PRT)

    def getPRQ(self):
        return self.getParamValue(PARAM_PRQ)
        
    def getPRGP(self):
        return self.getParamValue(PARAM_PRGP)

    def getOUT(self):
        return self.getParamValue(PARAM_OUT)

    def getTMP(self):
        return self.getParamValue(PARAM_TMP)

    def getHST(self):
        return self.getParamValue(PARAM_HST)

    def getTAR(self):
        return self.getParamValue(PARAM_TAR)

    def getPC(self):
        return self.getParamValue(PARAM_PC)

    def getMAN(self):
        return self.getParamValue(PARAM_MAN)

    def logAllParameters(self, logger):
        ParameterContainer.logAllParameters(self,logger,PRINT_COMPLETION_PARAM_LST, PRINT_COMPLETION_OPTIONAL_PARAM_LST)

# PrinterStatus Script parameters class to Help Printer Status  Script Development
class PrinterStatusParameter(ParameterContainer):
    def __init__(self,inputArguments):
        ParameterContainer.__init__(self,inputArguments)
        
    def validateParameters(self):
        ok = self.matchPrinterStatus()
        if not ok:
            raise ParameterException("MatchingError", [self.missingParametersDict, self.overmuchParametersDict])
        
        
    def getPRT(self):
        return self.getParamValue(PARAM_PRT)

    def getPRQ(self):
        return self.getParamValue(PARAM_PRQ)
        
    def getPRGP(self):
        return self.getParamValue(PARAM_PRGP)

    def getOUT(self):
        return self.getParamValue(PARAM_OUT)

    def getTMP(self):
        return self.getParamValue(PARAM_TMP)

    def getHST(self):
        return self.getParamValue(PARAM_HST)

    def getNAME(self):
        return self.getParamValue(PARAM_NAME)


    def logAllParameters(self, logger):
        ParameterContainer.logAllParameters(self,logger,PRINTER_STATUS_PARAM_LST, PRINTER_STATUS_OPTIONAL_PARAM_LST)




# Post Print Script parameters class to Help Post Print Script Development
class PostPrintParameter(ParameterContainer):
    def __init__(self,inputArguments):
        ParameterContainer.__init__(self,inputArguments)
        
    def validateParameters(self):
        ok = self.matchPostPrint()
        if not ok:
            raise ParameterException("MatchingError", [self.missingParametersDict, self.overmuchParametersDict])
        
    def getCAN(self):
        return self.getParamValue(PARAM_CAN)
        
    def getMLA(self):
        return self.getParamValue(PARAM_MLA)
        
    def logAllParameters(self, logger):
        ParameterContainer.logAllParameters(self,logger,POST_PRINT_PARAM_LST, None)

# Mailing Script parameters class to Help Mailing Script Development
class MailingParameter(ParameterContainer):
    def __init__(self,inputArguments):
        ParameterContainer.__init__(self,inputArguments)
        
    def validateParameters(self):
        ok = self.matchMailer()
        if not ok:
            raise ParameterException("MatchingError", [self.missingParametersDict, self.overmuchParametersDict])
        
    def getIDF(self):
        return self.getParamValue(PARAM_IDF)
        
    def getOP(self):
        return self.getParamValue(PARAM_OP)

    def getINT(self):
        return self.getParamValue(PARAM_INT)

    def getTAR(self):
        return self.getParamValue(PARAM_TAR)

    def getSTS(self):
        return self.getParamValue(PARAM_STS)

    def getMXP(self):
        return self.getParamValue(PARAM_MXP)

    def getMSD(self):
        return self.getParamValue(PARAM_MSD)

    def getUPD(self):
        return self.getParamValue(PARAM_UPD)
        
    def logAllParameters(self, logger):
        ParameterContainer.logAllParameters(self,logger,MAILER_PARAM_LST, MAILER_OPTIONAL_PARAM_LST)

# Post Mailing Script parameters class to Help Post Mailing Script Development
class PostMailingParameter(ParameterContainer):
    def __init__(self,inputArguments):
        ParameterContainer.__init__(self,inputArguments)
        
    def validateParameters(self):
        ok = self.matchPostMail()
        if not ok:
            raise ParameterException("MatchingError", [self.missingParametersDict, self.overmuchParametersDict])
        
    def getIDF(self):
        return self.getParamValue(PARAM_IDF)

    def getTMP(self):
        return self.getParamValue(PARAM_TMP)
        
    def getEXP(self):
        return self.getParamValue(PARAM_EXP)

    def getTYP(self):
        return self.getParamValue(PARAM_TYP)

    def getMLA(self):
        return self.getParamValue(PARAM_MLA)

    def getOP(self):
        return self.getParamValue(PARAM_OP)

    def getMRG(self):
        return self.getParamValue(PARAM_MRG)

    def getINT(self):
        return self.getParamValue(PARAM_INT)

    def getHST(self):
        return self.getParamValue(PARAM_HST)

    def getTAR(self):
        return self.getParamValue(PARAM_TAR)

    def getSTS(self):
        return self.getParamValue(PARAM_STS)
        
    def getMXP(self):
        return self.getParamValue(PARAM_MXP)

    def getMSD(self):
        return self.getParamValue(PARAM_MSD)

    def getUPD(self):
        return self.getParamValue(PARAM_UPD)

    def logAllParameters(self, logger):
        ParameterContainer.logAllParameters(self,logger,POST_MAIL_PARAM_LST, POST_MAIL_OPTIONAL_PARAM_LST)

# Groupring Processing Script parameters class to Help Reprint Processing Script Development
class GroupingProcessingParameter(ParameterContainer):
    def __init__(self,inputArguments):
        ParameterContainer.__init__(self,inputArguments)
        
    def validateParameters(self):
        ok = self.matchGroupProcessing()
        if not ok:
            raise ParameterException("MatchingError", [self.missingParametersDict, self.overmuchParametersDict])
        
    def getListJobFile(self):
        return self.getParamValue(PARAM_LST)
        
    def getPrintFileName(self):
        return self.getParamValue(PARAM_PRT)
        
    def logAllParameters(self, logger):
        ParameterContainer.logAllParameters(self,logger,GROUP_PROCESSING_PARAM_LST, None)

# Joining Script parameters class to Help Joining Script Development
class JoiningParameter(ParameterContainer):
    def __init__(self,inputArguments):
        ParameterContainer.__init__(self,inputArguments)
        
    def validateParameters(self):
        ok = self.matchJoining()
        if not ok:
            raise ParameterException("MatchingError", [self.missingParametersDict, self.overmuchParametersDict])
        
    def getOutVpfFileName(self):
        return self.getParamValue(PARAM_PRT)
        
    def getListJobFile(self):
        return self.getParamValue(PARAM_LST)
        
    def logAllParameters(self, logger):
        ParameterContainer.logAllParameters(self,logger,JOINING_PARAM_LST, None)

# Rendering Script parameters class to Help Rendering Script Development
class RenderingParameter(ParameterContainer):
    def __init__(self,inputArguments):
        ParameterContainer.__init__(self,inputArguments)
        
    def validateParameters(self):
        ok = self.matchRendering()
        if not ok:
            raise ParameterException("MatchingError", [self.missingParametersDict, self.overmuchParametersDict])
        
    def getInputFileName(self):
        return self.getParamValue(PARAM_IN)
        
    def getOutPutFileName(self):
        return self.getParamValue(PARAM_OUT)
        
    def getGroupFlag(self):
        return self.getParamValue(PARAM_GRP)
        
    def logAllParameters(self, logger):
        ParameterContainer.logAllParameters(self,logger,RENDERING_PARAM_LST, None)

# Deletion Script parameters class to Help Deletion Script Development
class DeletionParameter(ParameterContainer):
    def __init__(self,inputArguments):
        ParameterContainer.__init__(self,inputArguments)
        
    def validateParameters(self):
        ok = self.matchDeletion()
        if not ok:
            raise ParameterException("MatchingError", [self.missingParametersDict, self.overmuchParametersDict])
        
    def logAllParameters(self, logger):
        ParameterContainer.logAllParameters(self,logger,DELETION_PARAM_LST, None)

# Pre Print Script parameters class to Help Pre Print Script Development
class PrePrintQAParameter(ParameterContainer):
    def __init__(self,inputArguments):
        ParameterContainer.__init__(self,inputArguments)
        
    def validateParameters(self):
        ok = self.matchPrePrintQA()
        if not ok:
            raise ParameterException("MatchingError", [self.missingParametersDict, self.overmuchParametersDict])
        
    def getCAN(self):
        return self.getParamValue(PARAM_CAN)
        
    def getMLA(self):
        return self.getParamValue(PARAM_MLA)
        
    def logAllParameters(self, logger):
        ParameterContainer.logAllParameters(self,logger,POST_PRINT_PARAM_LST, None)

# Reprint have also associated parameter file where information depend on PARAM_TYP
"""
There will also be a parameter file <Job ID>.par containing Printing Requirements, Mailing Requirements and Stock Code information.

1.3.1.  -TYPE = INT (Interrupt)

Reprint Script should use:

 -<-REPT Parameter>.refp
 -<-REPT Parameter>.vpf
 -<-REPT Parameter>.vpf.ind

To create:

 -<-REPT Parameter>.lis.

                The -REPF Parameter will always be 0 for Interrupt reprints

1.3.2.  -TYPE = REC (Reconcilliation)

Reprint Script should use:

-<-REPF Parameter>.refm
-<-REPF Parameter>.vpf

To create :

-<-REPT Parameter>.vpf
-<-REPT Parameter>.vpf.ind
-<-REPT Parameter>.lis

                For automatic reconcilliation (due to Mailer Sub system reporting mailpieces need printing) then -REPF will always be one less than -REPT.

                For manual reconcilliation (due to Operator action) -REPF can be any value that is less than -REPT.

The -CFG parameter is used to determine what output protocol to use

1.3.3.  Return File

The .ret file produced should be in the same format as the .ret file for the Processing Script. There will only ever be one FILE in the OUTPUTFILELIST. FILENUMBER should be set to the Output File Number obtained from -PRT value.
"""

if __name__ == '__main__':
    parameters = ParameterContainer([1,2,3])

