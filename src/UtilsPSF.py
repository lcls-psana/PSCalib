#!/usr/bin/env python
"""
:py:class:`UtilsPSF` - module for geometry conversion from psana to psf format
==============================================================================

    import PSCalib.UtilsPSF as ups
    psf,sego = ups.psf_from_geo(geo)
    psf,sego = ups.psf_from_file(fname_geometry)
    print(ups.info_psf(psf))

Created: 2021-12-06 by Mikhail Dubrovin
"""

import sys
import logging
logger = logging.getLogger(__name__)
from PSCalib.GeometryAccess import GeometryAccess
from PSCalib.GlobalUtils import CFRAME_LAB, CFRAME_PSANA
from Detector.GlobalUtils import info_ndarr

import numpy as np

def panel_psf_v0(sego, x, y, z):
    """Returns psf vectors for segment ASICs.
       Parameters:
       - sego [SegGeometry] - segment geometry object
       - x, y, z [float] - segment pixel coordimane arrays (in the detector coordinate frame)
    """
    lst = []
    for (r0,c0) in sego.asic0indices():
        vp = x[r0,c0], y[r0,c0], z[r0,c0]
        vs = x[r0,c0+1]-x[r0,c0],\
             y[r0,c0+1]-y[r0,c0],\
             z[r0,c0+1]-z[r0,c0]
        vf = x[r0+1,c0]-x[r0,c0],\
             y[r0+1,c0]-y[r0,c0],\
             z[r0+1,c0]-z[r0,c0]
        lst.append((vp, vs, vf))
    return lst


def panel_psf(sego, x, y, z):
    """Returns psf vectors for segment ASICs.
       Parameters:
       - sego [SegGeometry] - segment geometry object
       - x, y, z [float] - segment pixel coordimane arrays (in the detector coordinate frame)
    """
    return [((x[r0,c0], y[r0,c0], z[r0,c0]),\
            (x[r0,c0+1]-x[r0,c0],\
             y[r0,c0+1]-y[r0,c0],\
             z[r0,c0+1]-z[r0,c0]),\
            (x[r0+1,c0]-x[r0,c0],\
             y[r0+1,c0]-y[r0,c0],\
             z[r0+1,c0]-z[r0,c0])) for (r0,c0) in sego.asic0indices()]


def psf_from_file(fname, cframe=CFRAME_LAB):
    """
    Parameters:
    -----------
       - fname [str] - psana detector geometry file name.
       - cframe [int] - 0/1 = CFRAME_PSANA/CFRAME_LAB - psana/LAB coordinate frame.
    """
    logger.info('load geometry from file %s' % fname)
    geo = GeometryAccess(fname, 0, use_wide_pix_center=False)
    return psf_from_geo(geo, cframe)


def psf_from_geo(geo, cframe=CFRAME_LAB):
    """
    Parameters:
    -----------
       - geo [GeometryAccess] - psana geometry description object.
       - cframe [int] - 0/1 = CFRAME_PSANA/CFRAME_LAB - psana/LAB coordinate frame.
    """
    logger.info('psf_from_geo - converts geometry constants from psana to psf format')

    geo1 = geo.get_seg_geo() #sgs.Create(segname=segname, pbits=0)
    sego = geo1.algo
    srows, scols = sego.shape()

    logger.info('\n  segment id: %s oindex: %d' % (geo1.oname, geo1.oindex)\
      + '\n  per ASIC info'\
      + '\n  SegGeometry implementation class: %s' % sego.name()\
      + '\n  asic0ind: %s' % str(sego.asic0indices())\
      + '\n  arows: %d acols: %d' % sego.asic_rows_cols()\
      + '\n  ssize: %d' % sego.size()\
      + '\n  sego.shape(): %s' % str(sego.shape())\
      + '\n  pix_size, um: %f' % sego.pixel_scale_size()\
      + '\n  nasics_in_rows: %d nasics_in_cols: %d' % sego.number_of_asics_in_rows_cols()\
    )

    x, y, z = geo.get_pixel_coords(oname=None, oindex=0, do_tilt=True, cframe=cframe)
    logger.debug(info_ndarr(x, name='x', first=0, last=10))
    logger.debug(info_ndarr(y, name='y', first=0, last=10))

    nsegs = x.size/sego.size()
    logger.info('nsegs in geometry: %d' % nsegs)

    shape = (nsegs, srows, scols)
    logger.info('geo shape: %s' % str(shape))
    x.shape = y.shape = z.shape = shape

    lst = None
    for n in range(nsegs):
        incr = panel_psf(sego, x[n,:], y[n,:], z[n,:])
        if lst is None: lst = incr
        else: lst += incr

    return lst, sego


def info_psf(psf,\
      fmtp='\np=(%12.2f, %12.2f, %12.2f)',\
      fmts='  s=(%8.2f, %8.2f, %8.2f)',\
      fmtf='  f=(%8.2f, %8.2f, %8.2f)', title=''):
    s = title
    fmt = fmtp + fmts + fmtf
    for (px,py,pz), (sx,xy,xz), (fx,fy,fz) in psf:
        s += fmt % (px,py,pz,  sx,xy,xz,  fx,fy,fz)
    return s


def savetext_psf(psf, fname='psf.txt',\
                 fmtp='\n%12.3f %12.3f %12.3f',\
                 fmts='  %8.3f %8.3f %8.3f',\
                 fmtf='  %8.3f %8.3f %8.3f', title=''):
    """Save psf vectors as text, each line has 3 vecotrs for ASIC: position, slow, fast.
    """
    if fname is None:
       logger.info('savetext_psf file name is None, file is not saved')
       return

    f = open(fname,'w')
    f.write(info_psf(psf, fmtp, fmts, fmtf, title))
    f.close()
    logger.info('geometry constants in psf format saved as text in: %s' % fname)


def save_psf(psf, fname='psf.npy'):
    """Save psf vectors as numpy array
    """
    nda = np.array(psf)
    np.save(fname, nda)
    logger.info('geometry constants in psf format saved as numpy array in: %s' % fname)


def load_psf(fname):
    assert isinstance(fname, str) and fname.split('.')[-1]=='npy', 'file name is not a str object or not *.npy'
    return np.load(fname)





def data_to_psf(sego, data):
    """
       Parameters:
       - sego [SegmentGeometry] - psana segment geometry description object.
       - data [np.array] - psana data object.
    """
    logger.info('data_to_psf - conversion of psana data to psf shape')

    srows, scols = sego.shape()

    logger.info('  per ASIC info'\
      + '\n  SegGeometry implementation class: %s' % sego.name()\
      + '\n  asic0ind: %s' % str(sego.asic0indices())\
      + '\n  arows: %d acols: %d' % sego.asic_rows_cols()\
      + '\n  ssize: %d' % sego.size()\
      + '\n  sego.shape(): %s' % str(sego.shape())\
      + '\n  pix_size, um: %f' % sego.pixel_scale_size()\
      + '\n  nasics_in_rows: %d nasics_in_cols: %d' % sego.number_of_asics_in_rows_cols()\
    )

    nsegs = data.size/sego.size()
    shape = (nsegs, srows, scols)
    logger.info('nsegs in data: %d shape: %s per-segment shape: %s' % (nsegs, str(data.shape), str(shape)))

    data_psf = None
    for n in range(nsegs):
        incr = panel_psf(sego, x[n,:], y[n,:], z[n,:])
        if data_psf is None: data_psf = incr
        else: data_psf += incr

    return data_psf







if __name__ == "__main__":

  logging.basicConfig(format='[%(levelname).1s] %(filename)s L%(lineno)04d: %(message)s', level=logging.DEBUG)

  scrname = sys.argv[0].rsplit('/')[-1]
  tname = sys.argv[1] if len(sys.argv)>1 else '1'

  fn_geo_cspadv1        = '/reg/d/psdm/CXI/cxitut13/calib/CsPad::CalibV1/CxiDs1.0:Cspad.0/geometry/0-end.data'
  fn_geo_cspad_cxi      = '/reg/g/psdm/detector/data2_test/geometry/geo-cspad-cxi.data'
  fn_geo_cspad_xpp      = '/reg/g/psdm/detector/data2_test/geometry/geo-cspad-xpp.data'
  fn_geo_epix10ka2m_16  = '/reg/g/psdm/detector/data2_test/geometry/geo-epix10ka2m-16-segment.data'
  fn_geo_epix10ka2m_def = '/reg/g/psdm/detector/data2_test/geometry/geo-epix10ka2m-default.data'
  fn_geo_jungfrau_8     = '/reg/g/psdm/detector/data2_test/geometry/geo-jungfrau-8-segment.data'
  fn_geo_pnccd_amo      = '/reg/g/psdm/detector/data2_test/geometry/geo-pnccd-amo.data'

  fn_data_epix10ka2m = '/reg/g/psdm/detector/data_test/npy/nda-mfxc00118-r0184-epix10ka2m-silver-behenate-max.txt'
  fn_data_cspad      = '/reg/g/psdm/detector/data_test/npy/nda-mfx11116-r0624-e005365-MfxEndstation-0-Cspad-0-max.txt'
  fn_data_jungfrau   = '/reg/g/psdm/detector/data_test/npy/nda-cxilv9518-r0008-jungfrau-lysozyme-max.npy'

  def load_data_fropm_file(fname):
    assert isinstance(fname, str), 'file name is not a str'
    ext = fname.split('.')[-1]
    if ext=='npy': return np.load(fname)
    else:
        from PSCalib.NDArrIO import load_txt
        return load_txt(fname)
#        from PSCalib.GlobalUtils import load_textfile
#        return load_textfile(fname)


  def test_geo_from_file(fname_geo):
    import psana
    from PSCalib.GeometryAccess import GeometryAccess
    from Detector.GlobalUtils import info_ndarr
    geo = GeometryAccess(fname_geo)
    X, Y, Z = geo.get_pixel_coords()
    print(info_ndarr(X,'X:'))
    print(info_ndarr(Y,'Y:'))
    print(info_ndarr(Z,'Z:'))


  def test_psf_from_file(fname_geo):
    #import PSCalib.UtilsPSF as ups
    #psf,sego = ups.psf_from_geo(geo)
    psf,sego = psf_from_file(fname_geo)
    print(type(sego))
    print(info_psf(psf, title='info_psf: psf.shape: %s \npsf vectors:' % (str(np.array(psf).shape))))
    savetext_psf(psf, fname='psf-test.txt')
    save_psf(psf, fname='psf-test.npy')


  def test_load_psf(fname='psf-test.npy'):
    psf = load_psf(fname)
    print(info_psf(psf, title='info_psf: psf.shape: %s \npsf vectors:' % (str(np.array(psf).shape))))


  def test_load_data_fropm_file(fname=fn_data_epix10ka2m):
    data = load_data_fropm_file(fname)
    print(info_ndarr(data, name='data', first=0, last=10))


  def test_data_to_psf(fname_geo, fname_data):
    #import PSCalib.UtilsPSF as ups
    #psf,sego = ups.psf_from_geo(geo)
    psf,sego = psf_from_file(fname_geo)
    print(type(sego))
    print(info_psf(psf, title='info_psf: psf.shape: %s \npsf vectors:' % (str(np.array(psf).shape))))

    data = load_data_fropm_file(fname_data)
    print(info_ndarr(data, name='data', first=0, last=10))


    print(20*'TBD ')






  if   tname=='0': test_geo_from_file(fn_geo_cspad_cxi)
  elif tname=='1': test_psf_from_file(fn_geo_cspad_cxi)
  elif tname=='2': test_psf_from_file(fn_geo_cspad_xpp)
  elif tname=='3': test_psf_from_file(fn_geo_epix10ka2m_16)
  elif tname=='4': test_psf_from_file(fn_geo_jungfrau_8)
  elif tname=='5': test_psf_from_file(fn_geo_pnccd_amo)

  elif tname=='11': test_load_psf()
  elif tname=='12': test_load_data_fropm_file(fn_data_cspad)
  elif tname=='13': test_load_data_fropm_file(fn_data_epix10ka2m)
  elif tname=='14': test_load_data_fropm_file(fn_data_jungfrau)

  elif tname=='22': test_data_to_psf(fn_geo_cspad_xpp,     fn_data_cspad)
  elif tname=='23': test_data_to_psf(fn_geo_epix10ka2m_16, fn_data_epix10ka2m)
  elif tname=='24': test_data_to_psf(fn_geo_jungfrau_8,    fn_data_jungfrau)

  else: logger.warning('NON-IMPLEMENTED TEST: %s' % tname)

# EOF
