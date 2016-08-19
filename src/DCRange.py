#-----------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#-----------------------------------------------------------------------------

"""
:py:class:`PSCalib.DCRange` - class for the Detector Calibration (DC) project.

Usage::

    # Import
    from PSCalib.DCRange import DCRange

    # Initialization
    ro = DCRange(tsbegin,tsend=None)

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
from math import floor, ceil
#import math
#import numpy as np
#from time import time
#from PSCalib.DCConfigParameters import cp
from PSCalib.DCInterface import DCRangeI
from PSCalib.DCLogger import log
from PSCalib.DCVersion import DCVersion
from PSCalib.DCUtils import save_string_as_dset, save_object_as_dset

#------------------------------

def key(begin, end=None) :
    """ Return range as a string,
    ex.: 1471285222.108249-1471285555.108249 or 1471285222.108249-end
    """
    #str_begin = ('%.6f' % begin) if begin is not None else 0
    #str_end = ('%.6f' % end) if end is not None else 'end'
    str_begin = ('%d' % floor(begin)) if begin is not None else 0
    str_end = ('%d' % ceil(end)) if end is not None else 'end'
    return '%s-%s' % (str_begin, str_end)

#------------------------------

class DCRange(DCRangeI) :

    """Class for the Detector Calibration (DC) project

       o = DCRangeI(begin, end=None)

       tsbegin     = o.begin()               # (int) time stamp beginning validity range
       tsend       = o.end()                 # (int) time stamp ending validity range
       versions    = o.versions()            # (list of uint) versions of calibrations
       versodef    = o.versdef()             # (DCVersion ~ h5py.Group) reference to the default version in the time-range object
       verso       = o.version(vers)         # (DCVersion ~ h5py.Group) specified version in the time-range object
       o.set_begin(tsbegin)                  # set (int) time stamp beginning validity range
       o.set_end(tsend)                      # set (int) time stamp ending validity range
       o.add_version(vers)                   # set (DCVersion ~ h5py.Group) versions of calibrations
       o.set_versdef(vers)                   # set (DCVersion ~ h5py.Group) versions of calibrations
       o.del_version(vers)                   # delete version 

       r = o.get(None, None, None)    
       o.save(group)
       o.load(group)
    """

    def __init__(self, begin, end=None) :
        DCRangeI.__init__(self, begin, end)
        self._name = self.__class__.__name__
        self.set_begin(begin)
        self.set_end(end)
        self._dicvers = {}
        self._versdef = None
        self._str_range = key(begin, end)
        log.debug('In c-tor for range: %s' % self._str_range, self._name)

    def range(self)                : return self._str_range

    def begin(self)                : return self._begin

    def end(self)                  : return self._end

    def versions(self)             : return self._dicvers

    def versdef(self)              : return self._versdef

    def version(self, vers)        : return self._dicvers.get(vers, None) if vers is not None else None

    def set_begin(self, begin)     : self._begin = begin

    def set_end(self, end=None)    : self._end   = end

    def add_version(self, vers)    :
        o = self._dicvers[vers] = DCVersion(vers)
        return o

    def set_versdef(self, vers)    : self._versdef = vers

    def del_version(self, vers)    : del self._dicvers[vers]

    def clear_versions(self)       : self._dicvers.clear()

    def save(self, group) :
        grp = group.create_group(self.range())
        ds1 = save_object_as_dset(grp, 'begin',   data=self.begin())        # dtype='double'
        ds2 = save_object_as_dset(grp, 'end',     data=self.end())          # dtype='double'
        ds3 = save_object_as_dset(grp, 'range',   data=self.range())        # dtype='str'
        ds4 = save_object_as_dset(grp, 'versdef', data=str(self.versdef())) # dtype='str'

        msg = '=== save(), group %s object for %s' % (grp.name, self.range())
        log.info(msg, self._name)

        for k,v in self.versions().iteritems() :
            v.save(grp)

        self.save_base(grp)

#---- TO-DO

    def load(self, group) : pass

    def get(self, p1, p2, p3)  : return None


#------------------------------

def test_DCRange() :

    o = DCRange(None, None)

    r = o.begin()
    r = o.end()
    r = o.versions()
    r = o.versdef()
    r = o.version(None)
    o.set_begin(None)
    o.set_end(None)
    o.add_version(None)
    o.set_versdef(None)
    o.del_version(None)
    o.clear_versions()

    r = o.get(None, None, None)    
    o.save(None)
    o.load(None)

#------------------------------

def test() :
    if len(sys.argv)==1 : print 'For test(s) use command: python %s <test-number=1-4>' % sys.argv[0]
    elif(sys.argv[1]=='1') : test_DCRange()        
    else : print 'Non-expected arguments: sys.argv = %s use 1,2,...' % sys.argv

#------------------------------

if __name__ == "__main__" :
    test()
    sys.exit( 'End of %s test.' % sys.argv[0])

#------------------------------
