#!/usr/bin/env python
#------------------------------
""":py:class:`CalibParsBaseCameraV1` - holds basic calibration metadata parameters for associated detector.

@see :py:class:`PSCalib.CalibPars`, :py:class:`PSCalib.CalibParsStore`.

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

Revision: $Revision$

@version $Id$

@author Mikhail S. Dubrovin
"""
#------------------------------

class CalibParsBaseCameraV1 :

    ndim = 2 
    rows = 0 
    cols = 0 
    size = rows*cols 
    shape = (rows, cols)
    size_cm = 16
    shape_cm = (size_cm,)
    cmod = (1,50,50,100, 1,size,1,0, 0,0,0,0, 0,0,0,0)
        
    def __init__(self) : pass

#------------------------------

