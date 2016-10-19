#-----------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#-----------------------------------------------------------------------------

"""
:py:class:`PSCalib.DCFileName` - file name object for Detector Calibration Store (DCS) project.

Usage::

    # Import
    from PSCalib.DCFileName import DCFileName

    # Instatiation
    o = DCFileName(env, 'Epix', calibdir='path-to/calib')
    # Methods
    o.set_dettype(env, src)
    o.set_detid(env, src)
    status = o.make_path_to_calib_file(mode=0770)

    dt  = o.dettype()
    did = o.detid()
    dn  = o.detname()

    fname = o.calib_file_name()      # e.g., epix100a-3925868555.h5
    fdir  = o.calib_file_dir()       # e.g., /reg/neh/home4/dubrovin/LCLS/rel-calib/calib
    fpath = o.calib_file_path()      # e.g., /reg/neh/home4/dubrovin/LCLS/rel-calib/calib/epix100a/epix100a-3925868555.h5
    fdir  = o.calib_file_dir_repo()  # e.g., /reg/g/psdm/detector/calib/epix100a/
    fpath = o.calib_file_path_repo() # e.g., /reg/g/psdm/detector/calib/epix100a/epix100a-3925868555.h5
    o.print_attrs() # print attributes
    o.log_attrs()  # dump attributes in the logger
    s = o.str_attrs() # returns a string of attributes


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
from   PSCalib.DCLogger import log
import PSCalib.DCUtils as gu
import PSCalib.DCDetectorId as did
from PSCalib.DCConfigParameters import cp

#------------------------------

class DCFileName() :
    """File name generator object for Detector Calibration Store (DCS) project. 

    Parameters
    
    evt : psana.Event -> event time
    src : str - source short/full name, alias or full
    calibdir : str - fallback path to calib dir (if xtc file is copied - calib and experiment name are lost)
    """

    fname_ext = 'h5'
    notype    = 'notype'
    noid      = 'noid'

    def __init__(self, env, src, calibdir=None) :
        self._name = self.__class__.__name__
        log.debug('c-tor', self._name)
        self._env = env   
        self._src = src
        self._set_detname(env, src)
        self._set_calib_dir(env, calibdir)


    def str_attrs(self) :
        return '%s attributes:'   % self._name\
            + '\n  env      : %s' % self._env\
            + '\n  src      : %s' % self._src\
            + '\n  src_name : %s' % self._src_name\
            + '\n  dettype  : %s' % self.dettype()\
            + '\n  detid    : %s' % self.detid()\
            + '\n  detname  : %s' % self.detname()\
            + '\n  file name: %s' % self.calib_file_name()\
            + '\n  calibdir : %s' % self._calibdir\
            + '\n  file dir : %s' % self.calib_file_dir()\
            + '\n  file path: %s' % self.calib_file_path()\
            + '\n  repo dir : %s' % self.calib_file_dir_repo()\
            + '\n  repo path: %s' % self.calib_file_path_repo()


    def print_attrs(self) :
        print self.str_attrs()


    def log_attrs(self) :
        log.info(self.str_attrs(), self._name)


    def set_dettype(self, env, src) :
        self._src_name = gu.source_full_name(env, src) # DetInfo(XppGon.0:Cspad2x2.0)
        if self._src_name is None :
            self._dettype = self.notype
            return
        self._dettype = gu.dettype_from_str_source(self._src_name).lower() # cspad2x2
        if self._dettype is None : 
            self._dettype = self.notype


    def set_detid(self, env, src) :
        if self._dettype == 'epix100a': self._detid = did.id_epix(env, src)
        else                          : self._detid = did.id_det_noid(env, src)
        if self._detid is None        : self._detid = self.noid


    def _set_detname(self, env, src) : 
        self.set_dettype(env, src)
        self.set_detid(env, self._src_name)
        self._detname = '%s-%s' % (self._dettype, self._detid.replace(':','-'))


    def _set_calib_dir(self, env, calibdir=None) :
        if calibdir is not None and calibdir != 'None' : 
            self._calibdir = calibdir
            return

        cdir = env.calibDir()
        self._calibdir = cdir 
        self._calibdir = None if '///' in cdir else cdir # /reg/d/psdm///calib


    def dettype(self) :
        """Returns detector id, ex.: epix100a"""
        return self._dettype


    def detid(self) :
        """Returns detector id, ex.: 3925868555"""
        return self._detid


    def detname(self) :
        """Returns detector name, ex.: epix100a-3925868555"""
        return self._detname


    def calib_file_dir(self) :
        """Returns file directory name, ex.: .../calib/epix100a/"""
        if self._calibdir is None : return None
        else : return '%s/%s' % (self._calibdir, self._dettype)


    def calib_file_dir_repo(self) :
        """Returns repository directory, ex.: /reg/g/psdm/detector/calib/epix100a/"""
        return '%s/%s' % (cp.dir_repo.value(), self._dettype)


    def calib_file_name(self) :
        """Returns file name, ex.: epix100a-3925868555.h5"""
        return '%s.%s' % (self._detname, self.fname_ext)


    def calib_file_path(self) :
        """Returns path to the file, ex.: .../calib/epix100a/epix100a-3925868555.h5"""
        if self._calibdir is None : return None
        else : return '%s/%s/%s.%s' % (self._calibdir, self._dettype, self._detname, self.fname_ext)


    def calib_file_path_repo(self) :
        """Returns path to the file in repository, ex.: /reg/g/.../calib/epix100a/epix100a-3925868555.h5"""
        return '%s/%s/%s.%s' % (cp.dir_repo.value(), self._dettype, self._detname, self.fname_ext)


    def make_path_to_calib_file(self, depth=2, mode=0775) :
        """Creates path beginning from calib directory, ex.: .../calib/epix100a/
        Returns True if path created and exists.
        """
        fdir = self.calib_file_dir()
        #print 'XXX:fdir', fdir
        return gu.create_path(fdir, depth, mode)


    def _parse_path_to_file(self, pathf) :
        #log.debug('_set_file_name', self._name)

        if os.path.exists(pathf) :
            self.path, self.fname = os.path.split(pathf)
            #fname, ext = os.path.splitext(fnamext)

        if pathf is None\
        or pathf is '' : raise IOError('%s: File name "%s" is not allowed'%(self._name, pathf))

        self.path = pathf 

        # add .h5 extension if missing
        self.fname = '%s.h5'%self.fname if self.ext != 'h5' else self.fname

        # check if fname needs in default path
        if pathf == '' : self.fname = os.path.join(cp.repo.value(), self.fname)
        
        #if not os.path.lexists(fname) : 
        log.info('Set file name: %s'%self.fname, self._name)


    def __del__(self) :
        log.debug('d-tor', self._name)

#------------------------------

def test_DCFileName() :
    print 20*'_', '\n%s:' % sys._getframe().f_code.co_name

    import psana
    ds = psana.DataSource('/reg/g/psdm/detector/data_test/types/0007-NoDetector.0-Epix100a.0.xtc')
    env=ds.env()

    #evt, env, src = None, None, None
    ofn1 = DCFileName(env, 'Imp'); ofn1.print_attrs()
    ofn2 = DCFileName(env, 'Epix', calibdir='path-to/calib'); ofn2.print_attrs()
    ofn3 = DCFileName(env, 'cs140_0'); ofn3.print_attrs()
    ofn4 = DCFileName(env, 'Cspad.', calibdir='path-to/calib'); ofn4.print_attrs()
    ds = psana.DataSource('exp=cxif5315:run=129')
    env=ds.env()
    ofn5 = DCFileName(env, 'Cspad.'); ofn5.print_attrs()

#------------------------------

def test_make_path_to_calib_file() :
    print 20*'_', '\n%s:' % sys._getframe().f_code.co_name

    import psana
    ds = psana.DataSource('/reg/g/psdm/detector/data_test/types/0007-NoDetector.0-Epix100a.0.xtc')

    ofn = DCFileName(ds.env(), 'Epix', calibdir='%s/calib' % gu.get_cwd())
    #ofn = DCFileName(ds.env(), 'Epix', calibdir='./calib')
    ofn.print_attrs()
    ofn.make_path_to_calib_file(mode=0770)

#------------------------------

def do_test() :
    log.setPrintBits(0377)

    tname = sys.argv[1] if len(sys.argv) > 1 else '0'
    print 50*'_', '\nTest %s:' % tname
    if   tname == '0' : test_DCFileName() # ; test_DCFileName()
    elif tname == '1' : test_DCFileName()
    elif tname == '2' : test_make_path_to_calib_file()
    else : print 'Not-recognized test: %s' % tname
    sys.exit('End of test %s' % tname)

#------------------------------

if __name__ == "__main__" :
    import sys; global sys
    do_test()

#------------------------------
