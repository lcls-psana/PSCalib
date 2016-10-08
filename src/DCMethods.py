#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#------------------------------------------------------------------------

"""
:py:class:`PSCalib.DCMethods` - contains a set of utilities for direct operations with calibration data.

Usage::

    # Import
    import PSCalib.DCMethods as dcm

    # Example of parameters

    dsname  = 'exp=cxif5315:run=129'
    # or:
    dsname   = '/reg/g/psdm/detector/data_test/xtc/cxif5315-e545-r0169-s00-c00.xtc'
    src      = 'Cspad.' # 'Epix100a.', etc
    ctype    = gu.PIXEL_MASK # OR: gu.PEDESTALS, gu.PIXEL_STATUS, etc.
    vers     = None # or 5
    calibdir = None # or './calib'
    nda      = np.zeros((32,185,388))
    pred     = 'CxiDs2.0:Cspad.0'
    succ     = 'CxiDs2.0:Cspad.0'

    # Methods
    dcm.add_constants(nda, evt, env, src, ctype, calibdir,\
                      vers=None,\
                      pred=None,\
                      succ=None,\
                      cmt=None) 

    dcm.get_constants(evt, env, src, ctype, calibdir=None, vers=None, verb=False)

    dcm.delete_version(evt, env, src, ctype, calibdir=None, vers=None, verb=False)

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

@version $Id: 2016-09-23$

@author Mikhail S. Dubrovin
"""

#--------------------------------
__version__ = "$Revision$"
#--------------------------------

import sys
import os
#import numpy as np
#import h5py
from time import time #localtime, strftime

from PSCalib.DCLogger import log
from PSCalib.DCFileName import DCFileName

import PSCalib.DCUtils as dcu
from PSCalib.DCStore import DCStore

sp = dcu.sp
gu = dcu.gu

#------------------------------

def add_constants(nda, evt, env, src='Epix100a.', ctype=gu.PIXEL_MASK, calibdir=None,\
                  vers=None,\
                  pred=None,\
                  succ=None,\
                  cmt=None,\
                  verb=False) :
    """Add specified numpy array to the hdf5 file.

    Parameters
    
    nda : numpy.array - array of calibration constants to save in file 
    env : psana.Env -> full detector name for psana.Source 
    evt : psana.Event -> event time
    src : str - source short/full name, alias or full
    ctype : gu.CTYPE - enumerated calibration type, e.g.: gu.PIXEL_MASK
    calibdir : str - fallback path to calib dir (if xtc file is copied - calib and experiment name are lost)
    vers : int - calibration version
    pred : str - predecessor name
    succ : str - successor name
    cmt : str - comment saved as a history record within DCRange
    verb : bool - verbosity, default=False - do not prnt any message
    """
    metname = sys._getframe().f_code.co_name

    str_ctype = gu.dic_calib_type_to_name[ctype]

    if verb : print '  src: %s\n  ctype: %s\n  vers: %s\n  calibdir:%s'%\
                    (src, str_ctype, vers, calibdir)

    ofn = DCFileName(env, src, calibdir)
    fname = ofn.calib_file_path()

    if verb :
        ofn.print_attrs()
        #print 'path: ', fname

    if fname is None :
        if verb : print 'WARNING: file name is not defined - return None'
        return None

    tsec_ev = dcu.evt_time(evt)

    cs = DCStore(fname)

    if verb : log.setPrintBits(0377) # 0377

    if os.path.exists(fname) : cs.load()

    cs.set_tscfile(tsec=tsec_ev)
    cs.set_predecessor(pred)
    cs.set_successor(succ)

    msg = 'detname:%s predecessor:%s successor:%s ts:%.0f' %\
          (cs.detname(), cs.predecessor(), cs.successor(), cs.tscfile())
    #cs.add_history_record('%s for %s' % (metname, msg))
    #cs.add_par('par-1-in-DCStore', 1)

    ct = cs.add_ctype(str_ctype)
    if ct is None : return
    #ct.add_history_record('%s - add DCType %s' % (metname,str_ctype))
    #ct.add_par('par-1-in-DCType', 1)

    cr = ct.add_range(tsec_ev, end=None)
    if cr is None : return
    #cr.set_vnum_def(vnum=None)

    cv = cr.add_version(vnum=vers, tsec_prod=time(), nda=nda, cmt=None)
    if cv is None : return
    v = cr.vnum_last() if vers is None else vers
    rec='%s vers=%d: %s' % (metname, v, cmt if cmt is not None else 'no-comments') 
    cr.add_history_record(rec)
    #cv.add_data(nda)
    #cv.add_history_record('%s - add data' % metname)

    if verb : 
        print 50*'_','\nIn %s:' % metname
        cs.print_obj()
    
    if verb : log.setPrintBits(02) # 0377

    ofn.make_path_to_calib_file() # depth=2, mode=0775)
    cs.save()

#------------------------------

def get_constants(evt, env, src='Epix100a.', ctype=gu.PIXEL_MASK, calibdir=None, vers=None, verb=False) :

    """Returns specified array of calibration constants.
    
    Parameters
    
    env : psana.Env -> full detector name for psana.Source 
    evt : psana.Event -> event time
    src : str - source short/full name, alias or full
    ctype : gu.CTYPE - enumerated calibration type, e.g.: gu.PIXEL_MASK
    calibdir : str - fallback path to calib dir (if xtc file is copied - calib and experiment name are lost)
    vers : int - calibration version
    """

    str_ctype = gu.dic_calib_type_to_name[ctype]
    if verb : print '  src: %s\n  ctype: %s\n  vers: %s\n  calibdir:%s'%\
                    (src, str_ctype, vers, calibdir)

    ofn = DCFileName(env, src, calibdir)
    fname = ofn.calib_file_path()
    if verb :
        ofn.print_attrs()

    if fname is None : return None
    if not os.path.exists(fname) :
        if verb : print 'WARNING: path does not exist.'
        return None

    cs = DCStore(fname)
    cs.load()
    if verb :
        print 50*'_','\nDCStore.print_obj()' 
        cs.print_obj()

    ct = cs.ctypeobj(str_ctype)
    if ct is None : return None 
    #if verb : 
    #    print 50*'_','\nDCType.print_obj()' 
    #    ct.print_obj()

    cr = ct.range_for_evt(evt)
    if cr is None : return None
    #if verb :
    #    print 50*'_','\nDCRange.print_obj()' 
    #    cr.print_obj()

    cv = cr.version(vnum=vers)
    if cv is None : return None
    #if verb :
    #    print 50*'_','\nDCVersion.print_obj()' 
    #    cv.print_obj()

    return cv.data()

#------------------------------

def delete_version(evt, env, src='Epix100a.', ctype=gu.PIXEL_MASK, calibdir=None, vers=None, cmt=None, verb=False) :

    """Delete specified version from calibration constants.
    
    Parameters
    
    env : psana.Env -> full detector name for psana.Source 
    evt : psana.Event -> event time
    src : str - source short/full name, alias or full
    ctype : gu.CTYPE - enumerated calibration type, e.g.: gu.PIXEL_MASK
    calibdir : str - fallback path to calib dir (if xtc file is copied - calib and experiment name are lost)
    vers : int - calibration version
    """
    metname = sys._getframe().f_code.co_name

    str_ctype = gu.dic_calib_type_to_name[ctype]
    if verb : print '  src: %s\n  ctype: %s\n  vers: %s\n  calibdir:%s'%\
                    (src, str_ctype, vers, calibdir)

    ofn = DCFileName(env, src, calibdir)
    fname = ofn.calib_file_path()
    if verb :
        ofn.print_attrs()

    if fname is None : return None
    if not os.path.exists(fname) :
        if verb : print 'WARNING: path does not exist.'
        return None

    cs = DCStore(fname)
    cs.load()
    #if verb :
    #    print 50*'_','\nDCStore.print_obj()' 
    #    cs.print_obj()

    ct = cs.ctypeobj(str_ctype)
    if ct is None : return None 
    #if verb :
    #    print 50*'_','\nDCType.print_obj()' 
    #    ct.print_obj()

    cr = ct.range_for_evt(evt)
    if cr is None : return None
    #if verb :
    #    print 50*'_','\nDCRange.print_obj()' 
    #    cr.print_obj()

    v = vers if vers is not None else cr.vnum_last()
    c = cmt if cmt is not None else ''
    rec='%s vers=%d: %s' % (metname, v, c) 
    cr.add_history_record(rec)

    vdeleted = cr.del_version(vnum=vers)

    if verb : log.setPrintBits(02) # 0377

    ofn.make_path_to_calib_file() # depth=2, mode=0775)

    if verb :
        print 50*'_','\nDCStore.print_obj() after delete version %d' % vdeleted
        cs.print_obj()
    
    cs.save()
    return vdeleted

#------------------------------

def print_file_content(evt, env, src='Epix100a.', calibdir=None) :

    """Delete specified version from calibration constants.
    
    Parameters
    
    env : psana.Env -> full detector name for psana.Source 
    evt : psana.Event -> event time
    src : str - source short/full name, alias or full
    calibdir : str - fallback path to calib dir (if xtc file is copied - calib and experiment name are lost)
    """
    metname = sys._getframe().f_code.co_name

    ofn = DCFileName(env, src, calibdir)
    fname = ofn.calib_file_path()
    ofn.print_attrs()

    if fname is None :
        print 'WARNING: file name is not defined'
        return

    if not os.path.exists(fname) :
        print 'WARNING: path does not exist'
        return

    cs = DCStore(fname)

    t0_sec = time()
    cs.load()
    print 'File content loading time (sec) = %.6f' % (time()-t0_sec)
    
    print 50*'_','\nDCStore.print_obj()' 
    cs.print_obj()

#------------------------------
#------------------------------
#------------------------------
#------------------------------

def get_constants_v0(*par, **opt) :
    ofn = DCFileName(par[0], opt['src'])

#------------------------------

def test_add_constants() :
    metname = sys._getframe().f_code.co_name
    print 20*'_', '\n%s' % metname

    import numpy as np

    vers = None
    #nda  = np.zeros((32,185,388), dtype=np.float32)
    nda  = np.zeros((1000,1000), dtype=np.float32)
    pred = None
    succ = None
    cmt  = 'my comment to add'
    
    add_constants(nda, gevt, genv, gsrc, gctype, gcalibdir, vers, pred, succ, cmt, gverb)
    print '%s: constants added nda.shape=%s' % (metname, nda.shape)

#------------------------------

def test_get_constants() :
    metname = sys._getframe().f_code.co_name
    print 20*'_', '\n%s' % metname

    vers = None
    nda = get_constants(gevt, genv, gsrc, gctype, gcalibdir, vers, gverb)

    print '%s: retrieved constants for vers %s nda.shape=%s' % (metname, str(vers), str(nda.shape))

#------------------------------

def test_delete_version() :
    metname = sys._getframe().f_code.co_name
    print 20*'_', '\n%s' % metname

    vers = None # for default - last version
    cmt  = 'my comment to delete'
    vdeleted = delete_version(gevt, genv, gsrc, gctype, gcalibdir, vers, cmt, gverb)

    print '%s: deleted version %s' % (metname, str(vdeleted))

#------------------------------

def test_print_file_content() :
    print 20*'_', '\n%s' % sys._getframe().f_code.co_name
    print_file_content(gevt, genv, gsrc, gcalibdir)

#------------------------------

def test_misc() :
    print 20*'_', '\n%s' % sys._getframe().f_code.co_name

    import PSCalib.DCUtils as dcu

    print 20*'_', '\n%s:' % sys._getframe().f_code.co_name
    print 'get_enviroment(USER) : %s' % dcu.get_enviroment()
    print 'get_login()          : %s' % dcu.get_login()
    print 'get_hostname()       : %s' % dcu.get_hostname()
    print 'get_cwd()            : %s' % dcu.get_cwd()

#------------------------------

def set_parameters() :

    import psana

    global genv, gevt, gsrc, gctype, gcalibdir, gverb

    #dsname  = 'exp=cxif5315:run=129'
    #dsname   = '/reg/g/psdm/detector/data_test/xtc/cxif5315-e545-r0169-s00-c00.xtc'
    #gsrc      = 'Cspad.'

    #dsname = 'exp=mfxn8316:run=11'
    dsname = '/reg/g/psdm/detector/data_test/types/0021-MfxEndstation.0-Epix100a.0.xtc'
    gsrc      = ':Epix100a.'

    gcalibdir = './calib'
    gctype    = gu.PIXEL_STATUS # gu.PIXEL_MASK, gu.PEDESTALS, etc.
    gverb     = True
    #gverb     = False

    ds = psana.DataSource(dsname)
    genv=ds.env()
    gevt=ds.events().next()

#------------------------------

def do_test() :
    from time import time

    set_parameters()

    #log.setPrintBits(0377)

    tname = sys.argv[1] if len(sys.argv) > 1 else '0'
    print 50*'_', '\nTest %s:' % tname
    t0_sec = time()
    if   tname == '0' : test_misc(); 
    elif tname == '1' : test_add_constants()
    elif tname == '2' : test_get_constants()
    elif tname == '3' : test_delete_version()
    elif tname == '4' : test_print_file_content()
    else : print 'Not-recognized test name: %s' % tname
    msg = 'End of test %s, consumed time (sec) = %.6f' % (tname, time()-t0_sec)
    sys.exit(msg)
 
#------------------------------

if __name__ == "__main__" :
    do_test()

#------------------------------
