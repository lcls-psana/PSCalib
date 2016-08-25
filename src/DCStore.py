#!/usr/bin/env python
#-----------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#-----------------------------------------------------------------------------

""":py:class:`PSCalib.DCStore` class for the Detector Calibration (DC) project.

Usage::

    # Import
    from PSCalib.DCStore import DCStore

    # Initialization
    calibdir = env.calibDir()  # or '/reg/d/psdm/INS/experiment/calib'
    rnum = evt.run()

    cs = DCStore(path)

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

import os
import sys
from time import time
import h5py

#import math
#import numpy as np
#from PSCalib.DCConfigParameters import cp
from PSCalib.DCInterface import DCStoreI
from PSCalib.DCType import DCType
from PSCalib.DCLogger import log
from PSCalib.DCUtils import save_string_as_dset, save_object_as_dset

#------------------------------

def print_warning(obj, metframe) :
    wng = 'INFO: %s.%s - abstract interface method needs to be re-implemented in derived class.' \
          % (obj.__class__.__name__, metframe.f_code.co_name)
    log.warning(wng, obj.__class__.__name__)
    #print wng
    #raise NotImplementedError(wng)

#------------------------------

#------------------------------

class DCStore(DCStoreI) :
    
    """Class for the Detector Calibration (DC) project

    cs = DCStore(fpath)

    tscfile     = cs.tscfile()               # (double) time stamp of the file creation
    dettype     = cs.dettype()               # (str) detector type
    detid       = cs.detid()                 # (str) detector id
    detname     = cs.detname()               # (str) detector name of self object
    predecessor = cs.predecessor()           # (str) detname of predecessor or None
    successor   = cs.successor()             # (str) detname of successor or None
    ctypes      = cs.ctypes()                # (list) calibration types in the file
    cto         = cs.ctypeobj(ctype)         # (DCType ~ h5py.Group) calibration type object

    nda         = cs.get(ctype, tsp, vers)

    cs.set_tscfile(tsec)                     # set (double) time stamp of the file creation 
    cs.set_dettype(dettype)                  # set (str) detector type
    cs.set_detid(detid)                      # set (str) detector id
    cs.set_detname(detname)                  # set (str) detector name of self object
    cs.set_predecessor(pred)                 # set (str) detname of predecessor or None
    cs.set_successor(succ)                   # set (str) detname of successor or None
    cs.add_ctype(ctype)                      # add (str) calibration type to the DCStore object
    cs.del_ctype(ctype)                      # delete ctype (str) from the DCStore object
    cs.clear_ctype()                         # clear all ctypes (str) from the DCStore object dictionary

    cs.save(group)                           # saves object content under h5py.group in the hdf5 file.
    cs.load(group)                           # loads object content from the hdf5 file. 
    """

#------------------------------

    def __init__(self, path) :
        DCStoreI.__init__(self, path)
        self._name = self.__class__.__name__
        self._set_file_name(path)
        self._tscfile = None
        self._dettype = None
        self._detid = None
        #self._detname = None
        self._predecessor = None
        self._successor = None
        self._dicctypes = {}
        log.debug('In c-tor for path: %s' % path, self._name)
        
#------------------------------

    def _set_file_name(self, path) :
        self._fpath = path if isinstance(path, str) else None

#------------------------------

    def tscfile(self)               : return self._tscfile

    def dettype(self)               : return self._dettype

    def detid(self)                 : return self._detid

    def detname(self)               :
        if self._dettype is None : return None
        if self._detid is None : return None
        return '%s-%s' % (self._dettype, self._detid)

    def predecessor(self)           : return self._predecessor

    def successor(self)             : return self._successor

    def ctypes(self)                : return self._dicctypes

    def ctypeobj(self, ctype)       : return self._dicctypes.get(ctype, None) if ctype is not None else None

    def set_tscfile(self, tsec=None): self._tscfile = time() if tsec is None else tsec

    def set_dettype(self, dettype)  : self._dettype = str(dettype)

    def set_detid(self, detid)      : self._detid = str(detid)

    def set_detname(self, detname)  :
        if not isinstance(detname, str) :
            self._dettype, self._detid = None, None
            return

        fields = detname.split('-')
        self._dettype, self._detid = fields[0], int(fields[1])

    def set_predecessor(self, pred) : self._predecessor = pred

    def set_successor(self, succ)   : self._successor = succ

    def add_ctype(self, ctype)      :
        o = self._dicctypes[ctype] = DCType(ctype)
        return o

    def del_ctype(self, ctype)      : del self._dicctypes[ctype] 

    def clear_ctypes(self)          : self._dicctypes.clear()     

    def save(self, path=None) :
        if path is not None : self._fpath = path
        if not isinstance(self._fpath, str) :
            msg = 'Invalid file name: %s' % str(self._fpath)
            log.error(msg, self.__class__.__name__)
            raise ValueError(msg)
        
        with h5py.File(self._fpath, 'w') as hf :
            
            msg = '= save(), group %s object for %s' % (hf.name, self.detname())
            log.debug(msg, self._name)

            ds1 = save_object_as_dset(hf, 'dettype',     data=self.dettype())     # 'str'
            ds2 = save_object_as_dset(hf, 'detname',     data=self.detname())     # 'str'
            ds3 = save_object_as_dset(hf, 'detid',       data=self.detid())       # 'str'
            ds4 = save_object_as_dset(hf, 'tscfile',     data=self.tscfile())     # 'double'
            ds5 = save_object_as_dset(hf, 'predecessor', data=self.predecessor()) # 'str'       
            ds6 = save_object_as_dset(hf, 'successor',   data=self.successor())   # 'str'

            for k,v in self.ctypes().iteritems() :
                #msg='Add type %s as object %s' % (k, v.ctype())
                #log.debug(msg, self._name)
                v.save(hf)

            self.save_base(hf)

            hf.close()
            log.info('File %s is saved' % self._fpath, self._name)


    def load(self, path=None) : 

        with h5py.File(self._fpath, 'r') as grp :
            
            #msg = 'Load data from file %s and fill %s object for group "%s"' % (self._fpath, self._name, grp.name)
            #log.info(msg, self._name)
            log.info('Load data from file %s' % self._fpath, self._name)

            for k,v in dict(grp).iteritems() :
                #subgrp = v
                #print '    ', k # , "   ", subg.name #, val, subg.len(), type(subg),

                if isinstance(v, h5py.Dataset) :                    
                    log.debug('load dataset "%s"' % k, self._name)
                    if   k == 'dettype'     : self.set_dettype(v[0])
                    elif k == 'detname'     : self.set_detname(v[0])
                    elif k == 'detid'       : self.set_detid(v[0])
                    elif k == 'tscfile'     : self.set_tscfile(v[0])
                    elif k == 'predecessor' : self.set_predecessor(v[0])
                    elif k == 'successor'   : self.set_successor(v[0])
                    else : log.warning('hdf file has unrecognized dataset "%s"' % k, self._name)

                elif isinstance(v, h5py.Group) :
                    if self.is_base_group(k,v) : continue
                    log.debug('load group "%s"' % k, self._name)                    
                    o = self.add_ctype(k)
                    o.load(v)
 

    def print_obj(self) :
        offset = 1 * self._offspace
        self.print_base(offset)
        print '%s dettype     %s' % (offset, self.dettype())
        print '%s detname     %s' % (offset, self.detname())
        print '%s detid       %s' % (offset, self.detid())
        print '%s tscfile     %f' % (offset, self.tscfile())
        print '%s predecessor %s' % (offset, self.predecessor())
        print '%s successor   %s' % (offset, self.successor())

        for k,v in self.ctypes().iteritems() :
        #    #msg='Add type %s as object %s' % (k, v.ctype())
        #    #log.info(msg, self._name)
            v.print_obj()

#---- TO-DO

    def get(self, ctype, tsp, vers) : print_warning(self, sys._getframe()); return None

#------------------------------
#------------------------------
#----------- TEST -------------
#------------------------------
#------------------------------

def test_DCStore() :

    o = DCStore('cspad-654321.h5')

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
    #o.save(None)
    o.load(None)

#------------------------------

def test_DCStore_save() :

    import numpy as np

    o = DCStore('cspad-654321.h5')
    o.set_dettype('cspad')
    o.set_detid('654321')
    o.set_tscfile(tsec=None)
    o.set_predecessor('cspad-654320')
    o.set_successor('cspad-654322')
    o.add_history_record('Some record 1 to commenet DCStore')
    o.add_history_record('Some record 2 to commenet DCStore')
    o.add_par('par-1-in-DCStore', 1)
    o.add_par('par-2-in-DCStore', 'some string 1')
    o.add_par('par-3-in-DCStore', 1.1)

    o.add_ctype('pixel_rms')
    o.add_ctype('pixel_status')
    o.add_ctype('pixel_mask')
    o.add_ctype('pixel_gain')
    o.add_ctype('geometry')
    po = o.add_ctype('pedestals')
    po.add_history_record('Some record 1 to commenet DCType')
    po.add_history_record('Some record 2 to commenet DCType')
    po.add_par('par-1-in-DCType', 2)
    po.add_par('par-2-in-DCType', 'some string 2')
    po.add_par('par-3-in-DCType', 2.2)

    t1 = time();
    t2 = t1+1;
    ro1 = po.add_range(t1, end=t1+1000)
    ro2 = po.add_range(t2, end=t2+1000)
    ro1.add_history_record('Some record 1 to commenet DCRange')
    ro1.add_history_record('Some record 2 to commenet DCRange')
    ro1.add_par('par-1-in-DCRange', 3)
    ro1.add_par('par-2-in-DCRange', 'some string 3')
    ro1.add_par('par-3-in-DCRange', 3.3)

    vo1 = ro2.add_version()
    vo2 = ro2.add_version()
    vo1.add_history_record('Some record 1 to commenet DCVersion')
    vo1.add_history_record('Some record 2 to commenet DCVersion')
    vo1.add_history_record('Some record 3 to commenet DCVersion')
    vo1.add_history_record('Some record 4 to commenet DCVersion')
    vo1.add_par('par-1-in-DCVersion', 4)
    vo1.add_par('par-2-in-DCVersion', 'some string 4')
    vo1.add_par('par-3-in-DCVersion', 4.4)

    #ro2.set_vnum_def(vo2.vnum())

    vo1.set_tsprod(time())
    vo1.add_data(np.zeros((32,185,388)))

    vo2.set_tsprod(time())
    vo2.add_data(np.ones((32,185,388)))

    o.print_obj()
    o.save()

#------------------------------

def test_DCStore_load() :

    import numpy as np

    o = DCStore('cspad-654321.h5')
    o.load()

    print 50*'_','\ntest o.print()' 
    o.print_obj()

#------------------------------

def test_DCStore_load_and_save() :

    import numpy as np

    o = DCStore('cspad-654321.h5')
    o.load()

    print 50*'_','\ntest o.print()' 
    o.print_obj()

    print 50*'_','\n test o.save(fname)' 
    o.save('cspad-re-loaded.h5')

#------------------------------

def test() :
    log.setPrintBits(0377) 
    if len(sys.argv)==1    : print 'For test(s) use command: python %s <test-number=1-4>' % sys.argv[0]
    elif(sys.argv[1]=='1') : test_DCStore()        
    elif(sys.argv[1]=='2') : test_DCStore_save()        
    elif(sys.argv[1]=='3') : test_DCStore_load()        
    elif(sys.argv[1]=='4') : test_DCStore_load_and_save()        
    else : print 'Non-expected arguments: sys.argv = %s use 1,2,...' % sys.argv

#------------------------------

if __name__ == "__main__" :
    test()
    sys.exit( 'End of %s test.' % sys.argv[0])

#------------------------------
