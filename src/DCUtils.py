#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#------------------------------------------------------------------------

"""
:py:class:`PSCalib.DCUtils` - contains a set of utilities

Usage::

    # Import
    import PSCalib.DCUtils as gu

    # Methods
    # Get string with time stamp, ex: 2016-01-26T10:40:53
    ts    = gu.str_tstamp(fmt='%Y-%m-%dT%H:%M:%S', time_sec=None)

    usr   = gu.get_enviroment(env='USER')
    usr   = gu.get_login()
    host  = gu.get_hostname()
    cwd   = gu.get_cwd()

@see

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

@version $Id: 2013-03-08$

@author Mikhail S. Dubrovin
"""

#--------------------------------
__version__ = "$Revision$"
#--------------------------------

#import sys
import os
import getpass
import socket
import numpy as np
from time import localtime, strftime

#------------------------------
#------------------------------

def str_tstamp(fmt='%Y-%m-%dT%H:%M:%S', time_sec=None) :
    """Returns string timestamp for specified format and time in sec or current time by default
    """
    return strftime(fmt, localtime(time_sec))

#------------------------------

def get_enviroment(env='USER') :
    """Returns the value of specified by string name environment variable
    """
    return os.environ[env]

#------------------------------

def get_login() :
    """Returns login name
    """
    #return os.getlogin()
    return getpass.getuser()

#------------------------------

def get_hostname() :
    """Returns login name
    """
    #return os.uname()[1]
    return socket.gethostname()

#------------------------------

def get_cwd() :
    """Returns current working directory
    """
    return os.getcwd()

#------------------------------

def create_directory(dir, verb=False) : 
    if os.path.exists(dir) :
        if verb : print 'Directory exists: %s' % dir
    else :
        os.makedirs(dir)
        if verb : print 'Directory created: %s' % dir

#------------------------------

def save_string_as_dset(grp, name, s) :
    """ Creates and returns the h5py dataset object with name for single string s
    """
    if s is None : return None
    #size = len(s)
    #create_dataset(name, shape=None, dtype=None, data=None, **kwds) 
    dset = grp.create_dataset(name, shape=(1,), dtype='S%d'%len(s)) #, data=s)
    dset[0] = s
    return dset

#------------------------------
#------------------------------
#------------------------------
#------------------------------

def do_test() :

    import sys

    print 'get_enviroment(USER) : %s' % get_enviroment()
    print 'get_login()          : %s' % get_login()
    print 'get_hostname()       : %s' % get_hostname()
    print 'get_cwd()            : %s' % get_cwd()
    #print ': %s' % 

#    if len(sys.argv) > 1 :
#      if sys.argv[1] == '1' : test_mask_neighbors_2d(allnbrs = False)
#      if sys.argv[1] == '2' : test_mask_neighbors_2d(allnbrs = True)
 
#------------------------------

if __name__ == "__main__" :
    do_test()

#------------------------------
