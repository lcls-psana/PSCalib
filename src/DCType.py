#-----------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#-----------------------------------------------------------------------------

"""
:py:class:`PSCalib.DCType` - class for the Detector Calibration (DC) project.

Usage::

    # Import
    from PSCalib.DCType import DCType

    # Initialization
    ct = DCType(ctype)

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
from PSCalib.DCInterface import DCTypeI
from PSCalib.DCLogger import log
from PSCalib.DCRange import DCRange, key
from PSCalib.DCUtils import save_object_as_dset, h5py

#------------------------------

class DCType(DCTypeI) :
    
    """Class for the Detector Calibration (DC) project

    cto = DCType(type)

    cto.set_ctype(ctype)                # add (str) of time ranges for ctype.
    ctype  = cto.ctype()                # returns (str) of ctype name.
    ranges = cto.ranges()               # returns (dict) of time range objects.
    range  = cto.range(begin, end)      # returns time stamp validity range object.
    cto.add_range(begin, end)           # add (str) of time ranges for ctype.
    cto.del_range(begin, end)           # delete range from the DCType object.
    cto.clear_ranges()                  # delete all range objects from dictionary.

    o.save(group)                       # saves object content under h5py.group in the hdf5 file.
    o.load(group)                       # loads object content from the hdf5 file. 
    r = o.get(None, None, None)    
    """

    def __init__(self, ctype) :
        DCTypeI.__init__(self, ctype)
        self._name = self.__class__.__name__
        self._dicranges = {}
        self._ctype = ctype
        log.debug('In c-tor for ctype: %s' % ctype, self._name)

    def ctype(self)  : return self._ctype

    def set_ctype(self, ctype) : self._ctype = ctype

    def ranges(self) : return self._dicranges

    def range(self, begin, end=None) :
        return self._dicranges.get(key(begin, end), None) if begin is not None else None

    def add_range(self, begin, end=None) :
        o = self._dicranges[key(begin, end)] = DCRange(begin, end)
        return o

    def del_range(self, begin, end=None) : del self._dicranges[key(begin, end)] 

    def clear_ranges(self) : self._dicranges.clear()

    def save(self, group) :

        grp = group.create_group(self.ctype())
        ds1 = save_object_as_dset(grp, 'ctype', data=self.ctype()) # dtype='str'

        msg = '== save(), group %s object for %s' % (grp.name, self.ctype())
        log.debug(msg, self._name)

        for k,v in self.ranges().iteritems() :
            v.save(grp)

        self.save_base(grp)

    def load(self, grp) :
        msg = '== load data from group %s and fill object %s' % (grp.name, self._name)
        log.debug(msg, self._name)

        for k,v in dict(grp).iteritems() :
            #subgrp = v
            #print 'XXX    ', k , v# , "   ", subg.name #, val, subg.len(), type(subg),

            if isinstance(v, h5py.Dataset) :                    
                log.debug('load dataset "%s"' % k, self._name)
                if   k == 'ctype' : self.set_ctype(v[0])
                else : log.warning('group "%s" has unrecognized dataset "%s"' % (grp.name, k), self._name)

            elif isinstance(v, h5py.Group) :
                if self.is_base_group(k,v) : continue
                log.debug('load group "%s"' % k, self._name)
                o = self.add_range(v['begin'][0], v['end'][0])
                o.load(v)


    def print_obj(self) :
        offset = 2 * self._offspace
        self.print_base(offset)
        print '%s ctype     %s' % (offset, self.ctype())
        for k,v in self.ranges().iteritems() :
            v.print_obj()

#---- TO-DO

    def get(self, p1, p2, p3)  : return None

#------------------------------
#------------------------------
#------------------------------
#----------- TEST -------------
#------------------------------
#------------------------------

def test_DCType() :

    o = DCType('pedestals')

    r = o.ctype()
    r = o.ranges()
    r = o.range(None)
    o.add_range(None)
    o.del_range(None)
    o.clear_ranges()

    r = o.get(None, None, None)    
    #o.save(None)
    o.load(None)

#------------------------------

def test() :
    log.setPrintBits(0377) 
    if   len(sys.argv)==1  : print 'For test(s) use command: python %s <test-number=1-4>' % sys.argv[0]
    elif(sys.argv[1]=='1') : test_DCType()        
    else : print 'Non-expected arguments: sys.argv = %s use 1,2,...' % sys.argv

#------------------------------

if __name__ == "__main__" :
    test()
    sys.exit( 'End of %s test.' % sys.argv[0])

#------------------------------