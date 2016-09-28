#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#------------------------------------------------------------------------

"""
:py:class:`PSCalib.DCUtils` - contains a set of utilities

Usage::

    # Import
    import PSCalib.DCUtils as gu

    # Methods
    # Get string with time stamp, ex: 2016-01-26T10:40:53
    ts    = gu.str_tstamp(fmt='%Y-%m-%dT%H:%M:%S', time_sec=None)

    usr   = gu.get_enviroment(env='USER')
    usr   = gu.get_login()
    host  = gu.get_hostname()
    cwd   = gu.get_cwd()

    etc.

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

@version $Id: 2013-03-08$

@author Mikhail S. Dubrovin
"""

#--------------------------------
__version__ = "$Revision$"
#--------------------------------

import sys
import os
import getpass
import socket
import numpy as np
from time import localtime, strftime #, time
from PSCalib.DCLogger import log
import PSCalib.GlobalUtils as gu

#------------------------------

class h5py_proxy :
    def __init__(self) :
        self.h5py = None
        self.Dataset = None
        self.Group = None
        self.File = None

    def fetch_h5py(self) :
        if self.h5py is None :
            import h5py
            self.h5py = h5py

#------------------------------
#h5py = h5py_proxy()
import h5py
#------------------------------

class Storage :
    def __init__(self) :
        self.psana = None
        self.dataset_t = h5py.Dataset
        self.group_t   = h5py.Group
        self.File      = h5py.File

#------------------------------
    
    def fetch_psana(self) :
        if sp.psana is None : import psana; sp.psana=psana
        return sp.psana

#------------------------------

sp = Storage()

#------------------------------

def str_tstamp(fmt='%Y-%m-%dT%H:%M:%S', time_sec=None) :
    """Returns string timestamp for specified format and time in sec or current time by default
    """
    return strftime(fmt, localtime(time_sec))

#------------------------------

def get_enviroment(env='USER') :
    """Returns the value of specified by string name environment variable
    """
    return os.environ[env]

#------------------------------

def get_login() :
    """Returns login name
    """
    #return os.getlogin()
    return getpass.getuser()

#------------------------------

def get_hostname() :
    """Returns login name
    """
    #return os.uname()[1]
    return socket.gethostname()

#------------------------------

def get_cwd() :
    """Returns current working directory
    """
    return os.getcwd()

#------------------------------

def create_directory_v0(dir, verb=False) : 
    if os.path.exists(dir) :
        if verb : print 'Directory exists: %s' % dir
    else :
        os.makedirs(dir)
        if verb : print 'Directory created: %s' % dir

#------------------------------

def create_directory(dir, mode=0775) :
    #print 'create_directory: %s' % dir
    if os.path.exists(dir) :
        log.debug('Directory exists: %s' % dir, __name__) 
    else :
        os.makedirs(dir, mode)
        #os.chmod(dir, mode)
        #os.system(cmd)
        log.info('Directory created: %s' % dir, __name__) 

#------------------------------

def create_path(path, depth=2, mode=0775) : 
    # Creates missing path for /reg/d/psdm/<INS>/<EXP>/calib/<dtype> beginning from calib
    subdirs = path.rstrip('/').rsplit('/', depth)
    log.debug('subdirs: %s' % str(subdirs), __name__)
    cpath = subdirs[0]
    length = len(subdirs)
    for i,sd in enumerate(subdirs[1:]) :
        cpath += '/%s'% sd 
        #if i<length-depth : continue
        create_directory(cpath, mode)
        #print 'create_path: %s' % cpath

    return os.path.exists(cpath)

#------------------------------

def save_string_as_dset(grp, name, s) :
    """Creates and returns the h5py dataset object with name for single string s
    """
    if s is None : return None
    #size = len(s)
    #create_dataset(name, shape=None, dtype=None, data=None, **kwds) 
    dset = grp.create_dataset(name, shape=(1,), dtype='S%d'%len(s)) #, data=s)
    dset[0] = s
    return dset

#------------------------------

def source_full_name(env, src) :
    """Returns full name like 'DetInfo(XppGon.0:Cspad2x2.0)' of the brief source or its alias
       using env.configStore().keys()
    """
    str_src = str(src)
    for k in env.configStore().keys() :
        if str_src in str(k.src())\
        or str_src == str(k.alias()) : return k.src()
    return None

#------------------------------

def dettype_from_str_source(src) :
    """Returns the detector type from full psana source name (Ex.: Cspad2x2 from DetInfo(XppGon.0:Cspad2x2.0) 
    """
    str_src = str(src)
    str_split = str_src.rsplit(':',1) 
    detname = str_split[1].split('.',1) if len(str_split)>1 else None
    return detname[0] if len(detname)>1 else None

#------------------------------

def string_from_source(source) :
  """Returns string like 'CxiDs2.0:Cspad.0' from 'DetInfo(CxiDs2.0:Cspad.0)'
     or 'DsaCsPad' from 'Source('DsaCsPad')' form input string or psana.Source object
  """
  str_src = str(source) 
  if '"' in str_src : return str_src.split('"')[1] # case of psana.String object
  str_split = str_src.rsplit('(',1) 
  return str_split[1].split(')',1)[0] if len(str_split)>1 else str_src

#------------------------------

def detector_full_name(env, src) :
    """Returns full detector name like 'XppGon.0:Cspad2x2.0' for short src, alias src, or psana.Source.
    """
    psana = sp.fetch_psana()

    str_src = str(src)
    str_src = string_from_source(str_src)
    if str_src is None : return None
    str_src = source_full_name(env, str_src)
    if str_src is None : return None
    return string_from_source(str_src)

##------------------------------

def psana_source(env, srcpar) :
    """returns psana.Source(src) from other psana.Source brief src or alias.
    
       Parameters

       srcpar  : str  - regular source or its alias, ex.: 'XppEndstation.0:Rayonix.0' or 'rayonix'
       set_sub : bool - default=True - propagates source parameter to low level package  
    """
    #print 'type of srcpar: ', type(srcpar)

    psana = sp.fetch_psana()
    
    src = srcpar if isinstance(srcpar, psana.Source) else psana.Source(srcpar)
    str_src = string_from_source(src)

    amap = env.aliasMap()
    psasrc = amap.src(str_src)
    source  = src if amap.alias(psasrc) == '' else amap.src(str_src)

    if not isinstance(source, psana.Source) : source = psana.Source(source)
    return source
 
#------------------------------

def get_subgroup(grp, subgr_name) :
    """For hdf5:
       returns subgroup of the group if it exists or creates and returns new subgroup
    """    
    #print 'YYY grp.name:', grp.name, '  subgr_name:', subgr_name
    if subgr_name in grp : return grp[subgr_name]
    return grp.create_group(subgr_name)

#------------------------------

def delete_object(grp, oname) :    
    """For hdf5: removes object from group.
    """    
    #print 'TTT grp.name: %s  delete object with name: %s' % (grp.name, oname)
    #t0_sec = time()
    if oname in grp : del grp[oname]
    #print 'TTT %s: time (sec) = %.6f' % (sys._getframe().f_code.co_name, time()-t0_sec)

#------------------------------

def save_object_as_dset(grp, name, shape=None, dtype=None, data=0) :
    """Saves object as h5py dataset

       Currently supports scalar int, double, string and numpy.array
    """
    #print 'XXX: save_object_as_dset '
    #print 'XXX grp.keys():',  grp.keys()
    #print 'XXX %s in grp.keys(): ' % name, name in grp.keys()
    if name in grp.keys() : return

    if isinstance(data, np.ndarray) :
        return grp.create_dataset(name, data=data)

    sh = (1,) if shape is None else shape
    if dtype is not None :
        return grp.create_dataset(name, shape=sh, dtype=dtype, data=data)

    if isinstance(data, str) :
        return save_string_as_dset(grp, name, data)

    if isinstance(data, int) :
        return grp.create_dataset(name, shape=sh, dtype='int', data=data)

    if isinstance(data, float) :
        return grp.create_dataset(name, shape=sh, dtype='double', data=data)

    log.warning("Can't save parameter: %s of %s in the h5py group: %s" % (name, str(dtype), grp.name), 'DCUtils.save_object_as_dset')

#------------------------------

def evt_time(evt) :
    """Returns event (double) time.
    """
    evid = evt.get(sp.fetch_psana().EventId)
    ttuple = evid.time()
    #print 'XXX time:',  ttuple
    return float(ttuple[0]) + float(ttuple[1])*1e-9

#------------------------------

def evt_fiducials(evt) :
    """Returns event fiducials.
    """
    evid = evt.get(sp.fetch_psana().EventId)
    return evid.fiducials()

#------------------------------

def test_source_full_name() :
    psana = sp.fetch_psana()
    ds = psana.DataSource('/reg/g/psdm/detector/data_test/types/0007-NoDetector.0-Epix100a.0.xtc')
    env=ds.env()    
    print 20*'_', '\n%s:' % sys._getframe().f_code.co_name
    print 'src="Epix"    :', source_full_name(env, 'Epix')
    print 'src="Cspad."  :', source_full_name(env, 'Cspad.')
    print 'src="Cspad"   :', source_full_name(env, 'Cspad')
    print 'src="cs140_0" :', source_full_name(env, 'cs140_0')

#------------------------------

def test_string_from_source() :
    psana = sp.fetch_psana()
    ds = psana.DataSource('/reg/g/psdm/detector/data_test/types/0007-NoDetector.0-Epix100a.0.xtc')
    env=ds.env()    
    source = psana_source(env, 'cs140_0')
    print 20*'_', '\n%s:' % sys._getframe().f_code.co_name
    print 'source', source
    print 'string_from_source', string_from_source(source)

#------------------------------

def test_psana_source() :
    psana = sp.fetch_psana()
    ds = psana.DataSource('/reg/g/psdm/detector/data_test/types/0007-NoDetector.0-Epix100a.0.xtc')
    env=ds.env()    
    print 20*'_', '\n%s:' % sys._getframe().f_code.co_name
    print 'psana_source(env, "Epix")    :', psana_source(env, 'Epix')
    print 'psana_source(env, "Cspad.")  :', psana_source(env, 'Cspad.')
    print 'psana_source(env, "Cspad")   :', psana_source(env, 'Cspad')
    print 'psana_source(env, "cs140_0") :', psana_source(env, 'cs140_0')

#------------------------------

def test_detector_full_name() :
    psana = sp.fetch_psana()
    ds = psana.DataSource('/reg/g/psdm/detector/data_test/types/0007-NoDetector.0-Epix100a.0.xtc')
    env=ds.env()
    print 20*'_', '\n%s:' % sys._getframe().f_code.co_name
    print 'src="Epix"                            :', detector_full_name(env, "Epix")
    print 'src=psana.Source("Epix"))             :', detector_full_name(env, psana.Source('Epix'))
    print 'src="DetInfo(NoDetector.0:Epix100a.0)":', detector_full_name(env, 'DetInfo(NoDetector.0:Epix100a.0)')
    print 'for alias src="cs140_0"               :', detector_full_name(env, 'cs140_0')

#------------------------------

def test_evt_time() :
    psana = sp.fetch_psana()
    ds = psana.DataSource('/reg/g/psdm/detector/data_test/types/0007-NoDetector.0-Epix100a.0.xtc')
    evt=ds.events().next()
    print 20*'_', '\n%s:' % sys._getframe().f_code.co_name
    t=evt_time(evt)
    print 'evt_time(evt) : %.9f' % t

#------------------------------

def test_misc() :
    print 20*'_', '\n%s:' % sys._getframe().f_code.co_name
    print 'get_enviroment(USER) : %s' % get_enviroment()
    print 'get_login()          : %s' % get_login()
    print 'get_hostname()       : %s' % get_hostname()
    print 'get_cwd()            : %s' % get_cwd()

#------------------------------

def do_test() :
    import sys; global sys
    tname = sys.argv[1] if len(sys.argv) > 1 else '0'
    print 50*'_', '\nTest %s:' % tname
    if   tname == '0' : test_misc(); test_source_full_name(); test_string_from_source();\
                        test_psana_source(); test_detector_full_name()
    elif tname == '1' : test_source_full_name()
    elif tname == '2' : test_string_from_source()
    elif tname == '3' : test_psana_source()
    elif tname == '4' : test_detector_full_name()
    elif tname == '5' : test_evt_time()
    else : print 'Not-recognized test name: %s' % tname
    sys.exit('End of test %s' % tname)
 
#------------------------------

if __name__ == "__main__" :
    do_test()

#------------------------------
