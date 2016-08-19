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
from PSCalib.DCUtils import save_string_as_dset, save_object_as_dset

#------------------------------

#class DCBase() :
class DCBase(object) :
    """Base class for the Detector Calibration (DC) project

    o = DCBase()

    # Dictionary of parameters
    # ========================

    o.set_pars_dict(d)                   # set (dict) dictionary of pars.
    o.add_par(k,v)                       # add (k,v) par to the dictionary of pars.
    o.del_par(k)                         # delete par with key k. 
    o.clear_pars()                       # delete all pars from the dictionary.
    d = o.pars_dict()                    # returns (dict) dictionary of pars.
    p = o.par(k)                         # returns par value for key k.
    t = o.pars_text()                    # returns (str) text of all pars.

    # History records
    # ===============

    o.set_history_dict(d)                # set (dict) dictionary of history from specified dictionary
    o.add_history_record(rec, tsec=None) # add (str) record with (int) time[sec] to the history dictionary of (tsec:rec).
                                         # If tsec is None - current time is used as a key.
    o.del_history_record(tsec)           # Delete one history record from the dictionary by its time tsec.
    o.clear_history()                    # Delete all history records from the dictionary.
    d = o.history_dict()                 # returns (dict) history dictionary associated with current object .
    r = o.history_record(tsec)           # returns (str) history record for specified time tsec.
    t = o.history_text(tsfmt=None)       # returns (str) all history records preceded by the time stamp as a text.

    # Save and Load
    # =============

    o.save_history_file(path='history.txt', verb=False) # save history in the text file
    o.load_history_file(path='history.txt', verb=False) # load history from the text file

    o.save_base(grp)                     # save everything in hdf5 group
    o.load_base(grp)                     # load from hdf5 group

    # Time convertors
    # ===============

    t_str = o.tsec_to_tstr(tsec, tsfmt=None) # converts (float) time[sec] to the (str) time stamp
    t_sec = o.tstr_to_tsec(tstr, tsfmt=None) # converts (str) time stamp to (float) time[sec]

    """
    _tsfmt = '%Y-%m-%dT%H:%M:%S'

    def __init__(self) :
        self._name = 'DCBase'
        self._dicpars = {}
        self._dichist = {}
        msg = 'In c-tor %s' % self._name
        log.debug(msg, self._name)
        self._grp_pars_name = '_parameters'
        self._grp_history_name = '_history'

    def __del__(self) :
        self._dicpars.clear()

    def set_pars_dict(self, d) :
        self._dicpars.clear()
        for k,v in d.items() :
            self._dicpars[k] = v
    
    def add_par(self, k, v) :
        self._dicpars[k] = v

    def del_par(self, k) :
        if k in self._dicpars.keys() : del self._dicpars[k]
        
    def clear_pars(self) :
        self._dicpars.clear()

    def pars_dict(self) :
        return self._dicpars if len(self._dicpars)>0 else None

    def par(self, k ) :
        return self._dicpars.get(k, None)

    def pars_text(self) :
        return ', '.join(['(%s : %s)' % (str(k), str(v)) for k,v in self._dicpars.items()])

    def set_history_dict(self, d) :
        self._dichist.clear()
        for k,v in d.items() :
            self._dichist[k] = v

    def add_history_record(self, rec, tsec=None) :
        t_sec = time() if tsec is None else tsec
        self._dichist[t_sec] = rec
        sleep(1) # wait 1ms in order to get unique timestamp
        #print 'add recod in time = %.6f' % t_sec
        #log.debug('Add recod: %s with time:  %.6f' % (rec, t_sec), self._name)

    def del_history_record(self, k) :
        if k in self._dichist.keys() : del self._dichist[k]
        
    def clear_history(self) :
        self._dicpars.clear()

    def history_dict(self) :
        return self._dichist

    def history_record(self, tsec) :
        return self._dichist.get(tsec)

    def history_text(self, tsfmt=None) :
        """Returns (str) history records preceded by the time stamp as a text"""
        fmt = self._tsfmt if tsfmt is None else tsfmt
        return '\n'.join(['%s %s' % (self.tsec_to_tstr(ts), str(rec)) for ts,rec in sorted(self._dichist.items())])

    def save_history_file(self, path='history.txt', verb=False) :
        """Save history in the text file"""
        f = open(path,'w')
        f.write(self.history_text())
        f.close()
        if verb : 
            #print 'History records are saved in the file: %s' % path
            log.debug('History records are saved in the file: %s' % path, self._name)
    
    def load_history_file(self, path='history.txt', verb=False) :
        """Load history from the text file"""
        f = open(path,'r')
        lines = f.readlines()
        f.close()
        for line in lines :
            tsstr, rec = line.rstrip('\n').split(' ',1)
            #print 'XXX:', tsstr, rec            
            self._dichist[self.tstr_to_tsec(tsstr)] = rec
        if verb : 
            #print 'Read history records from the file: %s' % path
            log.debug('Read history records from the file: %s' % path, self._name)

    def _save_pars_dict(self, grp) :
        """Saves _dicpars in the h5py group"""
        grpdic = grp.create_group(self._grp_pars_name)
        for k,v in self._dicpars.items() :
            ds = save_object_as_dset(grpdic, name=k, data=v)

    def _save_hystory_dict(self, grp) :
        """Saves _dichist in the h5py group"""
        grpdic = grp.create_group(self._grp_history_name)
        for k,v in self._dichist.items() :
            tstamp = str(self.tsec_to_tstr(k))
            #print 'XXX:', tstamp, v
            ds = save_object_as_dset(grpdic, tstamp, data=v)
        #print 'In %s.save_hystory_dict(): group name=%s TBD: save parameters and hystory' % (self._name, grp.name)

    def save_base(self, grp) :
        self._save_pars_dict(grp)
        self._save_hystory_dict(grp)
    
    def load_base(self, grp) :
        print 'In %s.load_base(): group name=%s TBD: load parameters and hystory' % (self._name, grp.name)
    
    def tsec_to_tstr(self, tsec, tsfmt=None) :
        """converts float tsec like 1471035078.908067 to the string 2016-08-12T13:51:18.908067"""
        fmt = self._tsfmt if tsfmt is None else tsfmt
        itsec = floor(tsec)
        strfsec = ('%.6f' % (tsec-itsec)).lstrip('0')
        return '%s%s' % (strftime(fmt, localtime(itsec)), strfsec)

    def tstr_to_tsec(self, tstr, tsfmt=None) :
        """converts string tstr like 2016-08-12T13:51:18.908067 to the float time in seconds 1471035078.908067"""
        fmt = self._tsfmt if tsfmt is None else tsfmt
        ts, fsec = tstr.split('.')
        return mktime(strptime(ts, fmt)) + 1e-6*int(fsec)

#------------------------------

def test_pars() :
    o = DCBase()
    d = {1:'10', 2:'20', 3:'30'}
    o.set_pars_dict(d)
    print '\nTest pars: %s' % o.pars_text()
    o.del_par(2)
    print '\nAfter del_par(2): %s' % o.pars_text()
    print '\npar(3): %s' % o.par(3)

#------------------------------

def test_history() :
    o = DCBase()
    o.add_history_record('rec 01')
    o.add_history_record('rec 02')
    o.add_history_record('rec 03')
    o.add_history_record('rec 04')
    o.add_history_record('rec 05')
    o.add_history_record('rec 06')
    print '\nTest history records:\n%s' % o.history_text()
    o.save_history_file('history-test.txt', verb=True)
    o.add_history_record('rec 07')

    o.load_history_file('history-test.txt', verb=True)
    print '\nTest history records:\n%s' % o.history_text()

#------------------------------

def test_time_converters() :
    o = DCBase()
    t_sec  = time()
    t_str  = o.tsec_to_tstr(t_sec, tsfmt=None) 
    t_sec2 = o.tstr_to_tsec(t_str, tsfmt=None)
    print 'convert time     %.6f to time stamp: %s' % (t_sec,  t_str)
    print 'and back to time %.6f' % (t_sec2)

#------------------------------

if __name__ == "__main__" :
    import sys
    test_pars()
    test_history()
    test_time_converters()
    sys.exit( 'End of %s test.' % sys.argv[0])

#------------------------------
