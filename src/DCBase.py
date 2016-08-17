#!/usr/bin/env python
#-----------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#-----------------------------------------------------------------------------

""":py:class:`PSCalib.DCStore` base class for the Detector Calibration (DC) project.

Usage::

    # Import
    from PSCalib.DCBase import DCBase

    o = DCBase()


@see classes 
\n   :py:class:`PSCalib.DCStore`,
\n   :py:class:`PSCalib.DCType`,
\n   :py:class:`PSCalib.DCRange`,
\n   :py:class:`PSCalib.DCVersion`,
\n   :py:class:`PSCalib.DCBase`

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

@version $Id$

@author Mikhail S. Dubrovin
"""

#---------------------------------
__version__ = "$Revision$"
#---------------------------------

from time import time, sleep, localtime, gmtime, strftime, strptime, mktime
from math import floor
from PSCalib.DCLogger import log

#------------------------------

#class DCBase() :
class DCBase(object) :
    """Base class for the Detector Calibration (DC) project

    o = DCBase()

    pars = o.pars()                  # (dict) dictionary of pars associated with each object
    par  = o.par(k)                  # returns par value for key k
    log  = o.history(fmt)            # returns (str) history records preceded by the time stamp as a text
    d    = o.histdict()              # returns (dict) history dictionary associated with current object 

    o.set_pars(d)                    # set (dict) dictionary of pars for object
    o.add_par(k,v)                   # add (k,v) par to the dictionary of pars for object
    o.del_pars()                     # delete all pars from the dictionary
    o.del_par(k)                     # delete par with key k 
    o.str_pars()                     # returns a string of pars
    o.set_history(d)                 # set (dict) dictionary of history from specified dictionary
    o.add_history(rec, ts)           # add (str) record with (int) time stamp to the history dictionary (ts:rec).
                                     # If ts is None - current time is used as a key.
    """

    #tsfmt = '%Y-%m-%dT%H:%M:%S%Z'
    tsfmt = '%Y-%m-%dT%H:%M:%S'

    def __init__(self) :
        self._name = 'DCBase'
        self.dicpars = {}
        self.dichist = {}
        msg = 'In c-tor %s' % self._name
        log.debug(msg, self._name)

    def __del__(self) :
        self.dicpars.clear()

    def pars(self) :
        return self.dicpars if len(self.dicpars)>0 else None

    def par(self, k ) :
        return self.dicpars.get(k, None)

    def add_par(self, k, v) :
        self.dicpars[k] = v

    def set_pars(self, d) :
        self.dicpars.clear()
        for k,v in d.items() :
            self.dicpars[k] = v
    
    def del_pars(self) :
        self.dicpars.clear()

    def del_par(self, k) :
        if k in self.dicpars : del self.dicpars[k]
        
    def str_pars(self) :
        return ', '.join(['(%s : %s)' % (str(k), str(v)) for k,v in self.dicpars.items()])

    def set_history(self, d) :
        self.dichist.clear()
        for k,v in d.items() :
            self.dichist[k] = v

    def add_history(self, rec, ts=None) :
        t_sec = time() if ts is None else ts
        self.dichist[t_sec] = rec
        #sleep(0.0001)
        #print 'add recod in time = %.6f' % t_sec

    def histdict(self) :
        return self.dichist

    def history(self, fmt=None) :
        tsfmt = self.tsfmt if fmt is None else fmt
        return '\n'.join(['%s %s' % (self.tsec_to_tstr(ts), str(rec)) for ts,rec in sorted(self.dichist.items())])

    def save_history_file(self, path='history.txt', verb=False) :
        f = open(path,'w')
        f.write(self.history())
        f.close()
        if verb : print 'History records are saved in the file: %s' % path
    
    def load_history_file(self, path='history.txt', verb=False) :
        f = open(path,'r')
        lines = f.readlines()
        f.close()
        for line in lines :
            tsstr, rec = line.rstrip('\n').split(' ',1)
            #print 'XXX:', tsstr, rec            
            self.dichist[self.tstr_to_tsec(tsstr)] = rec
        if verb : print 'Read history records from the file: %s' % path

    def tsec_to_tstr(self, tsec, fmt=None) :
        """converts float tsec like 1471035078.908067 to the string 2016-08-12T13:51:18.908067"""
        tsfmt = self.tsfmt if fmt is None else fmt
        itsec = floor(tsec)
        strfsec = ('%.6f' % (tsec-itsec)).lstrip('0')
        return '%s%s' % (strftime(tsfmt, localtime(itsec)), strfsec)


    def tstr_to_tsec(self, tstr, fmt=None) :
        """converts string tstr like 2016-08-12T13:51:18.908067 to the float time in seconds 1471035078.908067"""
        tsfmt = self.tsfmt if fmt is None else fmt
        ts, fsec =  tstr.split('.')
        return mktime(strptime(ts, tsfmt)) + 1e-6*int(fsec)

    def save_base(self, grp) :
        print 'In %s.save_base(): group name=%s TBD: save parameters and hystory' % (self._name, grp.name)
    
    def load_base(self, grp) :
        print 'In %s.load_base(): group name=%s TBD: load parameters and hystory' % (self._name, grp.name)
    
#------------------------------

def test_pars() :
    o = DCBase()
    d = {1:'10', 2:'20', 3:'30'}
    o.set_pars(d)
    print '\nTest pars: %s' % o.str_pars()

#------------------------------

def test_history() :
    o = DCBase()
    o.add_history('rec 01')
    o.add_history('rec 02')
    o.add_history('rec 03')
    o.add_history('rec 04')
    o.add_history('rec 05')
    o.add_history('rec 06')
    print '\nTest history records:\n%s' % o.history()
    o.save_history_file('history-test.txt', verb=True)
    o.add_history('rec 07')

    o.load_history_file('history-test.txt', verb=True)
    print '\nTest history records:\n%s' % o.history()

#------------------------------

def test_tstamp() :
    o = DCBase()
    tsec = time()
    tstr = o.tsec_to_tstr(tsec)
    #tstr = '2016-08-12T12:02:44PDT'
    print 'Current time in sec: %f is converted to the time stamp string: %s' % (tsec, tstr)
    print 'Time stamp string: %s is converted to time in sec: %f' % (tstr, o.tstr_to_tsec(tstr))

#------------------------------

if __name__ == "__main__" :
    import sys
    test_tstamp()
    test_pars()
    test_history()
    sys.exit( 'End of %s test.' % sys.argv[0])

#------------------------------
