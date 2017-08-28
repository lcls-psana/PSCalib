#!/usr/bin/env python
#------------------------------
"""
---
:py:class:`CalibPars` - abstract interface for access to calibration parameters.

Methods of this class should be re-implemented in derived classes with name pattern CalibPars<Detector>
for different type of detectore. For example, CSPAD can be implemented in class :py:class:`PSCalib.CalibParsCspadV1`
which enherits from :py:class:`PSCalib.CalibPars`, etc.
Currently implementation of this interface for all detectors is done in class :py:class:`PSCalib.GenericCalibPars`.
Access to all detectors is available through the factory method in class :py:class:`PSCalib.CalibParsStore`.

Usage of (implemented) interface methods::

    from PSCalib.CalibPars import CalibPars
    import PSCalib.GlobalUtils as gu

    cp = CalibPars()
    cp.print_attrs()

    size = cp.pedestals()
    size = cp.pixel_status()
    size = cp.pixel_rms()
    size = cp.pixel_gain()
    size = cp.pixel_mask()
    size = cp.pixel_bkgd()
    size = cp.common_mode()

    ctype = gu.PEDESTALS # ex.: gu.PIXEL_STATUS, gu.PIXEL_RMS, gu.PIXEL_MASK, etc.
    size = cp.ndim(ctype)
    size = cp.size(ctype)
    size = cp.shape(ctype)
    size = cp.status(ctype)

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


This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

Author: Mikhail Dubrovin

---
"""
#------------------------------

import sys
#import os
#import math
#import numpy as np
import PSCalib.GlobalUtils as gu

#------------------------------

class CalibPars :

#------------------------------

    def __init__(self) : 
        """ Constructor
        """
        self.wmsg = 'WARNING! %s.%s' % (self.__class__.__name__,\
                    '%s - interface method from the base class needs to be re-implemented in the derived class.')
        pass

#------------------------------

    def print_attrs(self) :
        """ Prints attributes
        """
        print self.wmsg % 'print_attrs()'

#------------------------------

    def pedestals(self) :
        """ Returns pedestals
        """
        print self.wmsg % 'pedestals()'

#------------------------------

    def pixel_status(self) :
        """ Returns pixel_status
        """
        print self.wmsg % 'pixel_status()'

#------------------------------

    def pixel_rms(self) :
        """ Returns pixel_rms
        """
        print self.wmsg % 'pixel_rms()'

#------------------------------

    def pixel_gain(self) :
        """ Returns pixel_gain
        """
        print self.wmsg % 'pixel_gain()'

#------------------------------

    def pixel_mask(self) :
        """ Returns pixel_mask
        """
        print self.wmsg % 'pixel_mask()'

#------------------------------

    def pixel_bkgd(self) :
        """ Returns pixel_bkgd
        """
        print self.wmsg % 'pixel_bkgd()'

#------------------------------

    def common_mode(self) :
        """ Returns common_mode
        """
        print self.wmsg % 'common_mode()'

#------------------------------
#------------------------------
#------------------------------
#------------------------------

    def ndim(self, ctype=gu.PEDESTALS) :
        """ Returns ndim
        """
        print self.wmsg % 'ndim(ctype)'

#------------------------------

    def shape(self, ctype=gu.PEDESTALS) :
        """ Returns shape
        """
        print self.wmsg % 'shape(ctype)'

#------------------------------

    def size(self, ctype=gu.PEDESTALS) :
        """ Returns size
        """
        print self.wmsg % 'size(ctype)'

#------------------------------

    def status(self, ctype=gu.PEDESTALS) :
        """ Returns status
        """
        print self.wmsg % 'size(status)'

#------------------------------
#------------------------------
#------------------------------
#------------------------------

if __name__ == "__main__" :
    print 'Module %s describes interface methods to access calibration parameters' % sys.argv[0]

    cp = CalibPars()
    cp.print_attrs()
    size = cp.size()
    size = cp.shape()
    size = cp.status()
    sys.exit ('End of %s' % sys.argv[0])

#------------------------------
#------------------------------
#------------------------------
#------------------------------


