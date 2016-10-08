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
    o = DCRange(begin, end=None, cmt=None)

    # Methods
    str_range   = o.range()               # (str) of the time stamp validity range
    t_sec       = o.begin()               # (double) time stamp beginning validity range
    t_sec       = o.end()                 # (double) time stamp ending validity range or (str) 'end'
    dico        = o.versions()            # (list of uint) versions of calibrations
    v           = o.vnum_def()            # returns default version number
    v           = o.vnum_last()           # returns last version number 
    vo          = o.version(vnum=None)    # returns version object for specified version
    ts_in_range = o.tsec_in_range(tsec)   # (bool) True/False if tsec is/not in the validity range
    evt_in_range= o.evt_in_range(evt)     # (bool) True/False if evt is/not in the validity range
    o.set_begin(tsbegin)                  # set (int) time stamp beginning validity range
    o.set_end(tsend)                      # set (int) time stamp ending validity range
    o.add_version(vnum=None, tsec_prod=None, nda=None, cmt=None) # add object for new version of calibration data
    o.set_vnum_def(vnum=None)             # set default version number, if available. vnum=None - use last available.
    vd = o.del_version(vnum=None)         # delete version, returns deleted version number or None if nothing was deleted
    o.del_versions()                      # delete all registered versions

    o.save(group)                         # saves object content under h5py.group in the hdf5 file. 
    o.load(group)                         # loads object content from the hdf5 file. 
    o.print_obj()                         # print info about this object and its children

@see project modules
    * :py:class:`PSCalib.DCStore`
    * :py:class:`PSCalib.DCType`
    * :py:class:`PSCalib.DCRange`
    * :py:class:`PSCalib.DCVersion`
    * :py:class:`PSCalib.DCBase`
    * :py:class:`PSCalib.DCInterface`
    * :py:class:`PSCalib.DCUtils`
    * :py:class:`PSCalib.DCDetectorId`
    * :py:class:`PSCalib.DCConfigParameters`
    * :py:class:`PSCalib.DCFileName`
    * :py:class:`PSCalib.DCLogger`
    * :py:class:`PSCalib.DCMethods`
    * :py:class:`PSCalib.DCEmail`

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
from PSCalib.DCUtils import sp, evt_time, get_subgroup, save_object_as_dset, delete_object

#------------------------------

def key(begin, end=None) :
    """ Return range as a string,
    ex.: 1471285222-1471285555 or 1471285222-end from double time like 1471285222.123456
    """
    str_begin = ('%d' % floor(begin)) if begin is not None else 0
    str_end = 'end' if (end is None or end=='end') else ('%d' % ceil(end))
    return '%s-%s' % (str_begin, str_end)

#------------------------------

class DCRange(DCRangeI) :

    """Class for the Detector Calibration (DC) project

    Parameters
    
    begin : double - time in sec
    end   : double - time in sec or None meaning infinity
    cmt   : str - comment
    """

    def __init__(self, begin, end=None, cmt=None) : # double, double/None
        DCRangeI.__init__(self, begin, end, cmt)
        self._name = self.__class__.__name__
        self.set_begin(begin)
        self.set_end(end)
        self._dicvers = {}
        self._dicstat = {} # flags 0/1 = good/marked-to-delete
        self._vnum_def = 0 # 0 = use last
        self._str_range = key(begin, end)
        log.debug('In c-tor for range: %s' % self._str_range, self._name)

    def range(self)                : return self._str_range

    def begin(self)                : return self._begin

    def end(self)                  : return self._end

    def versions(self)             : return self._dicvers

    def vnum_def(self) :
        #return self.vnum_last()
        if self._vnum_def == 0 or self._vnum_def is None :
            return self.vnum_last()
        return self._vnum_def 

    def vnum_last(self) :
        keys = self._dicvers.keys()
        return keys[-1] if len(keys) else 0

    def version(self, vnum=None)   :
        v = vnum if vnum is not None else self.vnum_def()
        return self._dicvers.get(v, None) if v is not None else None

    def set_begin(self, begin)     : self._begin = begin

    def set_end(self, end=None)    : self._end = 'end' if end is None else end

    def set_str_range(self, str_range) : self._str_range = str_range

    def add_version(self, vnum=None, tsec_prod=None, nda=None, cmt=None) :
        vn = self.vnum_last() + 1 if vnum is None else vnum
        o = self._dicvers[vn] = DCVersion(vn, tsec_prod, nda)
        self._dicstat[vn] = 0
        #self.add_history_record('vers=%d deleted. %s'%(vers, cmt))
        #if cmt is not None : o.add_history_record(cmt)
        #self._vnum_def = vn
        return o


    def set_vnum_def(self, vnum=None) :
        if vnum is None or vnum == 0 :
            self._vnum_def = 0 # will use last
        elif vnum in self._dicvers.keys() :
            self._vnum_def = vnum
            self.add_history_record('WARNING: set_vnum_defdef sets default version %d' % vnum)
        else :
            msg = 'Attemt to set non-existent version %d as default' % vnum
            log.warning(msg, self._name)


    def del_version(self, vnum=None) :
        vers = self.vnum_last() if vnum is None else vnum

        if vers in self._dicvers.keys() :
            del self._dicvers[vers]
            self._dicstat[vers] = 1 # set flag for delition 
            #self.add_history_record('vers=%d deleted. %s'%(vers, cmt))
            return vers
        else :
            msg = 'Requested delition of non-existent version %s' % str(vers)
            log.warning(msg, self._name)
            return None


    def del_versions(self) :
        for vers in self._dicvers.keys() :
            self.del_version(self, vers)


    def __del__(self) :
        for vers in self._dicvers.keys() :
            del self._dicvers[vers]


    def clear_versions(self) :
        self._dicvers.clear()
        self._dicstat.clear()


    def tsec_in_range(self, tsec) :
        if tsec < self.begin() : return False 
        if self.end() == 'end' : return True 
        if tsec > self.end()   : return False 
        return True


    def evt_in_range(self, evt) :
        return self.tsec_in_range(evt_time(evt))


    def __cmp__(self, other) :
        """for comparison in sorted()
        """
        if self.begin() <  other.begin() : return -1
        if self.begin() >  other.begin() : return  1
        if self.begin() == other.begin() : 
            if self.end() == other.end() : return  0
            if self.end()  == 'end'      : return -1 # inverse comparison for end
            if other.end() == 'end'      : return  1
            if self.end()  > other.end() : return -1
            if self.end()  < other.end() : return  1


    def save(self, group) :

        #grp = group.create_group(self.range())
        grp = get_subgroup(group, self.range())

        ds1 = save_object_as_dset(grp, 'begin',   data=self.begin())    # dtype='double'
        ds2 = save_object_as_dset(grp, 'end',     data=self.end())      # dtype='double'
        ds3 = save_object_as_dset(grp, 'range',   data=self.range())    # dtype='str'
        ds4 = save_object_as_dset(grp, 'versdef', data=self._vnum_def)  # dtype='int'

        msg = '=== save(), group %s object for %s' % (grp.name, self.range())
        log.debug(msg, self._name)

        #print 'ZZZ: self._dicstat', self._dicstat 
        #print 'ZZZ: self.versions()', self.versions() 

        for k,v in self._dicstat.iteritems() :
            if v & 1 : delete_object(grp, version_int_to_str(k))
            else     : self.versions()[k].save(grp)

        self.save_base(grp)


    def load(self, grp) :
        msg = '=== load data from group %s and fill object %s' % (grp.name, self._name)
        log.debug(msg, self._name)

        for k,v in dict(grp).iteritems() :
            #subgrp = v
            #print '    ', k , v

            if isinstance(v, sp.dataset_t) :                    
                log.debug('load dataset "%s"' % k, self._name)
                if   k == 'begin'   : self.set_begin(v[0])
                elif k == 'end'     : self.set_end(v[0])
                elif k == 'range'   : self.set_str_range(v[0])
                elif k == 'versdef' : self.set_vnum_def(v[0]) # self._vnum_def = v[0]
                else : log.warning('group "%s" has unrecognized dataset "%s"' % (grp.name, k), self._name)

            elif isinstance(v, sp.group_t) :
                if self.is_base_group(k,v) : continue
                log.debug('load group "%s"' % k, self._name)
                o = self.add_version(v['version'][0])
                o.load(v)


    def print_obj(self) :
        offset = 3 * self._offspace
        self.print_base(offset)
        print '%s begin     %s' % (offset, self.begin()),
        print ': %s'            % self.tsec_to_tstr(self.begin())
        print '%s end       %s' % (offset, self.end()),
        print ' %s'             % ('' if (self.end() in (None,'end')) else self.tsec_to_tstr(self.end()))
        print '%s range     %s' % (offset, self.range())
        print '%s versdef   %s' % (offset, self.vnum_def())
        print '%s N vers    %s' % (offset, len(self.versions()))
        print '%s versions  %s' % (offset, str(self.versions().keys()))

        for k,v in self.versions().iteritems() :
            v.print_obj()

#---- TO-DO

#    def get(self, p1, p2, p3)  : return None

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
    v = o.del_version(None)
    o.del_versions()
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
