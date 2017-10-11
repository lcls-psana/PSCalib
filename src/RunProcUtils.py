#!/usr/bin/env python
#------------------------------

import os
import sys
from time import time
from expmon.EMUtils import list_of_runs_in_xtc_dir #, list_of_files_in_dir_for_ext 
import PSCalib.GlobalUtils as gu

"""
Module :py:class:`NewRunFinderUtils` contains a set of utilities helping find new runs in xtc directory for data processing.

Content of files in the xtc directory is conmpared with log file in static DIR_LOG place 
for specified process name. New runs available in the xtc directory and not listed in the log file 
can be retrieved. After new run(s) processing log record(s) should be appended.

Usage::

    # Import
    import PSCalib.NewRunFinderUtils as fu

    # Parameters
    exp = 'xpptut15'
    run = '0059'
    procname = 'pixel_status'

    # Methods
    dsn   = fu.dsname(exp, run)
    fname = fu.control_file(procname)
    fname = fu.log_file(exp, procname)
    dname = fu.xtc_dir(exp)
    runs  = fu.runs_in_xtc_dir(exp)
    recs  = fu.recs_in_log_file(exp, procname)
    runs  = fu.runs_in_log_file(exp, procname)

    # Most useful methods
    runs  = fu.runs_new_in_xtc(exp, procname, verb=1)
    fu.append_log_file(exp, procname, runs=[run,])

Methods 
  * :meth:`dsname`
  * :meth:`log_file`
  * :meth:`xtc_dir`
  * :meth:`runs_in_xtc_dir`
  * :meth:`recs_in_log_file`
  * :meth:`runs_in_log_file`
  * :meth:`runs_new_in_xtc`
  * :meth:`append_log_file`

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

Created on 2017-10-05 by Mikhail Dubrovin
"""
#------------------------------

INSTRUMENTS = ('SXR', 'AMO', 'XPP', 'XCS', 'CXI', 'MEC', 'MFX', 'DET', 'MOB', 'USR', 'DIA')
DIR_INS = '/reg/d/psdm'
DIR_LOG = '/reg/g/psdm/logs/run_proc'

#------------------------------

def dsname(exp='xpptut15', run='0001') :
    return 'exp=%s:run=%s' % (exp, run.lstrip('0'))

#------------------------------

def control_file(procname='pixel_status') :
    """Returns (str) control file name, e.g. '/reg/g/psdm/logs/run_proc/pixel_status/proc_control.txt'
    """
    return '%s/%s/experiments.txt' % (DIR_LOG, procname)

#------------------------------

def log_file(exp='xpptut15', procname='pixel_status') :
    """Returns (str) log file name, e.g. '/reg/g/psdm/logs/run_proc/pixel_status/CXI/xpptut15-proc-runs.txt'
    """
    return '%s/%s/%s/%s-proc-runs.txt' % (DIR_LOG, procname, exp[:3].upper(), exp)

#------------------------------

def xtc_dir(exp='xpptut15') :
    """Returns (str) xtc directory name, e.g. '/reg/d/psdm/XPP/xpptut15/xtc'
    """
    return '%s/%s/%s/xtc' % (DIR_INS, exp[:3].upper(), exp)

#------------------------------

def instrument_dir(ins='CXI') :
    _ins = ins.upper()
    if not(_ins in INSTRUMENTS): raise IOError('Unknown instrument "%s"' % ins)
    return '%s/%s' % (DIR_INS, _ins)

#------------------------------

def runs_in_xtc_dir(exp='xpptut15') :
    """Returns sorted list of (str) runs in xtc directory name, e.g. ['0059', '0060',...]
    """
    dirxtc = xtc_dir(exp)
    if not os.path.lexists(dirxtc) : raise IOError('Directory %s is not available' % dirxtc)
    print 'Scan directory: %s' % dirxtc
    return sorted(list_of_runs_in_xtc_dir(dirxtc))

#------------------------------

def recs_in_log_file(exp='xpptut15', procname='pixel_status') :
    """Returns list of (str) records in the log file for specified experiment and process name.
       E.g. of one record: '0151 2017-10-05T15:19:21'
    """
    fname_log = log_file(exp, procname)
    print 'Log file: %s' % fname_log
    if not os.path.lexists(fname_log) : 
        print 'Log file "%s" does not exist' % fname_log
        return []
    recs = gu.load_textfile(fname_log).split('\n')
    return recs # list of records, each record is '0059 <time-stamp>'

#------------------------------

def runs_in_log_file(exp='xpptut15', procname='pixel_status') :
    """Returns list of (4-char str) runs in the log file for specified experiment and process name.
       E.g. ['0059', '0060',...]
    """
    runs = [rec.split(' ')[0] for rec in recs_in_log_file(exp, procname) if rec]
    return runs

#------------------------------

def append_log_file(exp='xpptut15', procname='pixel_status', runs=[]) :
    """Appends records in the log file for list of (str) runs for specified experiment and process name.
    """
    fname_log = log_file(exp, procname)
    print 'Append log file: %s' % fname_log
    gu.create_path(fname_log, depth=6, mode=0774, verb=True)

    tstamp = gu.str_tstamp('%Y-%m-%dT%H:%M:%S', time())
    login  = gu.get_login()
    cwd    = gu.get_cwd()
    host   = gu.get_hostname()
    cmd    = sys.argv[0]
    recs = ['%s %s %s %s cwd:%s cmd:%s'%(s, tstamp, login, host, cwd, cmd) for s in runs]
    text = '\n'.join(recs)

    #print 'Save in file text "%s"' % text
    gu.save_textfile(text, fname_log, mode='a')
    os.chmod(fname_log, 0664)

#------------------------------

def runs_new_in_xtc(exp='xpptut15', procname='pixel_status', verb=0) :
    """Returns list of (4-char str) runs which are found and xtc directory and not yet listed in the log file,
       e.g. ['0059', '0060',...]
    """
    runs_log = runs_in_log_file(exp, procname)
    runs_xtc = runs_in_xtc_dir(exp)
    runs_new = [s for s in runs_xtc if not(s in runs_log)]

    if verb & 2:
        for srun in runs_xtc :
            if srun in runs_new : print '%s - new' % srun
            else :                print '%s - processed %s' % (srun, dsname(exp, srun))

    if verb :
        print '\nScan summary for exp=%s process="%s"' % (exp, procname)
        print '%4d runs in xtc dir  : %s' % (len(runs_xtc), xtc_dir(exp)),\
              '\n%4d runs in log file : %s' % (len(runs_log), log_file(exp, procname)),\
              '\n%4d runs NEW' % len(runs_new)

    return runs_new

#------------------------------

def experiments(ins='CXI') :
    """Returns list of (8,9-char-str) experiment names for specified 3-char (str) instrument name
       e.g. ['mfxo1916', 'mfxn8416', 'mfxlq3915',...]
    """
    dirname = instrument_dir(ins)
    _ins = ins.lower()
    return [fname for fname in os.listdir(dirname) if fname[:3] == _ins]

#------------------------------

def experiments_under_control(procname='pixel_status') :
    """Returns list of (str) experiment names under control.
    """
    fname = control_file(procname)
    if not os.path.lexists(fname) : 
        #raise IOError('Control file "%s" does not exist' % fname)
        print 'WARNING: control file "%s" does not exist' % fname
        return []
    recs = gu.load_textfile(fname).split('\n')
    return [rec for rec in recs if (rec and (rec[0]!='#'))] # skip empty and commented records

#------------------------------
#------------------------------
#--------  EXAMPLES  ----------
#------------------------------
#------------------------------

def proc_new_runs(exp='xpptut15', procname='pixel_status', verb=1) :
    runs_new = runs_new_in_xtc(exp, procname, verb)
    if len(runs_new) :
        print 'New runs found in %s for process %s:' % (exp, procname)
        for srun in runs_new :
            print srun,
        print ''
        append_log_file(exp, procname, runs_new)
    else :
        print 'No new runs found in %s for process %s' % (exp, procname)

        #ctime_sec = os.path.getctime(fname)
        #ctime_str = gu.str_tstamp('%Y-%m-%dT%H:%M:%S', ctime_sec)
        #print ctime_str, fname

#------------------------------

def proc_experiments_under_control(procname='pixel_status') :
    for exp in experiments_under_control(procname) :
        print '%s\nProcess new runs for %s' % (50*'=', exp)
        proc_new_runs(exp, procname)

#------------------------------

def print_experiments(ins='CXI') :
    exps = experiments(ins)
    for exp in exps :
        print exp
    print '%d experiments found in %s' % (len(exps), instrument_dir(ins))

#------------------------------

def print_experiments_under_control(procname='pixel_status') :
    for exp in experiments_under_control(procname) :
        print exp

#------------------------------

def print_all_experiments() :
    tot_nexps=0
    ins_nexps={}
    for ins in INSTRUMENTS : 
        exps = experiments(ins)
        for exp in exps :
            print exp
            tot_nexps += 1
        print '%d experiments found in %s\n' % (len(exps), instrument_dir(ins))
        ins_nexps[ins] = len(exps)

    print 'Number of expriments per instrument'
    #print '%d experiments found in %s' % (len(exps), ''.join(INSTRUMENTS))
    for ins in INSTRUMENTS : print '%s : %4d' % (ins, ins_nexps[ins])
    print 'Total number of expriments %d' % tot_nexps

#------------------------------

if __name__ == "__main__" :
    print 80*'_'
    tname = sys.argv[1] if len(sys.argv)>1 else '0' # 'CXI'
    cname = tname.upper()

    if cname in INSTRUMENTS : print_experiments(ins=cname)
    elif tname=='0': print_all_experiments()
    elif tname=='1': proc_new_runs(exp='xpptut15', procname='pixel_status', verb=1)
    elif tname=='2': proc_new_runs(exp='xpptut15', procname='pixel_status', verb=2)
    elif tname=='3': print_experiments_under_control(procname='pixel_status')

    elif tname=='101': proc_experiments_under_control(procname='pixel_status')

    else : sys.exit ('Not recognized test name: "%s"' % tname)
    sys.exit ('End of %s' % sys.argv[0])

#------------------------------
