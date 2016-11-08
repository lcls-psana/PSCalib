#-----------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#-----------------------------------------------------------------------------

"""
:py:class:`PSCalib.DCDetectorId` - class for the Detector Calibration (DC) project.

Usage::

    # Import
    from PSCalib.DCDetectorId import id_epix, id_cspad

    # Parameters
    dsn = 'exp=cxif5315:run=169'
    # or
    dsn = '/reg/g/psdm/detector/data_test/types/0003-CxiDs2.0-Cspad.0-fiber-data.xtc'
    ds = psana.DataSource(dsn)
    env = ds.env()
    src = psana.Source('CxiDs2.0:Cspad.0') # or unique portion of the name ':Cspad.' or alias 'DsaCsPad'

    # Access methods
    ide = id_epix(env, src)
    idc = id_cspad(env, src)

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

#import os
#import math
#import numpy as np
#from time import time

from PSCalib.DCUtils import detector_full_name, psana_source

from Detector.PyDataAccess import\
     get_cspad_config_object,\
     get_cspad2x2_config_object,\
     get_epix_config_object

#------------------------------

def id_epix(env, src) :
    """Returns Epix100 Id as a string, e.g., 3925999616-0996663297-3791650826-1232098304-0953206283-2655595777-0520093719"""
    psa_src = psana_source(env, src)
    o = get_epix_config_object(env, psa_src)
    return '%010d-%010d-%010d-%010d-%010d-%010d-%010d' % (o.version(),\
                                                          o.carrierId0(),     o.carrierId1(),\
                                                          o.digitalCardId0(), o.digitalCardId1(),\
                                                          o.analogCardId0(),  o.analogCardId1())
#------------------------------

def id_cspad(env, src) :
    """Returns detector full name for any src, e.g., XppGon.0:Cspad2x2.0"""
    return detector_full_name(env, src)

#------------------------------

def id_det_noid(env, src) :
    """Returns detector full name for any src, e.g., XppGon.0:Cspad2x2.0"""
    return detector_full_name(env, src)

#------------------------------
#------------------------------
#------------------------------
#------------------------------
#------------------------------
#------------------------------

def test_id_epix() :
    dsn = '/reg/g/psdm/detector/data_test/types/0019-XppGon.0-Epix100a.0.xtc'
    src = 'XppGon.0:Epix100a.0'  
    ds = psana.DataSource(dsn)
    env = ds.env()
    print 20*'_', '\n%s:' % sys._getframe().f_code.co_name
    print 'dataset     : %s' % dsn
    print 'source      : %s' % src
    print 'Detector Id : %s' % id_epix(env, src)

#------------------------------

def test_id_cspad() :
    dsn = '/reg/g/psdm/detector/data_test/types/0003-CxiDs2.0-Cspad.0-fiber-data.xtc'
    src = ':Cspad.0' # 'CxiDs2.0:Cspad.0'
    ds = psana.DataSource(dsn)
    env = ds.env()
    print 20*'_', '\n%s:' % sys._getframe().f_code.co_name
    print 'dataset     : %s' % dsn
    print 'source      : %s' % src
    print 'Detector Id : %s' % id_cspad(env, src)

#------------------------------

def do_test() :
    tname = sys.argv[1] if len(sys.argv) > 1 else '0'
    print 50*'_', '\nTest %s:' % tname
    if   tname == '0' : test_id_epix(); test_id_cspad()
    elif tname == '1' : test_id_epix()        
    elif tname == '2' : test_id_cspad()        
    else : print 'Not-recognized test: %s' % tname
    sys.exit( 'End of test %s' % tname)

#------------------------------

if __name__ == "__main__" :
    import sys; global sys
    import psana; global psana
    do_test()

#------------------------------
