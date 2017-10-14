#!/usr/bin/env python
#------------------------------

import os
import sys
from time import time
import subprocess # for subprocess.Popen
#import PSCalib.GlobalUtils as gu
from PSCalib.RunProcUtils import log_file, append_log_file, exp_run_new, exp_run_new_under_control, dict_exp_run_old, print_exp_runs_old

"""
:py:class:`SubprocUtils` contains utils to use subproccesses in specific apps.

Usage::

    # Import
    import PSCalib.SubprocUtils as su

    # Parameters

    # Methods
    dsn   = su.dsname(exp='xpptut15', run='0001')

Methods 
  * :meth:`dsname`
  * ...

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

Created on 2017-10-11 by Mikhail Dubrovin
"""
#------------------------------

def call(cmd, shell=False) :
    subprocess.call(cmd.split(), shell=shell) # , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

#------------------------------

def subproc(cmd, env=None, shell=False) :
    """e.g., command='bsub -q psananehq -o log-ls.txt ls -l]
       command_seq=['bsub', '-q', cp.batch_queue, '-o', 'log-ls.txt', 'ls -l']
    """
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, shell=shell) #, stdin=subprocess.STDIN
    p.wait()
    out = p.stdout.read() # reads entire file
    err = p.stderr.read() # reads entire file
    return out, err

#------------------------------
#------------------------------
#------------------------------
#------------------------------
#------------------------------

def proc_exp_runs(exp_runs, procname='pixel_status', add_to_log=False) :
    for i,(exp,run) in enumerate(exp_runs) :
        dsname = 'exp=%s:run=%s'%(exp, run.lstrip('0'))
        logname = log_file(exp, procname)
        print '%4d %s %4s %s %s'%(i+1, exp.ljust(10), run, dsname.ljust(22), logname)
        #--------------
        if add_to_log : append_log_file(exp, procname, [run,])
        #--------------
    print '%d new runs found' % (len(exp_runs))

#------------------------------

def proc_datasets_new(ins='CXI', procname='pixel_status', add_to_log=False) :
    exp_runs = exp_run_new(ins, procname)
    #print 'XXX:\n', exp_runs
    proc_exp_runs(exp_runs, procname, add_to_log)

#------------------------------

def proc_datasets_new_under_control(procname='pixel_status', add_to_log=False) :
    exp_runs = exp_run_new_under_control(procname)
    proc_exp_runs(exp_runs, procname, add_to_log)

#------------------------------

def proc_datasets_old(ins='CXI', procname='pixel_status', move_to_archive=False) :
    dic_exp_runs = dict_exp_run_old(ins, procname)
    print_exp_runs_old(dic_exp_runs, procname, move_to_archive)

#------------------------------
#------------------------------
#------------------------------

def test_cmd(cmd = 'ls -ltra') :
    out, err = subproc(cmd)
    print 'Command: "%s"' % cmd
    print 'out:\n"%s"' % out
    print 'err:\n"%s"' % err
 
#------------------------------

def test01() :
    cmd = 'bsub -q psanaq -o log-ls.txt ls -l'
    test_cmd(cmd)

#------------------------------
#------------------------------

def usage() :
    return  'python PSCalib/src/RunProcUtils.py <test_name>\n'\
           +'       <test_name> = 1  - print new files in experiments listed in control file\n'\
           +'                   = 10 - the same as 1 and save record for each new run in log file\n'\
           +'                   = 2  - print new files in all experiments\n'\
           +'                   = 20 - the same as 2 and save record for each new run in log file\n'\
           +'                   = 4  - print old (available in log but missing in xtc-dir) files for all experiments\n'\
           +'                   = 40 - the same as 4 and move old run records from log to archive file\n'

#------------------------------

if __name__ == "__main__" :
    print 80*'_'
    tname = sys.argv[1] if len(sys.argv)>1 else '1'
    t0_sec = time()

    if   tname=='1' : proc_datasets_new_under_control(procname='pixel_status')
    elif tname=='10': proc_datasets_new_under_control(procname='pixel_status', add_to_log=True)

    elif tname=='2' : proc_datasets_new(ins=None, procname='pixel_status')
    elif tname=='20': proc_datasets_new(ins=None, procname='pixel_status', add_to_log=True)

    elif tname=='4' : proc_datasets_old(ins=None, procname='pixel_status')
    elif tname=='40': proc_datasets_old(ins=None, procname='pixel_status', move_to_archive=True)

    else : sys.exit ('Not recognized test name: "%s"' % tname)
    print 'Test %s time (sec) = %.3f' % (tname, time()-t0_sec)

    if len(sys.argv)<2 : print usage()

    sys.exit ('End of %s' % sys.argv[0])

#------------------------------
  
