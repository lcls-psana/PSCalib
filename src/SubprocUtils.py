#!/usr/bin/env python
#------------------------------

import os
import sys
from time import time
import subprocess # for subprocess.Popen
from PSCalib.GlobalUtils import get_login

#import PSCalib.GlobalUtils as gu
"""
:py:class:`SubprocUtils` contains utils to use subproccesses in specific apps
=============================================================================

Usage::

    # Import
    import PSCalib.SubprocUtils as su

    # Parameters
    cmd='bsub -q psnehq -o log-%%J.txt ls -l'
    qname='psnehq'
    env=None
    shell=False
    jobid='52966'

    # Methods
    su.call(cmd, shell=False)
    out, err = su.subproc(cmd, env=None, shell=False, do_wait=True)
    out, err, jobid = su.batch_job_submit(cmd='bsub -q psnehq -o log-%%J.txt ls -l', env=None, shell=False)
    njobs = su.number_of_batch_jobs(usr=None, qname=None)
    out, err = su.batch_job_kill(jobid, qname='psnehq')

Methods 
  * :meth:`call`
  * :meth:`subproc`
  * :meth:`batch_job_submit`
  * :meth:`number_of_batch_jobs`
  * :meth:`batch_job_kill`
  * ...

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

Created on 2017-10-11 by Mikhail Dubrovin
"""
#------------------------------

def call(cmd, shell=False) :
    subprocess.call(cmd.split(), shell=shell) # , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

#------------------------------

def subproc(cmd, env=None, shell=False, do_wait=True) :
    """e.g., command='bsub -q psananehq -o log-ls.txt ls -l]
       command_seq=['bsub', '-q', cp.batch_queue, '-o', 'log-ls.txt', 'ls -l']
    """
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, shell=shell) #, stdin=subprocess.STDIN
    out, err = '', ''
    if do_wait : 
        p.wait()
        out = p.stdout.read() # reads entire file
        err = p.stderr.read() # reads entire file
    return out, err

#------------------------------

def _str_jobid(msg) :
    """Returns (str) job Id from input string.

       E.g. returns '849160' from msg='Job <849160> is submitted to queue <psnehq>.'
    """
    fields = msg.split()
    if len(fields)<2 : return None
    if fields[0] !='Job' : return None
    return fields[1].lstrip('<').rstrip('>')

#------------------------------

def batch_job_submit(cmd='bsub -q psnehq -o log-%%J.txt ls -l', env=None, shell=False) :
    out, err = subproc(cmd, env, shell)
    jobid = _str_jobid(out)
    return out, err, jobid

#------------------------------

def _str_status(msg) :
    lines  = msg.split('\n')
    #for line in lines : print 'batch_job_status: ' + line
    if len(lines)<2 : return None
    line   = lines[1].strip('\n')
    status = line.split()[2]
    #print 'status: ', status
    return status # it might None, 'RUN', 'PEND', 'EXIT', 'DONE', etc 

#------------------------------

def batch_job_status(jobid, qname='psnehq') :
    """ Returns batch job (str) status, e.g. None, 'RUN', 'PEND', 'EXIT', 'DONE', etc 

        E.g.: strip responce of the bjobs command like

        JOBID   USER    STAT  QUEUE      FROM_HOST   EXEC_HOST   JOB_NAME   SUBMIT_TIME
        847941  dubrovi DONE  psnehq     psanaphi106 psana1507   *17:run=25 Oct 30 13:21

        and returns 'DONE'
    """
    cmd = 'bjobs -q %s %s' % (qname, jobid)
    out, err = subproc(cmd, env=None, shell=False)
    status = _str_status(out)
    return out, err, status

#------------------------------

def _number_of_records(txt) :
    lines  = txt.rstrip('\n').split('\n')
    return len(lines)

#------------------------------

def number_of_batch_jobs(usr=None, qname=None) : # qname='psnehq'
    """ Returns number of batch jobs.
    """
    cmd = 'bjobs -u %s' % (get_login() if usr is None else usr)
    if qname is not None : cmd += ' -q %s' % qname
    out, err = subproc(cmd, env=None, shell=False)
    return _number_of_records(out) - 1

#------------------------------

def batch_job_kill(jobid, qname='psnehq') :
    cmd = 'kill -q %s %s' % (qname, jobid)
    out, err = subproc(cmd)
    return out, err

#------------------------------
#------------------------------
#------------------------------
#------------------------------

def test_subproc(cmd='ls -ltra', env=None, shell=False, do_wait=True) :
    out, err = subproc(cmd, env, shell, do_wait)
    print 'Command: "%s"' % cmd
    print 'out:\n"%s"' % out
    print 'err:\n"%s"' % err
 
#------------------------------

def test_batch_job_submit(cmd='bsub -q psnehq -o log-%J.txt ls -l', env=None, shell=False) :
    out, err, jobid = batch_job_submit(cmd, env, shell)
    print 'Command: "%s"' % cmd
    print 'out:\n"%s"' % out
    print 'err:\n"%s"' % err
    print 'jobid:"%s"' % jobid
    print 'check log file log-%s.txt' % jobid

#------------------------------

def test_number_of_batch_jobs(usr=None, qname='psnehq') :
    njobs = number_of_batch_jobs(usr, qname)
    print 'usr  : %s' % str(usr)
    print 'qname: %s' % qname
    print 'njobs: %d' % njobs

#------------------------------

def test_batch_job_kill(jobid, qname='psnehq') :
    out, err = batch_job_kill(jobid, qname)
    print 'qname: %s' % qname
    print 'jobid:"%s"' % jobid
    print 'out:\n"%s"' % out
    print 'err:\n"%s"' % err


#------------------------------
#------------------------------
#------------------------------

def usage() :
    return  'python PSCalib/src/SubprocUtils.py <test_name> [<jobid>]\n'\
           +'       <test_name> = 1  - test subproc\n'\
           +'                   = 2  - test batch_job_submit\n'\
           +'                   = 3  - test number_of_batch_jobs\n'\
           +'                   = 4  - test batch_job_kill, NEEDS IN PARAMETER <jobid>\n'

#------------------------------

if __name__ == "__main__" :
    print 80*'_'
    tname = sys.argv[1] if len(sys.argv)>1 else '1'
    t0_sec = time()

    if   tname=='1': test_subproc(cmd='ls -ltra')
    elif tname=='2': test_batch_job_submit(cmd='bsub -q psnehq -o log-%J.txt ls -l', env=None, shell=False)
    elif tname=='3': test_number_of_batch_jobs(usr=None, qname='psnehq')
    elif tname=='4': test_batch_job_kill(sys.argv[2], qname='psnehq')

    else : sys.exit ('Not recognized test name: "%s"' % tname)
    print 'Test %s time (sec) = %.3f' % (tname, time()-t0_sec)

    if len(sys.argv)<2 : print usage()

    sys.exit ('End of %s' % sys.argv[0])

#------------------------------
  
