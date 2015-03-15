'''
Created on Dec 14, 2014

@author: Duhi
'''

#! py -3
#need to install  Python Windows 32-bit extensions

import wmi

def main():
    rval = 0  # Default: Check passes.

    # Initialize WMI objects and query.
    wmi_o = wmi.WMI('.')
    wql = ("SELECT * FROM Win32_NTLogEvent WHERE Logfile = "
           "\'Application\' AND EventCode = \'3036\'")

    # Query WMI object.
    wql_r = wmi_o.query(wql)

    if len(wql_r) > 0:
        rval = -1  # Check fails.

    return rval



if __name__ == '__main__':
    main()