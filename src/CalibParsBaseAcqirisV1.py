#!/usr/bin/env python
#------------------------------
""":py:class:`CalibParsBaseAcqirisV1` - holds basic calibration metadata parameters for associated detector.

See :py:class:`PSCalib.CalibPars`, :py:class:`PSCalib.CalibParsStore`.

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

:Author: Mikhail Dubrovin
"""
#------------------------------

class CalibParsBaseAcqirisV1 :

    ndim = 2 
    rows = 0 # VARIABLE SHAPE DATA PARAMETERS WILL BE TAKEN FROM FILE METADATA
    cols = 0 # VARIABLE SHAPE DATA PARAMETERS WILL BE TAKEN FROM FILE METADATA
    size = rows*cols
    shape = (rows, cols)
    size_cm = 16 
    shape_cm = (size_cm,)
    cmod = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        
    def __init__(self) : pass

#------------------------------

