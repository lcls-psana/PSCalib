#!/usr/bin/env python
#------------------------------
"""
:py:class:`SvnProps` stores updated by svn properties
=====================================================

NOTE: To update revision number in this file when revision changes, use command:
psvn mktxtprop src/SvnProps.py
or
svn propset svn:keywords "Revision" src/SvnProps.py
Also see: ~/.subversion/config

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

Created: 2014-05-05 by Mikhai Dubrovin
"""
from __future__ import print_function

#------------------------------

import sys

#------------------------------

class SvnProps(object) :
    def __init__(self) : 
        self.updated  = "2014-05-05"
        self.revision = "$Revision$"
        self.author   = "$Author: dubrovin@SLAC.STANFORD.EDU $"
        self.id       = "$Id: SvnProps.py 9205 2014-11-05 00:58:52Z dubrovin@SLAC.STANFORD.EDU $"
        self.headurl  = "$HeadURL: https://pswww.slac.stanford.edu/svn/psdmrepo/PSCalib/trunk/src/SvnProps.py $"
        self.header   = "$Header:$"
        self.datelc   = "$LastChangedDate: 2014-11-04 16:58:52 -0800 (Tue, 04 Nov 2014) $"
        self.date     = "$Date: 2014-11-04 16:58:52 -0800 (Tue, 04 Nov 2014) $"

#------------------------------

svnprops = SvnProps()  # use it as a singleton

#------------------------------

if __name__ == "__main__" :
    
    print('svnprops.updated  : %s' % svnprops.updated)
    print('svnprops.revision : %s' % svnprops.revision)
    print('svnprops.author   : %s' % svnprops.author)
    print('svnprops.id       : %s' % svnprops.id)
    print('svnprops.headurl  : %s' % svnprops.headurl)
    print('svnprops.header   : %s' % svnprops.header)
    print('svnprops.datelc   : %s' % svnprops.datelc)
    print('svnprops.date     : %s' % svnprops.date)

    sys.exit ( 'End of test' )

#------------------------------
