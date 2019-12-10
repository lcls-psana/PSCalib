from __future__ import print_function

#from CalibManager.RegDBUtils import experiment_runs, run_attributes
from RegDB import experiment_info as expinfo

# expinfo.experiment_runs(ins, exp)
# expinfo.run_attributes(ins, exp, run)
# expinfo.unique_detector_names()
# expinfo.detectors(ins, exp, run)
# expinfo.calibration_runs(ins, exp)

def print_experiment_runs(ins, exp) :
    for r in expinfo.experiment_runs(ins, exp) :
        print(30*'_', '\n', r)
        for k,v in r.iteritems() :
            print('    ', k,v)


def print_run_attributes(ins, exp, run) :
    for r in expinfo.run_attributes(ins, exp, run) :
        print(r)


def print_unique_detector_names() :
    for r in expinfo.unique_detector_names() :
        print(r)


def print_detectors(ins, exp, run) :
    for r in expinfo.detectors(ins, exp, run) :
        print(r)


def print_calibration_runs(ins, exp) :
    for k,v in expinfo.calibration_runs(ins, exp).iteritems() :
        print(k,v)

#------------------------------

if __name__ == "__main__" :
    import sys; global sys
    tname = sys.argv[1] if len(sys.argv) > 1 else '0'
    print(50*'_', '\nTest %s:' % tname)
    if   tname=='0' : print_experiment_runs('CXI', 'cxif5315')
    elif tname=='1' : print_experiment_runs('CXI', 'cxif5315')
    elif tname=='2' : print_run_attributes('CXI', 'cxif5315', 205)
    elif tname=='3' : print_unique_detector_names()
    elif tname=='4' : print_detectors('CXI', 'cxif5315', 205)
    elif tname=='5' : print_calibration_runs('CXI', 'cxif5315')
    else : print('Not-recognized test name: "%s"' % tname)

    sys.exit ('End of %s' % sys.argv[0])

#------------------------------
