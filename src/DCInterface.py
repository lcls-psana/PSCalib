#-----------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#-----------------------------------------------------------------------------

"""
:py:class:`PSCalib.DCInterface` - abstract interface for the Detector Calibration (DC) project.

Usage::

    # Import
    from PSCalib.DCInterface import DCStore

    # Initialization
    calibdir = env.calibDir()  # or '/reg/d/psdm/<INS>/<experiment>/calib'
    rnum = evt.run()

    fname = calibdir + '/cspad/cspad-123456.h5

    cs = DCStore(fname)

    # Access methods
    nda = cs.get(PEDESTALS, ts, vers=None)

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

import sys
#import math
#import numpy as np
#from time import time
from PSCalib.DCBase import DCBase

#------------------------------

def print_warning(obj, metframe) :
    wng = 'WARNING: %s.%16s - abstract interface method needs to be re-implemented in derived class.' \
          % (obj.__class__.__name__, metframe.f_code.co_name)
    print wng
    #raise NotImplementedError(wng)

#------------------------------

class DCStoreI(DCBase) :
    """Abstract interface class for the Detector Calibration (DC) project

       cs = DCStoreI(fname)

       tscfile     = cs.tscfile()               # (int) time stamp of the file creation
       dettype     = cs.dettype()               # (str) detector type
       detid       = cs.detid()                 # (str) detector id
       detname     = cs.detname()               # (str) detector name of self object
       predecessor = cs.predecessor()           # (str) detname of predecessor or None
       successor   = cs.successor()             # (str) detname of successor or None
       ctypes      = cs.ctypes()                # (list) calibration types in the file
       cto         = cs.ctypeobj(ctype)         # (DCType ~ h5py.Group) calibration type object
       nda         = cs.get(ctype, tsp, vers)

       cs.set_tscfile(ts)                       # set (int) time stamp of the file creation 
       cs.set_dettype(dettype)                  # set (str) detector type
       cs.set_detid(detid)                      # set (str) detector id
       cs.set_detname(detname)                  # set (str) detector name of self object
       cs.set_predecessor(pred)                 # set (str) detname of predecessor or None
       cs.set_successor(succ)                   # set (str) detname of successor or None
       cs.add_ctype(ctype)                      # add (str) calibration type to the DCStore object
       cs.del_ctype(ctype)                      # delete ctype (str) from the DCStore object
       cs.clear_ctypes(ctype)                   # clear dictionary of ctypes in the DCStore object
       cs.save(path)                            # save current calibration in the file specified by path, if path is Null - update current file.
       cs.load(path)                            # load content of the file in DCStore object
    """

    def __init__(self, fname) :
        DCBase.__init__(self)
        #super(DCStoreI, self).__init__()
        self._name = self.__class__.__name__

    def tscfile(self)               : print_warning(self, sys._getframe()); return None
    def dettype(self)               : print_warning(self, sys._getframe()); return None
    def detid(self)                 : print_warning(self, sys._getframe()); return None
    def detname(self)               : print_warning(self, sys._getframe()); return None
    def predecessor(self)           : print_warning(self, sys._getframe()); return None
    def successor(self)             : print_warning(self, sys._getframe()); return None
    def ctypes(self)                : print_warning(self, sys._getframe()); return None
    def ctypeobj(self, ctype)       : print_warning(self, sys._getframe()); return None
    def get(self, ctype, tsp, vers) : print_warning(self, sys._getframe()); return None
    def set_tscfile(self, ts)       : print_warning(self, sys._getframe())
    def set_dettype(self, dettype)  : print_warning(self, sys._getframe())
    def set_detid(self, detid)      : print_warning(self, sys._getframe())
    def set_detname(self, detname)  : print_warning(self, sys._getframe())
    def set_predecessor(self, pred) : print_warning(self, sys._getframe())
    def set_successor(self, succ)   : print_warning(self, sys._getframe())
    def add_ctype(self, ctype)      : print_warning(self, sys._getframe()); return None
    def del_ctype(self, ctype)      : print_warning(self, sys._getframe())
    def clear_ctypes(self)          : print_warning(self, sys._getframe())
    def save(self, path)            : print_warning(self, sys._getframe())
    def load(self, path)            : print_warning(self, sys._getframe())
    def print_obj(self, offset)     : print_warning(self, sys._getframe())

#------------------------------

class DCTypeI(DCBase) :
    """Abstract interface class for the Detector Calibration (DC) project

       cto = DCTypeI(type)

       ctype       = cto.ctype()                # (str) of ctype name
       ranges      = cto.ranges()               # (list) of time ranges for ctype
       ro          = cto.rangeobj(begin, end)   # (DCRange ~ h5py.Group) time stamp validity range object
       cto.add_range(tsr)                       # add (str) of time ranges for ctype
       cto.del_range(tsr)                       # delete range from the DCType object
    """
 
    def __init__(self, ctype) :
        DCBase.__init__(self)
        self._name = self.__class__.__name__

    def ctype(self)                : print_warning(self, sys._getframe()); return None
    def ranges(self)               : print_warning(self, sys._getframe()); return None
    def range(self, begin, end)    : print_warning(self, sys._getframe()); return None
    def add_range(self, begin, end): print_warning(self, sys._getframe()); return None
    def del_range(self, begin, end): print_warning(self, sys._getframe())
    def clear_ranges(self)         : print_warning(self, sys._getframe())
    def save(self, group)          : print_warning(self, sys._getframe())
    def load(self, path)           : print_warning(self, sys._getframe())
    def print_obj(self)            : print_warning(self, sys._getframe())

#------------------------------

class DCRangeI(DCBase) :
    """Abstract interface class for the Detector Calibration (DC) project

       o = DCRangeI(begin, end)

       tsbegin     = o.begin()               # (int) time stamp beginning validity range
       tsend       = o.end()                 # (int) time stamp ending validity range
       dico        = o.versions()            # (list of uint) versions of calibrations
       vnum        = o.vnum_def()            # (DCVersion ~ h5py.Group) reference to the default version in the time-range object
       vo          = o.version(vers)         # (DCVersion ~ h5py.Group) specified version in the time-range object
       o.set_begin(tsbegin)                  # set (int) time stamp beginning validity range
       o.set_end(tsend)                      # set (int) time stamp ending validity range
       o.add_version(vers)                   # set (DCVersion ~ h5py.Group) versions of calibrations
       o.set_versdef(vers)                   # set (DCVersion ~ h5py.Group) versions of calibrations
       o.del_version(vers)                   # delete version 
    """

    def __init__(self, begin, end) :
        DCBase.__init__(self)
        self._name = self.__class__.__name__

    def begin(self)                : print_warning(self, sys._getframe()); return None
    def end(self)                  : print_warning(self, sys._getframe()); return None
    def versions(self)             : print_warning(self, sys._getframe()); return None
    def version(self, vnum)        : print_warning(self, sys._getframe()); return None
    def vnum_def(self)             : print_warning(self, sys._getframe()); return None
    def vnum_last(self)            : print_warning(self, sys._getframe()); return None
    def set_begin(self, begin)     : print_warning(self, sys._getframe())
    def set_end(self, end)         : print_warning(self, sys._getframe())
    def add_version(self)          : print_warning(self, sys._getframe()); return None
    def set_vnum_def(self, vnum)   : print_warning(self, sys._getframe())
    def del_version(self, vnum)    : print_warning(self, sys._getframe())
    def clear_versions(self)       : print_warning(self, sys._getframe())
    def save(self, group)          : print_warning(self, sys._getframe())
    def load(self, group)          : print_warning(self, sys._getframe())
    def print_obj(self)            : print_warning(self, sys._getframe())

#------------------------------

class DCVersionI(DCBase) :
    """Abstract interface class for the Detector Calibration (DC) project

       o = DCVersionI(vnum, tsprod=None, arr=None)

       o.set_vnum(vnum)            # sets (int) version 
       o.set_tsprod(tsprod)        # sets (double) time stamp of the version production
       o.add_data(nda)             # sets (np.array) calibration array
       vnum   = o.vnum()           # returns (int) version number
       s_vnum = o.str_vnum()       # returns (str) version number
       tsvers = o.tsprod()         # returns (double) time stamp of the version production
       nda    = o.data()           # returns (np.array) calibration array
       o.save(group)               # saves object content under h5py.group in the hdf5 file. 
       o.load(group)               # loads object content from the h5py.group of hdf5 file. 
    """

    def __init__(self, vnum, tsprod=None, arr=None) :
        DCBase.__init__(self)
        self._name = self.__class__.__name__

    def set_vnum(self, vnum)       : print_warning(self, sys._getframe())
    def set_tsprod(self, tsprod)   : print_warning(self, sys._getframe())
    def add_data(self, nda)        : print_warning(self, sys._getframe())
    def vnum(self)                 : print_warning(self, sys._getframe()); return None
    def str_vnum(self)             : print_warning(self, sys._getframe()); return None
    def tsprod(self)               : print_warning(self, sys._getframe()); return None
    def data(self)                 : print_warning(self, sys._getframe()); return None
    def save(self, group)          : print_warning(self, sys._getframe())
    def load(self, group)          : print_warning(self, sys._getframe())
    def print_obj(self)            : print_warning(self, sys._getframe())

#------------------------------
#------------------------------
#----------- TEST -------------
#------------------------------
#------------------------------

def test_DCStoreI() :

    o = DCStoreI(None)  # 'cfname.hdf5'

    r = o.tscfile()
    r = o.dettype()
    r = o.detid()
    r = o.detname()
    r = o.predecessor()
    r = o.successor()
    r = o.ctypes()
    r = o.ctypeobj(None)
    r = o.get(None, None, None)    
    o.set_tscfile(None)
    o.set_dettype(None)
    o.set_detid(None)
    o.set_detname(None)
    o.set_predecessor(None)
    o.set_successor(None)
    o.add_ctype(None)
    o.del_ctype(None)
    o.clear_ctypes()
    o.save(None)
    o.load(None)

#------------------------------

def test_DCTypeI() :

    o = DCTypeI(None)

    r = o.ctype()
    r = o.ranges()
    r = o.range(None, None)
    o.add_range(None, None)
    o.del_range(None, None)
    o.save(None)
    o.load(None)

#------------------------------

def test_DCRangeI() :

    o = DCRangeI(None, None)

    b = o.begin()
    e = o.end()
    v = o.versions()
    n = o.vnum_def()
    r = o.version(None)
    o.set_begin(None)
    o.set_end(None)
    v = o.add_version()
    o.set_vnum_def(None)
    o.del_version(None)
    o.save(None)
    o.load(None)

#------------------------------

def test_DCVersionI() :

    o = DCVersionI(None)

    r = o.vnum()
    r = o.str_vnum()
    r = o.tsprod()
    r = o.data()
    o.set_vnum(None)
    o.set_tsprod(None)
    o.add_data(None)
    o.save(None)
    o.load(None)

#------------------------------

def test() :
    if len(sys.argv)==1 : print 'For test(s) use command: python %s <test-number=1-4>' % sys.argv[0]
    elif(sys.argv[1]=='1') : test_DCStoreI()        
    elif(sys.argv[1]=='2') : test_DCTypeI()        
    elif(sys.argv[1]=='3') : test_DCRangeI()        
    elif(sys.argv[1]=='4') : test_DCVersionI()        
    else : print 'Non-expected arguments: sys.argv = %s use 1,2,...' % sys.argv

#------------------------------

if __name__ == "__main__" :
    test()
    sys.exit( 'End of %s test.' % sys.argv[0])

#------------------------------