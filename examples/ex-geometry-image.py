#!@PYTHON@
####!/usr/bin/env python

import sys
from time import time
import numpy as np

from pyimgalgos.GlobalUtils import print_ndarr
from PSCalib.GeometryAccess import GeometryAccess, img_from_pixel_arrays

import pyimgalgos.Graphics as gr
import pyimgalgos.GlobalGraphics as gg

#------------------------------

def plot_image(img):
    import pyimgalgos.GlobalGraphics as gg
    ave, rms = img.mean(), img.std()
    gg.plotImageLarge(img, amp_range=(ave-1*rms, ave+2*rms))
    gg.show()

#------------------------------
#    fig, axim, axcb = gg.fig_axes(figsize=(13,12), title='Image', dpi=80, \
#                       win_axim=(0.05,  0.03, 0.87, 0.93), \
#                       win_axcb=(0.923, 0.03, 0.02, 0.93))
#------------------------------
#    imsh, cbar = gr.imshow_cbar(fig, axim, axcb, img, amin=None, amax=None, extent=None,\
#                 interpolation='nearest', aspect='auto', origin='upper',\
#                 orientation='horizontal', cmap='jet') 
#------------------------------
# drawCircle(axes, xy0, radius, linewidth=1, color='w', fill=False)
# drawCenter(axes, xy0, s=10, linewidth=1, color='w')
# drawLine(axes, xarr, yarr, s=10, linewidth=1, color='w')
# drawRectangle(axes, xy, width, height, linewidth=1, color='w')
# save_fig(fig, fname='img.png', do_save=True, pbits=0377)

#------------------------------
#------------------------------

def ex_geometry_image(ntest) : 

    cdir = '/reg/d/psdm/MFX/mfx11116/calib'

    fname_geo = None
    fname_img = None
    shape     = None
    segname, segind, dx, dy = None, 0, 0, 0

    if tname == '1' :
      #fname_geo = '%s/%s' % (cdir, 'CsPad::CalibV1/MfxEndstation.0:Cspad.0/geometry/566-end.data')
      fname_geo = 'geo-cspad-mfx.txt'
      #fname_img = 'nda-mfx11116-r0624-e005365-MfxEndstation-0-Cspad-0-max.txt'
      fname_img = 'nda-mfx11116-r0625-e026505-MfxEndstation-0-Cspad-0-max.txt'
      #fname_img = 'nda-mfx11116-r0626-e015975-MfxEndstation-0-Cspad-0-max.txt'
      shape = (32,185,388)
      #segname, segind, dx, dy = 'CSPAD:V2', 0, -77500, 120000

    elif tname == '2' :
      #fname_geo = '%s/%s' % (cdir, 'Jungfrau::CalibV1/MfxEndstation.0:Jungfrau.0/geometry/0-end.data')
      fname_geo = 'geo-jf-mfx.txt'
      fname_img = 'nda-mfx11116-r0624-e005365-MfxEndstation-0-Jungfrau-0-max.txt'
      #fname_img = 'nda-mfx11116-r0625-e026505-MfxEndstation-0-Jungfrau-0-max.txt'
      #fname_img = 'nda-mfx11116-r0626-e015975-MfxEndstation-0-Jungfrau-0-max.txt'
      shape = (2,512,1024)
      #segname, segind, dx, dy = 'JFCAMERA:V1', 0, -90*1000, -3*1000

    print 'fname_geo: %s' % (fname_geo)
    print 'fname_img: %s' % (fname_img)

    t0_sec = time()
    geo = GeometryAccess(fname_geo, 0377)

    if segname is not None : 
        geo.move_geo(segname, segind, dx, dy, 0) # (hor, vert, z)

    X, Y, Z = geo.get_pixel_coords() # oname=None, oindex=0, do_tilt=True)
    print 'GeometryAccess time = %.6f sec' % (time()-t0_sec)
    xmin = X.min()
    xmax = X.max()
    ymin = Y.min()
    ymax = Y.max()
    print 'Image xmin=%.1f xmax=%.1f ymin=%.1f ymax=%.1f'% (xmin, xmax, ymin, ymax)

    print_ndarr(X, 'X')
    print_ndarr(Y, 'Y')

    nda = np.loadtxt(fname_img)
    iX, iY = geo.get_pixel_coord_indexes(do_tilt=True)
    print_ndarr(iX, 'iX')
    print_ndarr(iY, 'iY')
    print_ndarr(nda, 'nda')

    iX.shape = shape
    iY.shape = shape
    nda.shape = shape

    img = img_from_pixel_arrays(iX,iY,W=nda)
    print_ndarr(img, 'img')

    #plot_image(img)
    ave, rms = img.mean(), img.std()
    min, max = img.min(), img.max()
    amin, amax = ave-0.5*rms, ave+2.5*rms
    #amin, amax = 600, 1300
    print 'Image ave=%.1f rms=%.1f min=%.1f max=%.1f amin=%.1f amax=%.1f'%\
          (ave, rms, min, max, amin, amax)

    fig, axim, axcb = gg.fig_axes(figsize=(13,12), title=fname_geo)
    imsh, cbar = gr.imshow_cbar(fig, axim, axcb, img, amin=amin, amax=amax, extent=(xmin,xmax,ymin,ymax),\
                                interpolation='nearest', aspect='auto', origin='upper',\
                                orientation='vertical', cmap='inferno') # 'inferno''Greys_r'

    xy0 = (0,0)

    gg.drawCenter(axim, xy0, s=xmax/20, linewidth=1, color='w')

    for radius in np.linspace(0, 2.5*xmax, 50, endpoint=True) :
        gg.drawCircle(axim, xy0, radius, linewidth=1, color='w', fill=False)

    gr.show(mode=None)
    ofname = 'img-%s.png' % fname_geo.split('.')[0]
    gg.save_fig(fig, fname=ofname, do_save=True, pbits=0377)

#------------------------------

if __name__ == "__main__" :
    tname = sys.argv[1] if len(sys.argv) > 1 else '1'
    print 50*'_', '\nTest %s:' % tname
    if   tname == '1' : ex_geometry_image(tname);
    elif tname == '2' : ex_geometry_image(tname)
    else : print 'Not-recognized test name: %s' % tname
    sys.exit('End of test %s' % tname)
 
#------------------------------
