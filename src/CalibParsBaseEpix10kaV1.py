#!/usr/bin/env python
#------------------------------
"""
:py:class:`CalibParsBaseEpix10kaV1` - holds basic calibration metadata parameters for associated detector
=========================================================================================================

See:
  -  :py:class:`GenericCalibPars`
  -  :py:class:`GlobalUtils`
  -  :py:class:`CalibPars`
  -  :py:class:`CalibParsStore` 
  -  :py:class:`CalibParsBaseAndorV1`
  -  :py:class:`CalibParsBaseAndor3dV1`
  -  :py:class:`CalibParsBaseCameraV1`
  -  :py:class:`CalibParsBaseCSPad2x2V1`
  -  :py:class:`CalibParsBaseCSPadV1`
  -  :py:class:`CalibParsBaseEpix100aV1`
  -  :py:class:`CalibParsBaseEpix10kaV1`
  -  :py:class:`CalibParsBasePnccdV1`
  -  :py:class:`CalibParsBasePrincetonV1`
  -  :py:class:`CalibParsBaseAcqirisV1`
  -  :py:class:`CalibParsBaseImpV1`

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

Author: Mikhail Dubrovin
"""
#------------------------------

class CalibParsBaseEpix10kaV1(object) :

    ndim = 4 # constants_shape = (7, 1, 352, 384) # data_shape = (16, 352, 384)
    segs = 1
    rows = 0 # 352->0 variable size array due to variable number of panels
    cols = 0 # 384 
    size = segs*rows*cols
    shape = (segs, rows, cols)
    size_cm = 16 
    shape_cm = (size_cm,)
    cmod = (3, 100, 100, 384, 0,0,0,0, 0,0,0,0, 0,0,0,0)
    # 3-median, 100-max threshold, 100-max correction, 384-pix group size
         
    def __init__(self) : pass

#------------------------------

