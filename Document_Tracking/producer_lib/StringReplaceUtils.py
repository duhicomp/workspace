#!/usr/bin/env python

# This package provide utiles functions for string manipulation
# Especially to replace variable of format ${var_name} in a string

"""
The 3 main functions are : 
    replaceStringToString(inputString, varDict, varFormat=0):
    replaceFileToString(inputFile, varDict, varFormat=0):
    replaceFileToFile(inputFile, outputFile, varDict, varFormat=0):

an example of how to use them is on the __main__
    
"""

FORMAT_DEFAULT=0                # variable delimiter is : ${varName} (format used for the setup of producer)
FORMAT_ENGINE_ENVIRONEMENT=1    # variable delimiter is : $varName$ (format used in the propertie file of EngineStarter used by MiddleOffice / FrontOffice / Projector ...) 
FORMAT_ENGINE_PARAMETER=2       # variable delimiter is : %varName% or <varName> or  >varName< (format used in the propertie file of EngineStarter used by MiddleOffice / FrontOffice / Projector ...) 
FORMAT_TECHPRINT_VARIABLE=3     # variable delimiter is : "varName"  (format used in Techprint textes for variable name) 

"""
formatKey : generic function for variable type definition
    varDict : is the dictionary of the variables {'varName':'varValue', ..., 'varNameN':'varValueN'}
    delimiterList : is a table of table to define the liste of delimiters for variables [[StartDelimiter,EndDelimiter], ..., [StartDelimiterN,EndDelimiterN]]
    this function return the dictonary formated with the variables delimiters
"""
def _formatKey(varDict,delimiterList):
    resu = {}
    for key in varDict.keys():
        for delimiter in delimiterList:
            resu[delimiter[0]+key+delimiter[1]]=varDict[key]
    return resu

"""
formatKeyDefault : define the default Format type
    varDict : is the dictionary of the variables {'varName':'varValue', ..., 'varNameN':'varValueN'}
    this function return the dictonary formated with the variables delimiters

        FORMAT_DEFAULT               # variable delimiter is : ${varName} 
        (format used for the setup of producer)
"""
def _formatKeyDefault(varDict):
    return _formatKey(varDict,[['${','}']])

"""
formatKeyEnvEngineProp : define the Format for Engine Propertie Environement type
    varDict : is the dictionary of the variables {'varName':'varValue', ..., 'varNameN':'varValueN'}
    this function return the dictonary formated with the variables delimiters
        FORMAT_ENGINE_ENVIRONEMENT   # variable delimiter is : $varName$ 
        (format used in the propertie file of EngineStarter used by MiddleOffice / FrontOffice / Projector ...) 
"""
def _formatKeyEnvEngineProp(varDict):
    return _formatKey(varDict,[['$','$']])

"""
formatKeyParEngineProp : define the Format for Engine Propertie Parameters type
    varDict : is the dictionary of the variables {'varName':'varValue', ..., 'varNameN':'varValueN'}
    this function return the dictonary formated with the variables delimiters
        FORMAT_ENGINE_PARAMETER      # variable delimiter is : %varName% or <varName> or  >varName< 
        (format used in the propertie file of EngineStarter used by MiddleOffice / FrontOffice / Projector ...) 
"""
def _formatKeyParEngineProp(varDict):
    return _formatKey(varDict,[['%','%'],['<','>'],['>','<']])
"""
formatKeyVarTechprint : define the Format for Techprint variables
    varDict : is the dictionary of the variables {'varName':'varValue', ..., 'varNameN':'varValueN'}
    this function return the dictonary formated with the variables delimiters
        FORMAT_TECHPRINT_VARIABLE    # variable delimiter is : "varName"  
        (format used in Techprint textes for variable name) 
"""
def _formatKeyVarTechprint(varDict):
    return _formatKey(varDict,[['"','"']])

def _getRegex(mydict): 
    """ Replace in 'text' all occurences of any key in the given
    dictionary by its corresponding value.  Returns the new tring.""" 
    import re
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, mydict.keys())))
    return regex

def _getMoLambda(mydict):
    return lambda mo: mydict[mo.string[mo.start():mo.end()]]
    
def _getReplacedText(mydict, mytext): 
    return _getReplace(_getRegex(mydict), _getMoLambda(mydict), mytext)

def _getReplace(regex, moLambda, mytext):
    # For each match, look-up corresponding value in dictionary
    return regex.sub(moLambda, mytext) 

"""
replaceStringToString : replace the variable of type "varFormat" in the String "inputString" return a string with the result.
    inputString : the input String where variables must be replaced
    varDict : is the dictionary of the variables {'varName':'varValue', ..., 'varNameN':'varValueN'}
    varFormat : is the format of the variables in the file. 
        FORMAT_DEFAULT               # variable delimiter is : ${varName} (format used for the setup of producer)
        FORMAT_ENGINE_ENVIRONEMENT   # variable delimiter is : $varName$ (format used in the propertie file of EngineStarter used by MiddleOffice / FrontOffice / Projector ...) 
        FORMAT_ENGINE_PARAMETER      # variable delimiter is : %varName% or <varName> or  >varName< (format used in the propertie file of EngineStarter used by MiddleOffice / FrontOffice / Projector ...) 
        FORMAT_TECHPRINT_VARIABLE    # variable delimiter is : "varName"  (format used in Techprint textes for variable name) 
"""
def replaceStringToString(inputString, varDict, varFormat=0):
    if varFormat == FORMAT_ENGINE_ENVIRONEMENT:
        formatedDict = _formatKeyEnvEngineProp(varDict)
    elif varFormat == FORMAT_ENGINE_PARAMETER:
        formatedDict = _formatKeyParEngineProp(varDict)
    elif varFormat == FORMAT_TECHPRINT_VARIABLE:
        formatedDict = _formatKeyVarTechprint(varDict)
    else:
        formatedDict = _formatKeyDefault(varDict)
    fileChangeContent = _getReplacedText(formatedDict,inputString)
    return fileChangeContent
    
"""
replaceFileToString : replace the variable of type "varFormat" in the file "inputFileName" return a string with the result.
    inputFileName : the input file name where variables must be replaced
    varDict : is the dictionary of the variables {'varName':'varValue', ..., 'varNameN':'varValueN'}
    varFormat : is the format of the variables in the file. 
        FORMAT_DEFAULT               # variable delimiter is : ${varName} (format used for the setup of producer)
        FORMAT_ENGINE_ENVIRONEMENT   # variable delimiter is : $varName$ (format used in the propertie file of EngineStarter used by MiddleOffice / FrontOffice / Projector ...) 
        FORMAT_ENGINE_PARAMETER      # variable delimiter is : %varName% or <varName> or  >varName< (format used in the propertie file of EngineStarter used by MiddleOffice / FrontOffice / Projector ...) 
        FORMAT_TECHPRINT_VARIABLE    # variable delimiter is : "varName"  (format used in Techprint textes for variable name) 
"""
def replaceFileToString(inputFileName, varDict, varFormat=0):
    fIn = open(inputFileName)
    fileContent = ''.join(fIn.readlines())
    fIn.close()
    fileChangeContent = replaceStringToString(fileContent,varDict,varFormat)
    return fileChangeContent

"""
replaceFileToFile : replace the variable of type "varFormat" in the file "inputFileName" and write the result in the file "outputFileName".
    outputFileName : the output file name where the result of the replacement must be written
    inputFileName : the input file name where variables must be replaced
    varDict : is the dictionary of the variables {'varName':'varValue', ..., 'varNameN':'varValueN'}
    varFormat : is the format of the variables in the file. 
        FORMAT_DEFAULT               # variable delimiter is : ${varName} (format used for the setup of producer)
        FORMAT_ENGINE_ENVIRONEMENT   # variable delimiter is : $varName$ (format used in the propertie file of EngineStarter used by MiddleOffice / FrontOffice / Projector ...) 
        FORMAT_ENGINE_PARAMETER      # variable delimiter is : %varName% or <varName> or  >varName< (format used in the propertie file of EngineStarter used by MiddleOffice / FrontOffice / Projector ...) 
        FORMAT_TECHPRINT_VARIABLE    # variable delimiter is : "varName"  (format used in Techprint textes for variable name) 
"""
def replaceFileToFile(outputFileName, inputFileName, varDict, varFormat=0):
    fileChangeContent = replaceFileToString(inputFileName,varDict,varFormat)
    fOut = open(outputFileName,"wb")
    fOut.writelines(fileChangeContent)
    fOut.close()
    
if __name__ == '__main__':
    tstString = []
    tstString.append('Text with default variable type : ${myVar1} ${myVar2}')
    tstString.append('Text with Engine Environement variable type : $myVar1$ $myVar2$')
    tstString.append('Text with Techprint Variables variable type : "myVar1" "myVar2"')
    tstString.append('Text with Engine Parameter variable type : %myVar1% <myVar2> >myVar3<')
    
    tstFileInName = 'StringReplaceUtil_in.tst'
    tstFileOutName = 'StringReplaceUtil_out.tst'
    
    tstString = '\n'.join(tstString)
    
    f = open(tstFileInName,'wb')
    f.writelines(tstString)
    f.close()
    
    tstDict = {'myVar1':'@@val1@@', 'myVar2':'@@val2@@', 'myVar3':'@@val3@@'}
    
    print 'Replace var in String to String : ',str(tstString)
    print 'Replace default ${varName} Var Format : ',replaceStringToString(str(tstString),tstDict,FORMAT_DEFAULT)
    print 'Replace Environment $varName$ Var Format : ',replaceStringToString(str(tstString),tstDict,FORMAT_ENGINE_ENVIRONEMENT)
    print 'Replace Variable "varName" Var Format : ',replaceStringToString(str(tstString),tstDict,FORMAT_TECHPRINT_VARIABLE)
    print 'Replace Parameter %varName% Var Format : ',replaceStringToString(str(tstString),tstDict,FORMAT_ENGINE_PARAMETER)

    tstRepaceStr = replaceStringToString(str(tstString),tstDict,FORMAT_DEFAULT)
    tstRepaceStr = replaceStringToString(tstRepaceStr,tstDict,FORMAT_ENGINE_ENVIRONEMENT)
    tstRepaceStr = replaceStringToString(tstRepaceStr,tstDict,FORMAT_TECHPRINT_VARIABLE)
    print 'Replace All Var Format : ',replaceStringToString(tstRepaceStr,tstDict,FORMAT_ENGINE_PARAMETER)
    
    import os.path
    print 'Replace var in File to String : ',os.path.abspath(tstFileInName)
    print 'Replace Parameter %varName% Var Format : ',replaceFileToString(str(tstFileInName),tstDict,FORMAT_ENGINE_PARAMETER)
        
    print 'Replace var in File to File : ',os.path.abspath(tstFileInName)
    'Replace Parameter %varName% Var Format : ',replaceFileToFile(str(tstFileOutName),str(tstFileInName),tstDict,FORMAT_ENGINE_PARAMETER)
    print ' to ',os.path.abspath(tstFileOutName), ' Done'
