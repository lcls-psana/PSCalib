#--------------------------------------------------------------------------
# File and Version Information:
#  $Id:DCConfigParameters.py 11923 2016-05-17 21:14:33Z dubrovin@SLAC.STANFORD.EDU $
#
# Description:
#------------------------------------------------------------------------

"""DCConfigParameters - class supporting configuration parameters for application.

@see base class :py:class:`CalibManager.ConfigParameters`

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

@version $Id:DCConfigParameters.py 11923 2016-05-17 21:14:33Z dubrovin@SLAC.STANFORD.EDU $

@author Mikhail S. Dubrovin
"""
#---------------------------------
__version__ = "$Revision$"
__author__ = "Mikhail S. Dubrovin"
#---------------------------------

from PSCalib.DCLogger import log
from CalibManager.ConfigParameters import ConfigParameters

#----------------------------

class DCConfigParameters(ConfigParameters) :
    """A storage of configuration parameters for Detector Calibration Store (DCS) project.
    """

    def __init__(self, fname=None) :
        """Constructor.
           - fname the file name with configuration parameters, if not specified then default value.
        """
        ConfigParameters.__init__(self)
        self.name = self.__class__.__name__
        self.fname_cp = 'confpars-dcs.txt' # Re-define default config file name
        log.info('In %s c-tor', self.name)

        self.declareParameters()
        self.readParametersFromFile(fname)
  
#-----------------------------
        
    def declareParameters(self) :
        # Possible typs for declaration : 'str', 'int', 'long', 'float', 'bool'
        # Logger.py
        self.log_level = self.declareParameter(name='LOG_LEVEL_OF_MSGS', val_def='info',      type='str' )
        self.log_file  = self.declareParameter(name='LOG_FILE_NAME',     val_def='./log.txt', type='str' )
        self.dir_repo  = self.declareParameter(name='CDS_DIR_REPO',      val_def='/reg/d/psdm/detector/calib', type='str' )
        #self.dir_repo  = self.declareParameter(name='CDS_DIR_REPO',      val_def='/reg/g/psdm/detector/calib', type='str' )

#------------------------------
    
cp = DCConfigParameters()

#------------------------------

def test_DCConfigParameters() :
    log.setPrintBits(0377)
    cp.readParametersFromFile()
    cp.printParameters()
    cp.log_level.setValue('debug')
    cp.saveParametersInFile()

#------------------------------

if __name__ == "__main__" :
    import sys
    test_DCConfigParameters()
    sys.exit(0)

#------------------------------
