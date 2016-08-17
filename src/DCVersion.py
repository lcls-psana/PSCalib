#-----------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#-----------------------------------------------------------------------------

"""
:py:class:`PSCalib.DCVersion` - class for the Detector Calibration (DC) project.

Usage::

    # Import
    from PSCalib.DCVersion import DCVersion

    # Initialization
    vo = DCVersion(version=None)

    # Access methods
    ...

@see implementation in :py:class:`PSCalib.DCStore`,
                       :py:class:`PSCalib.DCType`,
                       :py:class:`PSCalib.DCRange`,
                       :py:class:`PSCalib.DCVersion`,
                       :py:class:`PSCalib.DCBase`

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

@version $Id$

@author Mikhail S. Dubrovin
"""

#---------------------------------
__version__ = "$Revision$"
#---------------------------------

import os
import sys
#import math
#import numpy as np
#from time import time
#from PSCalib.DCConfigParameters import cp
from PSCalib.DCInterface import DCVersionI
from PSCalib.DCLogger import log
from PSCalib.DCUtils import save_string_as_dset

#------------------------------

class DCVersion(DCVersionI) :

    """Class for the Detector Calibration (DC) project

       o = DCVersionI(vers)

       tsvers      = o.tsprod()             # (int) time stamp of the version production
       calibdata   = o.calib()              # (np.array) calibration array
       vers        = o.version()            # (str) version 
       o.set_tsprod(tsprod)                 # set (int) time stamp of the version production
       o.add_calib(nda)                     # set (np.array) calibration array
       o.set_version(vers)                  # set (string) version 
       o.save(group)
       o.load(group)
    """

    def __init__(self, vers) :
        DCVersionI.__init__(self, vers)
        self._name = self.__class__.__name__

        self.set_version(vers)
        self._tsprod = None
        self._nda = None
        log.info('In c-tor for version: %s' % vers, self._name)

    def version(self)              : return self._vers

    def tsprod(self)               : return self._tsprod

    def calib(self)                : return self._nda

    def set_version(self, vers)    : self._vers = vers

    def set_tsprod(self, tsprod)   : self._tsprod = tsprod

    def add_calib(self, nda)       : self._nda = nda

    def save(self, group) :

        grp = group.create_group(self.version())
        ds1 = save_string_as_dset(grp, 'version', str(self.version()))
        ds2 = grp.create_dataset('tsprod', (1,), dtype='double', data = self.tsprod())
        ds3 = grp.create_dataset('calib', data = self.calib())

        msg = '==== save(), group %s object for %s' % (grp.name, self.version())
        log.info(msg, self._name)

        #for k,v in self.versions().iteritems() :
        #    v.save(grp)

        self.save_base(grp)

#---- TO-DO

    def load(self, group) : pass

    def get(self, p1, p2, p3)  : return None

#------------------------------

def test_DCVersion() :

    o = DCVersion(None)

    r = o.tsprod()
    r = o.calib()
    o.set_tsprod(None)
    o.add_calib(None)

    r = o.get(None, None, None)    
    o.save(None)
    o.load(None)

#------------------------------

def test() :
    if len(sys.argv)==1 : print 'For test(s) use command: python %s <test-number=1-4>' % sys.argv[0]
    elif(sys.argv[1]=='1') : test_DCVersion()        
    else : print 'Non-expected arguments: sys.argv = %s use 1,2,...' % sys.argv

#------------------------------

if __name__ == "__main__" :
    test()
    sys.exit( 'End of %s test.' % sys.argv[0])

#------------------------------
