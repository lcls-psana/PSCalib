#-----------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#-----------------------------------------------------------------------------

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
    vers     = None # or e.g. 5
    calibdir = None # or e.g. './calib'
    nda      = np.zeros((32,185,388))
    pred     = 'CxiDs2.0:Cspad.0'
    succ     = 'CxiDs2.0:Cspad.0'
    range    = '1474587520-end'

    # Methods of
    dcm.add_constants(nda, evt, env, src, ctype, calibdir, vers=None, pred=None, succ=None, cmt=None) 

    dcm.print_file(fname)
    dcm.print_file_content(env, src, calibdir=None)
    nda = dcm.get_constants(evt, env, src, ctype, calibdir=None, vers=None, verb=False)
    nda = dcm.get_constants_from_file(fname, evt, ctype, vers=None, verb=False)

    dcm.delete_version(evt, env, src, ctype, calibdir=None, vers=None, verb=False)
    dcm.delete_range  (evt, env, src, ctype, cdir, range, msg, verb)
    dcm.delete_ctype  (evt, env, src, ctype, cdir, msg, verb)

@see methods 
    :meth:`add_constants`, 
    :meth:`print_file`, 
    :meth:`print_file_content`, 
    :meth:`get_constants`, 
    :meth:`get_constants_from_file`, 
    :meth:`delete_version`, 
    :meth:`delete_range`, 
    :meth:`delete_ctype`

@see project modules
    * :class:`PSCalib.DCStore`
    * :class:`PSCalib.DCType`
    * :class:`PSCalib.DCRange`
    * :class:`PSCalib.DCVersion`
    * :class:`PSCalib.DCBase`
    * :class:`PSCalib.DCInterface`
    * :class:`PSCalib.DCUtils`
    * :class:`PSCalib.DCDetectorId`
    * :class:`PSCalib.DCConfigParameters`
    * :class:`PSCalib.DCFileName`
    * :class:`PSCalib.DCLogger`
    * :class:`PSCalib.DCMethods`
    * :class:`PSCalib.DCEmail`

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

def is_good_fname(fname, verb=False) :
    """Checks the hdf5 file name parameter fname validity, returns True or False.
    
    Parameters
    
    fname : str - full path to the file
    """
    metname = sys._getframe().f_code.co_name

    if fname is None :
        if verb : print '%s WARNING: file name is None' % metname
        return False

    if not isinstance(fname, str) :
        if verb : print '%s WARNING: parameter fname is not str' % metname
        return False

    if not os.path.exists(fname) :
        if verb : print '%s WARNING: file %s does not exist' % (metname, fname)
        return False

    return True

#------------------------------

def evt_to_tsec(par) :
    """Checks if par is float or assumes that it is psana.Event and returns event time in (float) sec or None.
    Parameters

    par   : psana.Event | float - tsec event time | None    
    """
    return None if par is None else\
           par if isinstance(par, float) else\
           dcu.evt_time(par) # for psana.Event

#------------------------------

def add_constants(data, evt, env, src='Epix100a.', ctype=gu.PIXEL_MASK, calibdir=None,\
                  vers=None,\
                  pred=None,\
                  succ=None,\
                  cmt=None,\
                  verb=False) :
    """Adds specified numpy array to the hdf5 file.

    Parameters
    
    data : numpy.array or str - array or string of calibration constants/data to save in file
    env  : psana.Env -> full detector name for psana.Source 
    evt  : psana.Event -> event time
    src  : str - source short/full name, alias or full
    ctype: gu.CTYPE - enumerated calibration type, e.g.: gu.PIXEL_MASK
    calibdir : str - fallback path to calib dir (if xtc file is copied - calib and experiment name are lost)
    vers : int - calibration version
    pred : str - predecessor name
    succ : str - successor name
    cmt  : str - comment saved as a history record within DCRange
    verb : bool - verbosity, default=False - do not prnt any message

    Back to :py:class:`PSCalib.DCMethods`
    """
    metname = sys._getframe().f_code.co_name

    str_ctype = gu.dic_calib_type_to_name[ctype]

    if verb : print '  src: %s\n  ctype: %s\n  vers: %s\n  calibdir:%s'%\
                    (src, str_ctype, vers, calibdir)

    ofn = DCFileName(env, src, calibdir)
    if verb : ofn.print_attrs()

    fname = ofn.calib_file_path()

    if verb : ofn.print_attrs()

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

    ct = cs.add_ctype(str_ctype, cmt='')
    if ct is None : return
    #ct.add_history_record('%s - add DCType %s' % (metname,str_ctype))
    #ct.add_par('par-1-in-DCType', 1)

    exp = env.experiment()
    exp = exp if exp != '' else 'unknown'
    runnum = evt.run()
    msg = 'exp=%s:run=%s' % (exp, str(runnum))
    cr = ct.add_range(tsec_ev, end=None, cmt=msg)
    if cr is None : return
    cr.add_par('experiment', exp)
    cr.add_par('run', str(runnum))
    #cr.set_vnum_def(vnum=None)

    msg = '' if cmt is None else cmt
    cv = cr.add_version(vnum=vers, tsec_prod=time(), nda=data, cmt=msg)
    if cv is None : return
    #v = cr.vnum_last() if vers is None else vers
    #rec='%s vers=%d: %s' % (metname, v, cmt if cmt is not None else 'no-comments') 
    #cr.add_history_record(rec)

    if verb : 
        print 50*'_','\nIn %s:' % metname
        cs.print_obj()
    
    if verb : log.setPrintBits(02) # 0377

    ofn.make_path_to_calib_file() # depth=2, mode=0775)
    cs.save()

#------------------------------

def get_constants_from_file(fname, par, ctype=gu.PIXEL_MASK, vers=None, verb=False) :
    """Returns specified array of calibration constants.
    
    Parameters

    fname : full path to the hdf5 file
    par   : psana.Event | float - tsec event time
    ctype : gu.CTYPE - enumerated calibration type, e.g.: gu.PIXEL_MASK
    vers  : int - calibration version

    Back to :py:class:`PSCalib.DCMethods`
    """
    if not is_good_fname(fname, verb) : return None

    cs = DCStore(fname)
    cs.load()
    if verb :
        print 50*'_','\nDCStore.print_obj()' 
        cs.print_obj()

    str_ctype = gu.dic_calib_type_to_name[ctype]
    ct = cs.ctypeobj(str_ctype)
    if ct is None : return None 
    #ct.print_obj()

    tsec = evt_to_tsec(par)
    #print 'XXX: get DCRange object for time = %.3f' % tsec
    cr = ct.range_for_tsec(tsec)
    #cr = ct.range_for_evt(evt)

    if cr is None : return None
    #cr.print_obj()

    cv = cr.version(vnum=vers)
    if cv is None : return None
    #cv.print_obj()

    return cv.data()

#------------------------------

def get_constants(par, env, src='Epix100a.', ctype=gu.PIXEL_MASK, calibdir=None, vers=None, verb=False) :
    """Returns specified array of calibration constants.
    
    Parameters
    
    par   : psana.Event | float - tsec event time
    env   : psana.Env -> full detector name for psana.Source 
    src   : str - source short/full name, alias or full
    ctype : gu.CTYPE - enumerated calibration type, e.g.: gu.PIXEL_MASK
    calibdir : str - fallback path to calib dir (if xtc file is copied - calib and experiment name are lost)
    vers : int - calibration version

    Back to :py:class:`PSCalib.DCMethods`
    """
    str_ctype = gu.dic_calib_type_to_name[ctype]
    if verb : print '  src: %s\n  ctype: %s\n  vers: %s\n  calibdir:%s'%\
                    (src, str_ctype, vers, calibdir)

    ofn = DCFileName(env, src, calibdir)
    if verb : ofn.print_attrs()

    fname = ofn.calib_file_path()

    return get_constants_from_file(fname, par, ctype, vers, verb)

#------------------------------

def delete_version(evt, env, src='Epix100a.', ctype=gu.PIXEL_MASK, calibdir=None, vers=None, cmt=None, verb=False) :
    """Delete specified version from calibration constants.
    
    Parameters
    
    evt : psana.Event -> event time
    env : psana.Env -> full detector name for psana.Source 
    src : str - source short/full name, alias or full
    ctype : gu.CTYPE - enumerated calibration type, e.g.: gu.PIXEL_MASK
    calibdir : str - fallback path to calib dir (if xtc file is copied - calib and experiment name are lost)
    vers : int - calibration version
    cmt  : str - comment
    verb : bool - verbousity

    Back to :py:class:`PSCalib.DCMethods`
    """
    metname = sys._getframe().f_code.co_name

    str_ctype = gu.dic_calib_type_to_name[ctype]
    if verb : print '  src: %s\n  ctype: %s\n  vers: %s\n  calibdir:%s'%\
                    (src, str_ctype, vers, calibdir)

    ofn = DCFileName(env, src, calibdir)
    if verb : ofn.print_attrs()

    fname = ofn.calib_file_path()
    if not is_good_fname(fname, verb) : return None

    cs = DCStore(fname)
    cs.load()

    ct = cs.ctypeobj(str_ctype)
    if ct is None : return None 
    #ct.print_obj()

    cr = ct.range_for_evt(evt)
    if cr is None : return None

    v = vers if vers is not None else cr.vnum_last()

    vdel = cr.mark_version(vnum=vers, cmt=cmt)

    if verb : log.setPrintBits(02) # 0377

    cs.save()

    if verb :
        print 50*'_','\nDCStore.print_obj() after delete version %s' % str(vdel)
        cs.print_obj()
    
    return vdel

#------------------------------

def delete_range(evt, env, src='Epix100a.', ctype=gu.PIXEL_MASK, calibdir=None, range=None, cmt=None, verb=False) :
    """Delete specified time range from calibration constants.
    
    Parameters
    
    evt : psana.Event -> event time
    env : psana.Env -> full detector name for psana.Source 
    src : str - source short/full name, alias or full
    ctype : gu.CTYPE - enumerated calibration type, e.g.: gu.PIXEL_MASK
    calibdir : str - fallback path to calib dir (if xtc file is copied - calib and experiment name are lost)
    range : str - range, e.g. '1474587520-end'
    cmt   : str - comment
    verb  : bool - verbousity

    Back to :py:class:`PSCalib.DCMethods`
    """
    #metname = sys._getframe().f_code.co_name

    str_ctype = gu.dic_calib_type_to_name[ctype]
    if verb : print '  src: %s\n  ctype: %s\n  range: %s\n  calibdir:%s'%\
                    (src, str_ctype, range, calibdir)

    ofn = DCFileName(env, src, calibdir)
    if verb : ofn.print_attrs()

    fname = ofn.calib_file_path()
    if not is_good_fname(fname, verb) : return None

    cs = DCStore(fname)
    cs.load()
    #cs.print_obj()

    ct = cs.ctypeobj(str_ctype)
    if ct is None : return None 

    rdel = ct.mark_range_for_key(range, cmt=cmt)
    if rdel is None : return None

    if verb : log.setPrintBits(02) # 0377

    cs.save()

    if verb :
        print 50*'_','\nDCStore.print_obj() after delete range %s' % rdel
        cs.print_obj()
    
    return rdel

#------------------------------

def delete_ctype(evt, env, src='Epix100a.', ctype=gu.PIXEL_MASK, calibdir=None, cmt=None, verb=False) :
    """Delete specified ctype from calibration constants.
    
    Parameters
    
    evt : psana.Event -> event time
    env : psana.Env -> full detector name for psana.Source 
    src : str - source short/full name, alias or full
    ctype : gu.CTYPE - enumerated calibration type, e.g.: gu.PIXEL_MASK
    calibdir : str - fallback path to calib dir (if xtc file is copied - calib and experiment name are lost)
    cmt   : str - comment
    verb  : bool - verbousity

    Back to :py:class:`PSCalib.DCMethods`
    """
    #metname = sys._getframe().f_code.co_name

    str_ctype = gu.dic_calib_type_to_name[ctype]
    if verb : print '  src: %s\n  ctype: %s\n  range: %s\n  calibdir:%s'%\
                    (src, str_ctype, range, calibdir)

    ofn = DCFileName(env, src, calibdir)
    if verb : ofn.print_attrs()

    fname = ofn.calib_file_path()
    if not is_good_fname(fname, verb) : return None

    cs = DCStore(fname)
    cs.load()
    #cs.print_obj()

    tdel = cs.mark_ctype(str_ctype, cmt=cmt)
    if tdel is None : return None 

    if verb : log.setPrintBits(02) # 0377

    cs.save()

    if verb :
        print 50*'_','\nDCStore.print_obj() after delete ctype %s' % tdel
        cs.print_obj()
    
    return tdel

#------------------------------

def print_file(fname) :
    """Prints content of the file.
    
    Parameters
    
    fname : str - full path to the file

    Back to :py:class:`PSCalib.DCMethods`
    """
    metname = sys._getframe().f_code.co_name

    if not is_good_fname(fname, True) : return

    cs = DCStore(fname)

    t0_sec = time()
    cs.load()
    print 'File content loading time (sec) = %.6f' % (time()-t0_sec)
    
    print 50*'_','\nDCStore.print_obj()' 
    cs.print_obj()

#------------------------------

def print_file_content(env, src='Epix100a.', calibdir=None) :
    """Defines the file name and prints file content.
    
    Parameters
    
    env : psana.Env -> full detector name for psana.Source 
    src : str - source short/full name, alias or full
    calibdir : str - fallback path to calib dir (if xtc file is copied - calib and experiment name are lost)

    Back to :py:class:`PSCalib.DCMethods`
    """
    #metname = sys._getframe().f_code.co_name

    ofn = DCFileName(env, src, calibdir)
    fname = ofn.calib_file_path()
    ofn.print_attrs()

    print_file(fname)

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
    cmt  = 'my comment is here'
    
    add_constants(nda, gevt, genv, gsrc, gctype, gcalibdir, vers, pred, succ, cmt, gverb)
    print '%s: constants added nda.shape=%s' % (metname, nda.shape)

#------------------------------

def test_add_text() :
    metname = sys._getframe().f_code.co_name
    print 20*'_', '\n%s' % metname

    import numpy as np

    data = 'Now we are going to save\n this little piece of text'
    vers = None
    pred = None
    succ = None
    ctype = gu.GEOMETRY
    cmt  = 'test_add_text'
    
    add_constants(data, gevt, genv, gsrc, ctype, gcalibdir, vers, pred, succ, cmt, gverb)
    print '%s: text is added to the file' % (metname)

#------------------------------

def test_add_constants_two() :
    metname = sys._getframe().f_code.co_name
    print 20*'_', '\n%s' % metname

    import numpy as np

    vers   = None
    pred   = None
    succ   = None
    ctype1 = gu.PIXEL_STATUS
    ctype2 = gu.PIXEL_MASK
    #nda   = np.zeros((32,185,388), dtype=np.float32)
    nda1   = np.ones((1000,1000), dtype=np.float32)
    nda2   = 2 * nda1
    cmt1   = 'my comment 1'
    cmt2   = 'my comment 2'
    
    add_constants(nda1, gevt, genv, gsrc, ctype1, gcalibdir, vers, pred, succ, cmt1, gverb)
    add_constants(nda2, gevt, genv, gsrc, ctype2, gcalibdir, vers, pred, succ, cmt2, gverb)
    print '%s: constants added ctype1=%s nda1.shape=%s' % (metname, str(ctype1), nda1.shape)
    print '%s: constants added ctype2=%s nda2.shape=%s' % (metname, str(ctype2), nda2.shape)

#------------------------------

def test_get_constants() :
    metname = sys._getframe().f_code.co_name
    print 20*'_', '\n%s' % metname

    vers = None
    nda = get_constants(gevt, genv, gsrc, gctype, gcalibdir, vers, gverb)

    print '%s: retrieved constants for vers %s' % (metname, str(vers))
    print '    nda:', nda
    if nda is not None : print '    nda.shape=%s' % (str(nda.shape))

#------------------------------

def test_delete_version() :
    metname = sys._getframe().f_code.co_name
    print 20*'_', '\n%s' % metname

    vers = None # for default - last version
    cmt  = 'my comment to delete version'
    vdel = delete_version(gevt, genv, gsrc, gctype, gcalibdir, vers, cmt, gverb)
    print '%s: deleted version %s' % (metname, str(vdel))

#------------------------------

def test_delete_range() :
    metname = sys._getframe().f_code.co_name
    print 20*'_', '\n%s' % metname

    range = '1474587520-end'
    cmt  = 'my comment to delete range'
    rdel = delete_range(gevt, genv, gsrc, gctype, gcalibdir, range, cmt, gverb)
    print '%s: deleted range %s' % (metname, str(rdel))

#------------------------------

def test_delete_ctype() :
    metname = sys._getframe().f_code.co_name
    print 20*'_', '\n%s' % metname

    cmt  = 'my comment to delete ctype'
    tdel = delete_ctype(gevt, genv, gsrc, gctype, gcalibdir, cmt, gverb)
    print '%s: deleted ctype %s' % (metname, str(tdel))

#------------------------------

def test_print_file() :
    metname = sys._getframe().f_code.co_name
    print 20*'_', '\n%s' % metname
    fname = './calib/epix100a/epix100a-3925999616-0996663297-3791650826-1232098304-0953206283-2655595777-0520093719.h5'
    print_file(fname)
    print '%s is completed' % (metname)

#------------------------------

def test_print_file_content() :
    metname = sys._getframe().f_code.co_name
    print 20*'_', '\n%s' % metname
    print_file_content(genv, gsrc, gcalibdir)
    print '%s is completed' % (metname)

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
    elif tname == '2' : test_add_constants_two()
    elif tname == '3' : test_get_constants()
    elif tname == '4' : test_print_file()
    elif tname == '5' : test_print_file_content()
    elif tname == '6' : test_delete_version()
    elif tname == '7' : test_delete_range()
    elif tname == '8' : test_delete_ctype()
    elif tname == '9' : test_add_text()
    else : print 'Not-recognized test name: %s' % tname
    msg = 'End of test %s, consumed time (sec) = %.6f' % (tname, time()-t0_sec)
    sys.exit(msg)
 
#------------------------------

if __name__ == "__main__" :
    do_test()

#------------------------------
