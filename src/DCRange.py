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
from PSCalib.DCVersion import DCVersion, version_int_to_str
from PSCalib.DCUtils import save_object_as_dset, h5py

#------------------------------

def key(begin, end=None) :
    """ Return range as a string,
    ex.: 1471285222-1471285555 or 1471285222-end from double time like 1471285222.123456
    """
    str_begin = ('%d' % floor(begin)) if begin is not None else 0
    str_end = ('%d' % ceil(end)) if end is not None else 'end'
    return '%s-%s' % (str_begin, str_end)

#------------------------------

class DCRange(DCRangeI) :

    """Class for the Detector Calibration (DC) project

       o = DCRangeI(begin, end=None)

       str_range   = o.range()               # (str) of the time stamp validity range
       t_sec       = o.begin()               # (double) time stamp beginning validity range
       t_sec       = o.end()                 # (double) time stamp ending validity range
       dico        = o.versions()            # (list of uint) versions of calibrations
       v           = o.vnum_def()            # returns default version number
       vo          = o.version(vnum=None)    # returns version object for specified version
       o.set_begin(tsbegin)                  # set (int) time stamp beginning validity range
       o.set_end(tsend)                      # set (int) time stamp ending validity range
       o.add_version()                       # add object for new version of calibration data
       o.set_vnum_def(vnum=None)             # set default version number, if available. vnum=None - set last available.
       o.set_vnum_last()                     # set last available versions of calibrations
       o.del_version(vnum=None)              # delete version 

       r = o.get(None, None, None)    
       o.save(group)                         # saves object content under h5py.group in the hdf5 file. 
       o.load(group)                         # loads object content from the hdf5 file. 
    """

    def __init__(self, begin, end=None) : # double, double/None
        DCRangeI.__init__(self, begin, end)
        self._name = self.__class__.__name__
        self.set_begin(begin)
        self.set_end(end)
        self._dicvers = {}
        self._vnum_def = None
        self._str_range = key(begin, end)
        log.debug('In c-tor for range: %s' % self._str_range, self._name)

    def range(self)                : return self._str_range

    def begin(self)                : return self._begin

    def end(self)                  : return self._end

    def versions(self)             : return self._dicvers

    def vnum_def(self) :
        return self._vnum_def if self._vnum_def is not None else len(self._dicvers)

    def vnum_last(self)            : return len(self._dicvers)

    def version(self, vnum=None)   :
        v = vnum if vnum is not None else self.vnum_def()
        return self._dicvers.get(v, None) if v is not None else None

    def set_begin(self, begin)     : self._begin = begin

    def set_end(self, end=None)    : self._end   = end

    def set_str_range(self, str_range) : self._str_range = str_range

    def add_version(self, vnum=None) :
        vn = self.vnum_last() + 1 if vnum is None else vnum
        o = self._dicvers[vn] = DCVersion(vn)
        return o

    def set_vnum_def(self, vnum=None) :
        if vnum is None :
            self._vnum_def = self.vnum_last()
        elif vnum in self._dicvers.keys() :
            self._vnum_def = vnum
        else :
            msg = 'Attemt to set non-existent version %d as default' % vnum
            log.warning(msg, self._name)

    def del_version(self, vnum) :
        if vnum in self._dicvers.keys() :
            del self._dicvers[vnum]
        else :
            msg = 'Requested delition of non-existent version %s' % str(vnum)
            log.warning(msg, self._name)

    def clear_versions(self) : self._dicvers.clear()

    def save(self, group) :
        grp = group.create_group(self.range())
        ds1 = save_object_as_dset(grp, 'begin',   data=self.begin())    # dtype='double'
        ds2 = save_object_as_dset(grp, 'end',     data=self.end())      # dtype='double'
        ds3 = save_object_as_dset(grp, 'range',   data=self.range())    # dtype='str'
        ds4 = save_object_as_dset(grp, 'versdef', data=self.vnum_def()) # dtype='int'

        msg = '=== save(), group %s object for %s' % (grp.name, self.range())
        log.debug(msg, self._name)

        for k,v in self.versions().iteritems() :
            v.save(grp)

        self.save_base(grp)


    def load(self, grp) :
        msg = '=== load data from group %s and fill object %s' % (grp.name, self._name)
        log.debug(msg, self._name)

        for k,v in dict(grp).iteritems() :
            #subgrp = v
            #print '    ', k , v

            if isinstance(v, h5py.Dataset) :                    
                log.debug('load dataset "%s"' % k, self._name)
                if   k == 'begin'   : self.set_begin(v[0])
                elif k == 'end'     : self.set_end(v[0])
                elif k == 'range'   : self.set_str_range(v[0])
                elif k == 'versdef' : self._vnum_def = v[0]
                else : log.warning('group "%s" has unrecognized dataset "%s"' % (grp.name, k), self._name)

            elif isinstance(v, h5py.Group) :
                if self.is_base_group(k,v) : continue
                log.debug('load group "%s"' % k, self._name)
                o = self.add_version(v['version'][0])
                o.load(v)


    def print_obj(self) :
        offset = 3 * self._offspace
        self.print_base(offset)
        print '%s begin     %s' % (offset, self.begin())
        print '%s end       %s' % (offset, self.end())
        print '%s range     %s' % (offset, self.range())
        print '%s versdef   %s' % (offset, self.vnum_def())
        for k,v in self.versions().iteritems() :
            v.print_obj()

#---- TO-DO

    def get(self, p1, p2, p3)  : return None

#------------------------------

def test_DCRange() :

    o = DCRange(None, None)

    r = o.begin()
    r = o.end()
    r = o.versions()
    r = o.vnum_def()
    r = o.version(None)
    o.set_begin(None)
    o.set_end(None)
    o.add_version()
    o.set_vnum_def(None)
    o.del_version(None)
    o.clear_versions()

    r = o.get(None, None, None)    
    #o.save(None)
    o.load(None)

#------------------------------

def test() :
    log.setPrintBits(0377) 

    if len(sys.argv)==1 : print 'For test(s) use command: python %s <test-number=1-4>' % sys.argv[0]
    elif(sys.argv[1]=='1') : test_DCRange()        
    else : print 'Non-expected arguments: sys.argv = %s use 1,2,...' % sys.argv

#------------------------------

if __name__ == "__main__" :
    test()
    sys.exit( 'End of %s test.' % sys.argv[0])

#------------------------------
