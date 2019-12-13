#!/usr/bin/env python
#------------------------------
"""
Class :py:class:`CalibParsBaseUxiV1` holds basic calibration metadata parameters for associated detector
============================================================================================================

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
  -  :py:class:`CalibParsBasePnccdV1`
  -  :py:class:`CalibParsBasePrincetonV1`
  -  :py:class:`CalibParsBaseAcqirisV1`
  -  :py:class:`CalibParsBaseImpV1`
  -  :py:class:`CalibParsBaseUxiV1`

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

Author: Mikhail Dubrovin
"""
#------------------------------

class CalibParsBaseUxiV1(object) :

    ndim = 3
    segs = 0 # 1-8 variable size
    rows = 0 # 1024 - variable size array due to re-binning
    cols = 0 # 512
    size = segs*rows*cols
    shape = (segs, rows, cols)
    size_cm = 16
    shape_cm = (size_cm,)
    cmod = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0) # cm correction is turned off
    def __init__(self) : pass

#------------------------------

