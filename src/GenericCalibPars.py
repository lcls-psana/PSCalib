#!/usr/bin/env python
#------------------------------
"""
Class :py:class:`GenericCalibPars` - implementation of :py:class:`CalibPars` interface methods for generic detectors.

Usage::

    # THIS CLASS IS NOT SUPPOSED TO BE USED AS SELF-DEPENDENT...
    # USE :py:class:`PSCalib.CalibParsStore`

    from PSCalib.GenericCalibPars import GenericCalibPars

    from PSCalib.CalibParsBaseAndorV1     import CalibParsBaseAndorV1    
    from PSCalib.CalibParsBaseCameraV1    import CalibParsBaseCameraV1   
    from PSCalib.CalibParsBaseCSPad2x2V1  import CalibParsBaseCSPad2x2V1 
    ...
    from PSCalib.CalibParsBasePnccdV1     import CalibParsBasePnccdV1    

    cbase = CalibParsBasePnccdV1()    

    calibdir = '/reg/d/psdm/CXI/cxif5315/calib'
    group    = 'PNCCD::CalibV1'
    source   = 'CxiDs2.0:Cspad.0'
    runnum   = 60
    pbits    = 255
    ctype    = gu.PEDESTALS

    gcp = GenericCalibPars(cbase, calibdir, group, source, runnum, pbits)

    nda = gcp.pedestals()
    nda = gcp.pixel_rms()
    nda = gcp.pixel_mask()
    nda = gcp.pixel_bkgd()
    nda = gcp.pixel_status()
    nda = gcp.pixel_datast()
    nda = gcp.pixel_gain()
    nda = gcp.pixel_offset()
    nda = gcp.common_mode()

    status = gcp.get_status(ctype=PEDESTALS) # see  list of ctypes in :py:class:`PSCalib.GlobalUtils`
    shape  = gcp.get_shape(ctype)
    size   = gcp.get_size(ctype)
    ndim   = gcp.get_ndim(ctype)

    nda = gcp.set_version(vers=None)
    nda = gcp.constants_default(ctype)
    nda = gcp.constants_calib(ctype)
    nda = gcp.constants_dcs(ctype, vers=None, verb=False)
    nda = gcp.constants(ctype, vers=None, verb=False)
    
See :py:class:`CalibPars`, :py:class:`CalibParsStore`, :py:class:`CalibParsCspad2x1V1`, :py:class:`GlobalUtils`

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

Author: Mikhail Dubrovin

--------
"""
#------------------------------

import sys
#import os
#import math
import numpy as np
from PSCalib.CalibPars import CalibPars
from PSCalib.CalibFileFinder import CalibFileFinder

import PSCalib.GlobalUtils as gu
from PSCalib.NDArrIO import load_txt # , save_txt, list_of_comments

from pyimgalgos.GlobalUtils import print_ndarr
#------------------------------

class GenericCalibPars(CalibPars) :

#------------------------------

    def __init__(self, cbase, calibdir, group, source, runnum, pbits=255, fnexpc=None, fnrepo=None, tsec=None) : 
        """:py:class:`GenericCalibPars` constructor

            Parameters

            - cbase    : PSCalib.CalibParsBase* - base-object
            - calibdir : string - calibration directory, ex: /reg/d/psdm/AMO/amoa1214/calib
            - group    : string - group, ex: PNCCD::CalibV1
            - source   : string - data source, ex: Camp.0:pnCCD.0
            - runnum   : int    - run number, ex: 10
            - pbits    : int    - print control bits, ex: 255
            - fnexpc   : str    - path to experiment calib hdf5 file
            - fnrepo   : str    - path to repository calib hdf5 file
            - tsec     : float  - event time to select calibration file range 
        """
        CalibPars.__init__(self)
        self.name = self.__class__.__name__

        self.cbase    = cbase    # ex.: PSCalib.CalibParsBaseAndorV1 or None
        self.calibdir = calibdir # ex.: '/reg/d/psdm/CXI/cxif5315/calib'
        self.group    = group    # ex.: 'PNCCD::CalibV1'
        self.source   = source   # ex.: 'CxiDs2.0:Cspad.0' 
        self.runnum   = runnum   # ex.: 10
        self.pbits    = pbits    # ex.: 255
        #---------- parameters introduced for DCS fallback
        self.fnexpc   = fnexpc   # ex.: /reg/d/psdm/<INS>/<exp>/calib/epix100a/epix100a-3925868555...h5
        self.fnrepo   = fnrepo   # ex.: /reg/g/psdm/detector/calib/epix100a/epix100a-3925868555...h5
        self.tsec     = tsec     # ex.: 1474587520.88

        self.reset_dicts()

        self.cff    = None if self.cbase is None else CalibFileFinder(calibdir, group, 0377 if pbits else 0)
        self._ndim  = None if self.cbase is None else cbase.ndim                                            
        self._size  = None if self.cbase is None else cbase.size # it might be 0 for variable size cameras  
        self._shape = None if self.cbase is None else cbase.shape                                           

#------------------------------

    def reset_dicts(self) :
        """Re-sets dictionaries with status and constants for cash
        """
        self.dic_constants = dict([(k, None) for k in gu.calib_types])
        self.dic_status    = dict([(k, gu.UNDEFINED) for k in gu.calib_types])

#------------------------------

    def set_print_bits(self, pbits=0) :
        self.pbits  = pbits
        if self.cff is not None : self.cff.pbits=0377 if pbits else 0

#------------------------------

    def print_attrs(self) :
        """Prints attributes
        """
        inf = '\nAttributes of %s object:' % self.name \
            + '\n  base object: %s' % self.cbase.__class__.__name__ \
            + '\n  calibdir   : %s' % self.calibdir \
            + '\n  group      : %s' % self.group    \
            + '\n  source     : %s' % self.source   \
            + '\n  runnum     : %s' % self.runnum   \
            + '\n  fnexpc     : %s' % self.fnexpc   \
            + '\n  fnrepo     : %s' % self.fnrepo   \
            + '\n  tsec       : %s' % self.tsec     \
            + '\n  pbits      : %s' % self.pbits    
        print inf

#------------------------------

    def msgh(self, i=3) :
        """Returns message header
        """
        if   i==3 : return '%s: source %s run=%d' % (self.name, self.source, self.runnum)
        elif i==2 : return '%s: source %s' % (self.name, self.source) 
        else      : return '%s:' % (self.name)

#------------------------------

    def msgw(self) :
        return '%s: %s' % (self.name, 'implementation of method %s')

#------------------------------

    def constants_default(self, ctype) :
        """Returns numpy array with default constants

        Logic:

        - 0) if detector is undefined and base constants are missing - return None
        - 1) if constants for common mode - return default numpy array
        - 2) if base size of calibration constants is 0 (for variable image size cameras)
           - return None (they can be loaded from file only!
        - 3) for PEDESTALS, PIXEL_STATUS, PIXEL_BKGD return numpy array of **zeros** for base shape and dtype
        - 4) for all other calibration types return numpy array of **ones** for base shape and dtype
        """

        if self.cbase is None : return None

        tname = gu.dic_calib_type_to_name[ctype]
        if self.pbits : print 'INFO %s: load default constants of type %s' % (self.msgh(3), tname)

        if ctype == gu.COMMON_MODE :
            self.dic_status[ctype] = gu.DEFAULT
            return np.array(self.cbase.cmod, dtype = gu.dic_calib_type_to_dtype[ctype])

        if self.cbase.size == 0 :
            if self.pbits : print 'WARNING %s: default constants of type %s' % (self.msgh(3), tname) \
                                  + ' are not available for variable size cameras.'\
                                  + '\n  Check if the file with calibration constanrs is available in calib directory.'
            return None

        self.dic_status[ctype] = gu.DEFAULT

        if ctype in (gu.PEDESTALS, gu.PIXEL_STATUS, gu.PIXEL_BKGD, gu.PIXEL_DATAST, gu.PIXEL_OFFSET) :
            return np.zeros(self.cbase.shape, dtype = gu.dic_calib_type_to_dtype[ctype])

        else : # for PIXEL_RMS, PIXEL_GAIN, PIXEL_MASK, etc
            return np.ones(self.cbase.shape, dtype = gu.dic_calib_type_to_dtype[ctype])

#------------------------------

    def constants_calib(self, ctype) :
        """Returns numpy array with calibration constants for specified type

        Logic:

        - a) if detector is undefined and base constants are missing - return None
        - 0) if constants are available in cash (self.dic_constants) - return them
        - 1) if calib file is not found:
           - return result from constants_default(ctype)
        - 2) try to load numpy array from file
           -- exception - return result from constants_default(ctype)
        - 3) if constants for common mode - return numpy array as is
        - 4) if base size==0 - return numpy array as is 
        - 5) if base size>0 and loaded size is not equal to the base size
           - return result from constants_default(ctype)
        - 6) reshape numpy array to the base shape and return.
        """

        if self.cbase is None : return None

        if self.dic_constants[ctype] is not None :
            return self.dic_constants[ctype]

        tname = gu.dic_calib_type_to_name[ctype]
        if self.pbits : print 'INFO %s: load constants of type %s' % (self.msgh(3), tname)

        fname = self.cff.findCalibFile(str(self.source), tname, self.runnum)

        if fname == '' :
            if self.pbits : print 'WARNING %s: calibration file for type %s is not found.' % (self.msgh(3), tname)
            self.dic_status[ctype] = gu.NONFOUND
            nda = self.dic_constants[ctype] = self.constants_default(ctype)
            return nda

        if self.pbits : print self.msgw() % tname
        if self.pbits : print 'fname_name: %s' % fname

        nda = None 
        try :
            #nda = np.loadtxt(fname, dtype=gu.dic_calib_type_to_dtype[ctype])
            nda = np.array(load_txt(fname), dtype=gu.dic_calib_type_to_dtype[ctype])
        except :
            if self.pbits : print 'WARNING %s: calibration file for type %s is unreadable.' % (self.msgh(3), tname)
            self.dic_status[ctype] = gu.UNREADABLE
            nda = self.dic_constants[ctype] = self.constants_default(ctype)
            return nda

        if ctype == gu.COMMON_MODE :
            self.dic_status[ctype] = gu.LOADED
            self.dic_constants[ctype] = nda
            return nda

        # Set shape, size, and ndim for variable size cameras
        if self.cbase.size == 0 :
            self.dic_status[ctype] = gu.LOADED
            self._ndim  = nda.ndim
            self._size  = nda.size
            self._shape = nda.shape
            self.dic_constants[ctype] = nda
            return nda

        # METADATA CAN BE CHECKED FOR >2-D ARRAYS AS WELL,
        # but, this >2-d detector should not be variable-size and should have parameters in the base class

        if self.cbase.size>0 and nda.size != self.cbase.size :
            self.dic_status[ctype] = gu.WRONGSIZE
            return self.constants_default(ctype)

        nda.shape = self._shape
        self.dic_status[ctype] = gu.LOADED
        self.dic_constants[ctype] = nda
        return nda

#------------------------------

    def constants_dcs(self, ctype=gu.PEDESTALS, vers=None) :
        """Returns numpy array with calibration constants of specified type from DCS

            See :class:`PSCalib.DCStore`, :class:`PSCalib.DCMethods`

            Parameters
    
            - ctype : int - enumerated calibration type from :class:`PSCalib.GlobalUtils`, e.g. gu.PIXEL_STATUS
        """
        from PSCalib.DCMethods import get_constants_from_file, is_good_fname

        verb = self.pbits & 128
        if self.pbits :
            self.print_attrs()
            print '%s.constants_dcs  tsec: %s  ctype: %s  vers: %s  verb: %s\n  fname: %s' %\
                  (self.name, str(self.tsec), str(ctype), str(vers), str(verb), self.fnexpc)

        return get_constants_from_file(self.fnrepo, self.tsec, ctype, vers, verb)

        #return get_constants_from_file(self.fnexpc, self.tsec, ctype, vers, verb) if is_good_fname(self.fnexpc) else\
        #       get_constants_from_file(self.fnrepo, self.tsec, ctype, vers, verb)

#------------------------------

    def constants(self, ctype, vers=None) :
        """Returns numpy array with calibration constants of specified type

            Parameters
    
            - vers  : int - version number
            - ctype : int - enumerated calibration type from :class:`PSCalib.GlobalUtils`, e.g. gu.PIXEL_STATUS
        """
        if self.dic_constants[ctype] is not None :
            return self.dic_constants[ctype]

        arr = self.constants_calib(ctype)

        if arr is None or self.dic_status[ctype] == gu.DEFAULT :
            # try to retrieve constants from DCS hdf5 file
            arr_dcs = self.constants_dcs(ctype, vers)
            if arr_dcs is not None :
                self.dic_status[ctype] = gu.DCSTORE
                self.dic_constants[ctype] = arr_dcs
                arr = arr_dcs

        if self.pbits & 128 :
            i_status = self.dic_status[ctype]
            s_status = gu.dic_calib_status_value_to_name[i_status]
            s_ctype  = gu.dic_calib_type_to_name[ctype]
            print '%s.constants  ctype:%s  status:%s' % (self.name, s_ctype, s_status)
            print_ndarr(arr, name='    arr', first=0, last=5)

        return arr

#------------------------------

    def pedestals(self, vers=None) :
        """Returns pedestals
        """
        return self.constants(gu.PEDESTALS, vers)

#------------------------------

    def pixel_status(self, vers=None) :
        """Returns pixel_status
        """
        return self.constants(gu.PIXEL_STATUS, vers)

#------------------------------

    def pixel_datast(self, vers=None) :
        """Returns pixel_datast
        """
        return self.constants(gu.PIXEL_DATAST, vers)

#------------------------------

    def pixel_rms(self, vers=None) :
        """Returns pixel_rms
        """
        return self.constants(gu.PIXEL_RMS, vers)

#------------------------------

    def pixel_gain(self, vers=None) :
        """Returns pixel_gain
        """
        return self.constants(gu.PIXEL_GAIN, vers)

#------------------------------

    def pixel_offset(self, vers=None) :
        """Returns pixel_offset
        """
        return self.constants(gu.PIXEL_OFFSET, vers)

#------------------------------

    def pixel_mask(self, vers=None) :
        """Returns pixel_mask
        """
        return self.constants(gu.PIXEL_MASK, vers)

#------------------------------

    def pixel_bkgd(self, vers=None) :
        """Returns pixel_bkgd
        """
        return self.constants(gu.PIXEL_BKGD, vers)

#------------------------------

    def common_mode(self, vers=None) :
        """Returns common_mode
        """
        return self.constants(gu.COMMON_MODE, vers)

#------------------------------
#------------------------------
#------------------------------
#------------------------------

    def retrieve_shape(self) :
        """Retrieve shape, size, and ndim parameters and set them as member data
        """        
        # if parameters are already set from base class or at file loading
        if self._size>0 : return
        for ctype in gu.calib_types[:-1] : # loop over all types except the last - common_mode
            arr = self.constants(ctype)    # shape parameters should be set here
            if arr is None : continue
            if arr.size>0  : break         # check if shape parameters defined

#------------------------------

    def ndim(self, ctype=gu.PEDESTALS) :
        """Returns ndim
        """
        if self.pbits & 128 : print self.msgw() % 'ndim  (%s)' % gu.dic_calib_type_to_name[ctype]
        if ctype == gu.COMMON_MODE : return 1
        else :
            self.retrieve_shape()
            return self._ndim

#------------------------------

    def shape(self, ctype=gu.PEDESTALS) :
        """Returns shape
        """
        if self.pbits & 128 : print self.msgw() % 'shape (%s)' % gu.dic_calib_type_to_name[ctype]
        if ctype == gu.COMMON_MODE : return self.cbase.shape_cm
        else :
            self.retrieve_shape()
            return self._shape

#------------------------------

    def size(self, ctype=gu.PEDESTALS) :
        """Returns size
        """
        if self.pbits & 128 : print self.msgw() % 'size  (%s)' % gu.dic_calib_type_to_name[ctype]
        if ctype == gu.COMMON_MODE : return self.cbase.size_cm
        else :
            self.retrieve_shape()
            return self._size

#------------------------------

    def status(self, ctype=gu.PEDESTALS) :
        """Returns status
        """
        if self.pbits & 128 : print self.msgw() % 'status(%s)' % gu.dic_calib_type_to_name[ctype]
        return self.dic_status[ctype]

#------------------------------
#------------------------------
#------------------------------
#------------------------------

if __name__ == "__main__" :
    sys.exit ('Test of %s is not implemented.' % sys.argv[0])

#------------------------------
#------------------------------
#------------------------------
#------------------------------


