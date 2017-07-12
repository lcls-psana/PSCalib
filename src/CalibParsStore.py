#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module CalibParsStore...
#
#------------------------------------------------------------------------

"""
:py:class:`PSCalib.CalibParsStore` - is a factory class/method to switch between different device-dependent
segments/sensors to access their pixel geometry uling :py:class:`PSCalib.SegGeometry` interface.

Usage::

    # Import
    from PSCalib.CalibParsStore import cps
    from PSCalib.GlobalUtils import *

    # Initialization
    calibdir = env.calibDir()  # or e.g. '/reg/d/psdm/<INS>/<experiment>/calib'
    group = None               # or e.g. 'CsPad::CalibV1'
    source = 'Camp.0:pnCCD.1'
    runnum = 10                # or e.g. evt.run()
    pbits = 255
    o = cps.Create(calibdir, group, source, runnum, pbits)

    # or using different list of parameters to access calibration from hdf5 DCS file:
    o = cps.CreateForEvtEnv(self, calibdir, group, source, evt, env, pbits=0)

    # Access methods
    nda = o.pedestals()
    nda = o.pixel_status()
    nda = o.pixel_rms()
    nda = o.pixel_mask()
    nda = o.pixel_gain()
    nda = o.pixel_bkgd()
    nda = o.common_mode()

    status = o.status(ctype=PEDESTALS) # see list of ctypes in :py:class:`PSCalib.GlobalUtils`
    shape  = o.shape(ctype)
    size   = o.size(ctype)
    ndim   = o.ndim(ctype)

@see
    :py:class:`PSCalib.GenericCalibPars`
    :py:class:`PSCalib.GlobalUtils`
    :py:class:`PSCalib.CalibPars`
    :py:class:`PSCalib.CalibParsStore` 
    :py:class:`PSCalib.CalibParsBaseAndorV1`
    :py:class:`PSCalib.CalibParsBaseAndor3dV1`
    :py:class:`PSCalib.CalibParsBaseCameraV1`
    :py:class:`PSCalib.CalibParsBaseCSPad2x2V1`
    :py:class:`PSCalib.CalibParsBaseCSPadV1`
    :py:class:`PSCalib.CalibParsBaseEpix100aV1`
    :py:class:`PSCalib.CalibParsBasePnccdV1`
    :py:class:`PSCalib.CalibParsBasePrincetonV1`
    :py:class:`PSCalib.CalibParsBaseAcqirisV1`
    :py:class:`PSCalib.CalibParsBaseImpV1`

This software was developed for the SIT project.  If you use all or 
part of it, please give an appropriate acknowledgment.

@version $Id: 2013-03-08$

@author Mikhail S. Dubrovin
"""

#--------------------------------
#  Module's version from CVS --
#--------------------------------
__version__ = "$Revision$"
#--------------------------------

import sys

#------------------------------

import PSCalib.GlobalUtils            as gu
from PSCalib.GenericCalibPars         import GenericCalibPars

from PSCalib.CalibParsBaseAndorV1     import CalibParsBaseAndorV1    
from PSCalib.CalibParsBaseAndor3dV1   import CalibParsBaseAndor3dV1    
from PSCalib.CalibParsBaseCameraV1    import CalibParsBaseCameraV1   
from PSCalib.CalibParsBaseCSPad2x2V1  import CalibParsBaseCSPad2x2V1 
from PSCalib.CalibParsBaseCSPadV1     import CalibParsBaseCSPadV1    
from PSCalib.CalibParsBaseEpix100aV1  import CalibParsBaseEpix100aV1 
from PSCalib.CalibParsBasePnccdV1     import CalibParsBasePnccdV1    
from PSCalib.CalibParsBasePrincetonV1 import CalibParsBasePrincetonV1
from PSCalib.CalibParsBaseAcqirisV1   import CalibParsBaseAcqirisV1
from PSCalib.CalibParsBaseImpV1       import CalibParsBaseImpV1
from PSCalib.CalibParsBaseJungfrauV1  import CalibParsBaseJungfrauV1

#------------------------------

class CalibParsStore() :
    """Factory class for CalibPars object of different detectors"""

#------------------------------

    def __init__(self) :
        self.name = self.__class__.__name__
        
#------------------------------

    def Create(self, calibdir, group, source, runnum, pbits=0, fnexpc=None, fnrepo=None, tsec=None) :
        """ Factory method

            Parameters

            calibdir : string - calibration directory, ex: /reg/d/psdm/AMO/amoa1214/calib
            group    : string - group, ex: PNCCD::CalibV1
            source   : string - data source, ex: Camp.0:pnCCD.0
            runnum   : int    - run number, ex: 10
            pbits=0  : int    - print control bits, ex: 255
        """        

        dettype = gu.det_type_from_source(source)
        grp = group if group is not None else gu.dic_det_type_to_calib_group[dettype]

        if pbits : print '%s: Detector type = %d: %s' % (self.name, dettype, gu.dic_det_type_to_name[dettype])

        cbase = None
        if   dettype ==  gu.CSPAD     : cbase = CalibParsBaseCSPadV1()
        elif dettype ==  gu.CSPAD2X2  : cbase = CalibParsBaseCSPad2x2V1() 
        elif dettype ==  gu.PNCCD     : cbase = CalibParsBasePnccdV1()    
        elif dettype ==  gu.PRINCETON : cbase = CalibParsBasePrincetonV1()
        elif dettype ==  gu.ANDOR3D   : cbase = CalibParsBaseAndor3dV1()    
        elif dettype ==  gu.ANDOR     : cbase = CalibParsBaseAndorV1()    
        elif dettype ==  gu.EPIX100A  : cbase = CalibParsBaseEpix100aV1() 
        elif dettype ==  gu.JUNGFRAU  : cbase = CalibParsBaseJungfrauV1()    
        elif dettype ==  gu.ACQIRIS   : cbase = CalibParsBaseAcqirisV1() 
        elif dettype ==  gu.IMP       : cbase = CalibParsBaseImpV1() 
        elif dettype in (gu.OPAL1000,\
                         gu.OPAL2000,\
                         gu.OPAL4000,\
                         gu.OPAL8000,\
                         gu.TM6740,\
                         gu.ORCAFL40,\
                         gu.FCCD960,\
                         gu.QUARTZ4A150,\
                         gu.RAYONIX,\
                         gu.FCCD,\
                         gu.TIMEPIX,\
                         gu.FLI,\
                         gu.ZYLA,\
                         gu.PIMAX) : cbase = CalibParsBaseCameraV1()

        else :
            print '%s: calibration is not implemented data source "%s"' % (self.__class__.__name__, source)
            #raise IOError('Calibration parameters for source: %s are not implemented in class %s' % (source, self.__class__.__name__))
        return GenericCalibPars(cbase, calibdir, grp, source, runnum, pbits, fnexpc, fnrepo, tsec)

#------------------------------

    def CreateForEvtEnv(self, calibdir, group, source, evt, env, pbits=0) :
        """ Factory method
            This method makes access to the calibration store with fallback access to hdf5 file.

            Parameters

            calibdir : string - calibration directory, ex: /reg/d/psdm/AMO/amoa1214/calib
            group    : string - group, ex: PNCCD::CalibV1
            source   : string - data source, ex: Camp.0:pnCCD.0
            evt      : psana.Event - event object - is used to get event time to retrieve DCRange
            env      : psana.Env   - environment object - is used to retrieve file name
            pbits=0  : int         - print control bits, ex: 255
        """

        runnum = evt if isinstance(evt, int) else evt.run()

        fnexpc, fnrepo, tsec = None, None, None

        if not isinstance(evt, int) : # evt is not integer runnum

            from PSCalib.DCFileName import DCFileName
            from PSCalib.DCUtils import evt_time

            ofn = DCFileName(env, source, calibdir)
            if pbits & 512 : ofn.print_attrs()
            fnexpc = ofn.calib_file_path()
            fnrepo = ofn.calib_file_path_repo()
            tsec = evt_time(evt)

            #if True :
            if pbits :
                print '%s.CreateForEvtEnv: for tsec: %s' % (self.name, str(tsec))
                print '  expected hdf5 file name repo : %s' % (fnrepo)
                print '  expected hdf5 file name local: %s' % (fnexpc)

        return self.Create(calibdir, group, source, runnum, pbits, fnexpc, fnrepo, tsec)

#------------------------------

cps = CalibParsStore()

#------------------------------
#------------------------------
#----------- TEST -------------
#------------------------------
#------------------------------

import numpy as np

def print_nda(nda, cmt='') :
    arr = nda if isinstance(nda, np.ndarray) else np.array(nda) 
    str_arr = str(arr) if arr.size<5 else str(arr.flatten()[0:5])
    print '%s %s: shape=%s, size=%d, dtype=%s, data=%s' % \
          (cmt, type(nda), str(arr.shape), arr.size, str(arr.dtype), str_arr)

#------------------------------

def test_cps() :

    if len(sys.argv)==1   : print 'For test(s) use command: python %s <test-number=1-3>' % sys.argv[0]

    calibdir = '/reg/d/psdm/CXI/cxif5315/calib'
    group    = None # will be substituted from dictionary or 'CsPad::CalibV1' 
    source   = 'CxiDs2.0:Cspad.0'
    runnum   = 60
    pbits    = 0
 
    if(sys.argv[1]=='1') :
        cp = cps.Create(calibdir, group, source, runnum, pbits)
        cp.print_attrs()

        print_nda(cp.pedestals(),    'pedestals')
        print_nda(cp.pixel_rms(),    'pixel_rms')
        print_nda(cp.pixel_mask(),   'pixel_mask')
        print_nda(cp.pixel_status(), 'pixel_status')
        print_nda(cp.pixel_gain(),   'pixel_gain')
        print_nda(cp.common_mode(),  'common_mode')
        print_nda(cp.pixel_bkgd(),   'pixel_bkgd') 
        print_nda(cp.shape(),        'shape')
 
        print 'size=%d' % cp.size()
        print 'ndim=%d' % cp.ndim()

        statval = cp.status(gu.PEDESTALS)
        print 'status(PEDESTALS)=%d: %s' % (statval, gu.dic_calib_status_value_to_name[statval])

        statval = cp.status(gu.PIXEL_GAIN)
        print 'status(PIXEL_GAIN)=%d: %s' % (statval, gu.dic_calib_status_value_to_name[statval])
 
    else : print 'Non-expected arguments: sys.argv = %s use 1,2,...' % sys.argv

#------------------------------

if __name__ == "__main__" :
    test_cps()
    sys.exit( 'End of %s test.' % sys.argv[0])

#------------------------------
