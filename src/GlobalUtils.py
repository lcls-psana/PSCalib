#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module CalibParsStore...
#
#------------------------------------------------------------------------

"""
:py:class:`PSCalib.GlobalUtils` - contains a set of utilities

Usage::

    # Import
    import PSCalib.GlobalUtils as gu

    # Initialization
    resp = gu.<method(pars)>

@see other interface methods in :py:class:`PSCalib.CalibPars`, :py:class:`PSCalib.CalibParsStore`

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

@version $Id: 2013-03-08$

@author Mikhail S. Dubrovin
"""

#--------------------------------
__version__ = "$Revision$"
#--------------------------------

import numpy as np

#import sys
#------------------------------
#------------------------------

# ATTENTION !!!!! ALL LISTS SHOULD BE IN THE SAME ORDER (FOR DICTIONARIES)

# Enumerated and named parameters

PEDESTALS    = 0
PIXEL_STATUS = 1
PIXEL_RMS    = 2
PIXEL_GAIN   = 3
PIXEL_MASK   = 4
PIXEL_BKGD   = 5
COMMON_MODE  = 6

calib_types  = ( PEDESTALS,   PIXEL_STATUS,   PIXEL_RMS,   PIXEL_GAIN,   PIXEL_MASK,   PIXEL_BKGD,   COMMON_MODE)
calib_names  = ('pedestals', 'pixel_status', 'pixel_rms', 'pixel_gain', 'pixel_mask', 'pixel_bkgd', 'common_mode')
calib_dtypes = ( np.float32,  np.uint16,      np.float32,  np.float32,   np.uint16,    np.float32,   np.double)

dic_calib_type_to_name  = dict(zip(calib_types, calib_names))
dic_calib_name_to_type  = dict(zip(calib_names, calib_types))
dic_calib_type_to_dtype = dict(zip(calib_types, calib_dtypes))

LOADED     = 1
DEFAULT    = 2
UNREADABLE = 3
UNDEFINED  = 4
WRONGSIZE  = 5
NONFOUND   = 6

calib_statvalues = ( LOADED,   DEFAULT,   UNREADABLE,   UNDEFINED,   WRONGSIZE,   NONFOUND)
calib_statnames  = ('LOADED', 'DEFAULT', 'UNREADABLE', 'UNDEFINED', 'WRONGSIZE', 'NONFOUND')

dic_calib_status_value_to_name = dict(zip(calib_statvalues, calib_statnames))
dic_calib_status_name_to_value = dict(zip(calib_statnames,  calib_statvalues))

#------------------------------
#------------------------------
#------------------------------
#------------------------------

UNDEFINED   = 0
CSPAD       = 1 
CSPAD2X2    = 2 
PRINCETON   = 3 
PNCCD       = 4 
TM6740      = 5 
OPAL1000    = 6 
OPAL2000    = 7 
OPAL4000    = 8 
OPAL8000    = 9 
ORCAFL40    = 10
EPIX        = 11
EPIX10K     = 12
EPIX100A    = 13
FCCD960     = 14
ANDOR       = 15
ACQIRIS     = 16
IMP         = 17
QUARTZ4A150 = 18
RAYONIX     = 19
EVR         = 20
FCCD        = 21
TIMEPIX     = 22
FLI         = 23
PIMAX       = 24

#XAMPS    # N/A data
#FEXAMP   # N/A data
#PHASICS  # N/A data
#OPAL1600 # N/A data
#EPIXS    # N/A data
#GOTTHARD # N/A data
""" Enumetated detector types"""

list_of_det_type = (UNDEFINED, CSPAD, CSPAD2X2, PRINCETON, PNCCD, TM6740, \
                    OPAL1000, OPAL2000, OPAL4000, OPAL8000, \
                    ORCAFL40, EPIX, EPIX10K, EPIX100A, FCCD960, ANDOR, ACQIRIS, IMP, QUARTZ4A150, RAYONIX,
                    EVR, FCCD, TIMEPIX, FLI, PIMAX)
""" List of enumetated detector types"""

list_of_det_names = ('UNDEFINED', 'Cspad', 'Cspad2x2', 'Princeton', 'pnCCD', 'Tm6740', \
                     'Opal1000', 'Opal2000', 'Opal4000', 'Opal8000', \
                     'OrcaFl40', 'Epix', 'Epix10k', 'Epix100a', 'Fccd960', 'Andor', 'Acqiris', 'Imp', 'Quartz4A150', 'Rayonix',\
                     'Evr', 'Fccd', 'Timepix', 'Fli', 'Pimax')
""" List of enumetated detector names"""

list_of_calib_groups = ('UNDEFINED',
                        'CsPad::CalibV1',
                        'CsPad2x2::CalibV1',
                        'Princeton::CalibV1',
                        'PNCCD::CalibV1',
                        'Camera::CalibV1',
                        'Camera::CalibV1',
                        'Camera::CalibV1',
                        'Camera::CalibV1',
                        'Camera::CalibV1',
                        'Camera::CalibV1',
                        'Epix::CalibV1',
                        'Epix10k::CalibV1',
                        'Epix100a::CalibV1',
                        'Camera::CalibV1',
                        'Andor::CalibV1',
                        'Acqiris::CalibV1',
                        'Imp::CalibV1',
                        'Camera::CalibV1',
                        'Camera::CalibV1',
                        'EvrData::CalibV1',
                        'Camera::CalibV1',
                        'Timepix::CalibV1',
                        'Fli::CalibV1',
                        'Pimax::CalibV1'
                        )
""" List of enumetated detector calibration groups"""

dic_det_type_to_name = dict(zip(list_of_det_type, list_of_det_names))
""" Dictionary for detector type : name"""

dic_det_type_to_calib_group = dict(zip(list_of_det_type, list_of_calib_groups))
""" Dictionary for detector type : group"""

#------------------------------
bld_names = \
['EBeam',
'PhaseCavity',
'FEEGasDetEnergy',
'Nh2Sb1Ipm01',
'HxxUm6Imb01',
'HxxUm6Imb02',
'HfxDg2Imb01',
'HfxDg2Imb02',
'XcsDg3Imb03',
'XcsDg3Imb04',
'HfxDg3Imb01',
'HfxDg3Imb02',
'HxxDg1Cam',
'HfxDg2Cam',
'HfxDg3Cam',
'XcsDg3Cam',
'HfxMonCam',
'HfxMonImb01',
'HfxMonImb02',
'HfxMonImb03',
'MecLasEm01',
'MecTctrPip01',
'MecTcTrDio01',
'MecXt2Ipm02',
'MecXt2Ipm03',
'MecHxmIpm01',
'GMD',
'CxiDg1Imb01',
'CxiDg2Imb01',
'CxiDg2Imb02',
'CxiDg4Imb01',
'CxiDg1Pim',
'CxiDg2Pim',
'CxiDg4Pim',
'XppMonPim0',
'XppMonPim1',
'XppSb2Ipm',
'XppSb3Ipm',
'XppSb3Pim',
'XppSb4Pim',
'XppEndstation0',
'XppEndstation1',
'MecXt2Pim02',
'MecXt2Pim03',
'CxiDg3Spec',
'Nh2Sb1Ipm02',
'FeeSpec0',
'SxrSpec0',
'XppSpec0',
'XcsUsrIpm01',
'XcsUsrIpm02',
'XcsUsrIpm03',
'XcsUsrIpm04',
'XcsSb1Ipm01',
'XcsSb1Ipm02',
'XcsSb2Ipm01',
'XcsSb2Ipm02',
'XcsGonIpm01',
'XcsLamIpm01',
'XppAin01',
'XcsAin01',
'AmoAin01']


#------------------------------

def det_type_from_source(source) :
    """ Returns enumerated detector type for string source
    """
    str_src = str(source)
    if   ':Cspad.'       in str_src : return CSPAD
    elif ':Cspad2x2.'    in str_src : return CSPAD2X2
    elif ':pnCCD.'       in str_src : return PNCCD
    elif ':Princeton.'   in str_src : return PRINCETON
    elif ':Andor.'       in str_src : return ANDOR
    elif ':Epix100a.'    in str_src : return EPIX100A
    elif ':Epix10k.'     in str_src : return EPIX10K
    elif ':Epix.'        in str_src : return EPIX
    elif ':Opal1000.'    in str_src : return OPAL1000
    elif ':Opal2000.'    in str_src : return OPAL2000
    elif ':Opal4000.'    in str_src : return OPAL4000
    elif ':Opal8000.'    in str_src : return OPAL8000
    elif ':Tm6740.'      in str_src : return TM6740
    elif ':OrcaFl40.'    in str_src : return ORCAFL40
    elif ':Fccd960.'     in str_src : return FCCD960
    elif ':Acqiris.'     in str_src : return ACQIRIS
    elif ':Imp.'         in str_src : return IMP
    elif ':Quartz4A150.' in str_src : return QUARTZ4A150
    elif ':Rayonix.'     in str_src : return RAYONIX
    elif ':Evr.'         in str_src : return EVR
    elif ':Fccd.'        in str_src : return FCCD
    elif ':Timepix.'     in str_src : return TIMEPIX
    elif ':Fli.'         in str_src : return FLI
    elif ':Pimax.'       in str_src : return PIMAX
    else                            : return UNDEFINED

#------------------------------
##-----------------------------
#------------------------------

def string_from_source(source) :
  """Returns string like "CxiDs2.0:Cspad.0" from "Source('DetInfo(CxiDs2.0:Cspad.0)')" or "Source('DsaCsPad')"
  """
  str_in_quots = str(source).split('"')[1]
  str_split = str_in_quots.split('(') 
  return str_split[1].rstrip(')') if len(str_split)>1 else str_in_quots

#------------------------------

def merge_masks(mask1=None, mask2=None) :
    """Merging masks using rule: (0,1,0,1)^(0,0,1,1) = (0,0,0,1) 
    """
    if mask1 is None : return mask2
    if mask2 is None : return mask1

    shape1 = mask1.shape
    shape2 = mask2.shape

    if shape1 != shape2 :
        if len(shape1) > len(shape2) : mask2.shape = shape1
        else                         : mask1.shape = shape2

    return np.logical_and(mask1, mask2)

##-----------------------------

def reshape_nda_to_2d(arr) :
    """Reshape np.array to 2-d
    """
    sh = arr.shape
    if len(sh)<3 : return arr
    arr.shape = (arr.size/sh[-1], sh[-1])
    return arr

##-----------------------------

def reshape_nda_to_3d(arr) :
    """Reshape np.array to 3-d
    """
    sh = arr.shape
    if len(sh)<4 : return arr
    arr.shape = (arr.size/sh[-1]/sh[-2], sh[-2], sh[-1])
    return arr

#------------------------------
#------------------------------
#------------------------------
