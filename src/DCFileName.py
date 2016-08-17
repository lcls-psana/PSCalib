#-----------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#-----------------------------------------------------------------------------

"""
:py:class:`PSCalib.DCFileName` - file name object for Detector Calibration Store (DCS) project.

Usage::

    # Import
    from PSCalib.DCFileName import DCFileName

    fn = DCFileName()

@see implementation in :py:class:`PSCalib.DCStore`,
                       :py:class:`PSCalib.DCType`,
                       :py:class:`PSCalib.DCRange`,
                       :py:class:`PSCalib.DCVersion`,
                       :py:class:`PSCalib.DCBase`
                       :py:class:`PSCalib.DCFileName`

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

@version $Id$

@author Mikhail S. Dubrovin
"""

#---------------------------------
__version__ = "$Revision$"
#---------------------------------

import os
from PSCalib.DCLogger import log

#------------------------------

class DCFileName() :
    """File name object for Detector Calibration Store (DCS) project
    """
    def __init__(self, pathf) :
        self.name = self.__class__.__name__
        log.debug('c-tor input pathf: %s'%pathf, self.name)
        self.path = ''   # path to the directory where file is located
        self.dettype = ''# <dettype>
        self.detid = ''  # <detid>
        self.ext = '.h5' # file extension preceded by dot
        self.fname = ''  # <dettype>-<detid>.py
        self.pathf = ''  # full path to file 
        self._parse_path_to_file(pathf)


    def _parse_path_to_file(self, pathf) :
        #log.debug('_set_file_name', self.name)

        if os.path.exists(pathf) :
            self.path, self.fname = os.path.split(pathf)
            #fname, ext = os.path.splitext(fnamext)

        if pathf is None\
        or pathf is '' : raise IOError('%s: File name "%s" is not allowed'%(self.name, pathf))

        self.path = pathf 

        # add .h5 extension if missing
        self.fname = '%s.h5'%fname if ext != 'h5' else fname

        # check if fname needs in default path
        if path == '' : self.fname = os.path.join(cp.repo.value(), self.fname)
        
        #if not os.path.lexists(fname) : 
        log.info('Set file name: %s'%self.fname, self.name)


    def __del__(self) :
        log.debug('d-tor', self.name)

#------------------------------

def test_DCFileName(path) :
    log.setPrintBits(0377) 
    fn = DCFileName(path)

#------------------------------

if __name__ == "__main__" :
    import sys
    test_DCFileName('cspad-654321')
    sys.exit('End of %s test.' % sys.argv[0])

#------------------------------
