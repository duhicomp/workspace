#!/usr/bin/env python

# This package provide utilities functions for time manipulation

"""
The main functions is : 
    changeTimeZone(inputTime, timeZone):

an example of how to use them is on the __main__
    
"""

import datetime,os,time

"""
changeTimeZone: convert an inputTime from the localTimeZone to the timeZone specified in parameter
    inputTime : time in the localTimeZone in format YYYYMMDDHHMMSS e.g. 20110524110155
    timeZone : name of the timeZone of the result e.g "America/Indianapolis"
    the result is in the same format than input YYYYMMDDHHMMSS
"""
def changeTimeZone(inputTime, timeZone):
    
    localTz = os.environ.get('TZ')
    localTzname=time.tzname
    localTime = datetime.datetime.strptime(inputTime, "%Y%m%d%H%M%S")
    localOffset = time.timezone
    os.environ['TZ'] = timeZone
    time.tzset()
    remoteOffset = time.timezone
    remoteTime = localTime + datetime.timedelta(0,localOffset-remoteOffset)
    if localTz != None:
        os.environ['TZ'] = localTz
    else:
        os.environ['TZ'] = localTzname[0]
    time.tzset()
    if localOffset != time.timezone:
        print "Error wrong initial offset restoration : %d != %d" % (localOffset, time.timezone)
    return remoteTime

def changeTimeZoneCheck(inputTime, timeZone):
    print "%s = %s -> %s" % (changeTimeZone(inputTime,timeZone), inputTime, timeZone)

if __name__ == '__main__':
    changeTimeZoneCheck("20110524110155","America/Indianapolis")
    changeTimeZoneCheck("20110524110155","UTC-11")
    changeTimeZoneCheck("20110524110155","UTC-10")
    changeTimeZoneCheck("20110524110155","UTC-9")
    changeTimeZoneCheck("20110524110155","UTC-8")
    changeTimeZoneCheck("20110524110155","UTC-7")
    changeTimeZoneCheck("20110524110155","UTC-6")
    changeTimeZoneCheck("20110524110155","UTC-5")
    changeTimeZoneCheck("20110524110155","UTC-4")
    changeTimeZoneCheck("20110524110155","UTC-3")
    changeTimeZoneCheck("20110524110155","UTC-2")
    changeTimeZoneCheck("20110524110155","UTC-1")
    changeTimeZoneCheck("20110524110155","UTC")
    changeTimeZoneCheck("20110524110155","UTC+1")
    changeTimeZoneCheck("20110524110155","UTC+2")
    changeTimeZoneCheck("20110524110155","UTC+3")
    changeTimeZoneCheck("20110524110155","UTC+4")
    changeTimeZoneCheck("20110524110155","UTC+5")
    changeTimeZoneCheck("20110524110155","UTC+6")
    changeTimeZoneCheck("20110524110155","UTC+7")
    changeTimeZoneCheck("20110524110155","UTC+8")
    changeTimeZoneCheck("20110524110155","UTC+9")
    changeTimeZoneCheck("20110524110155","UTC+10")
    changeTimeZoneCheck("20110524110155","UTC+11")
    changeTimeZoneCheck("20110524110155","America/Indianapolis")
    changeTimeZoneCheck("20110524110155","America/New_York")
    changeTimeZoneCheck("20110524110155","America/Detroit")
    changeTimeZoneCheck("20110524110155","America/Kentucky/Louisville")
    changeTimeZoneCheck("20110524110155","America/Kentucky/Monticello")
    changeTimeZoneCheck("20110524110155","America/Indiana/Indianapolis")
    changeTimeZoneCheck("20110524110155","America/Indiana/Vincennes")
    changeTimeZoneCheck("20110524110155","America/Indiana/Winamac")
    changeTimeZoneCheck("20110524110155","America/Indiana/Marengo")
    changeTimeZoneCheck("20110524110155","America/Indiana/Petersburg")
    changeTimeZoneCheck("20110524110155","America/Indiana/Vevay")
