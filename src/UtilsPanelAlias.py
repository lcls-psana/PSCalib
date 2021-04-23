
"""
Usage::
    from PSCalib.UtilsPanelAlias import alias_for_id, id_for_alias

    FNAME_PANEL_ID_ALIASES = '%s.aliases.txt'%CALIB_REPO

    alias    = alias_for_id(panel_id, fname=FNAME_PANEL_ID_ALIASES)
    panel_id = id_for_alias(alias, fname=FNAME_PANEL_ID_ALIASES)
"""

import logging
logger = logging.getLogger(__name__)

import os
from PSCalib.GlobalUtils import load_textfile, save_textfile, get_login, str_tstamp

FNAME_PANEL_ID_ALIASES = '.aliases.txt'

def alias_for_id(panel_id, fname=FNAME_PANEL_ID_ALIASES, exp=None, run=None):
    """Returns Epix100a/10ka panel short alias for long panel_id, 
       e.g., for panel_id = 3925999616-0996663297-3791650826-1232098304-0953206283-2655595777-0520093719
       returns 0001
    """
    alias_max = 0
    if os.path.exists(fname):
      #logger.debug('search alias for panel id: %s\n  in file %s' % (panel_id, fname))
      recs = load_textfile(fname).strip('\n').split('\n')
      for r in recs:
        if not r: continue # skip empty records
        fields = r.strip('\n').split(' ')
        if fields[1] == panel_id: 
            logger.debug('found alias %s for panel_id %s in %s' % (fields[0], panel_id, fname))
            return fields[0]
        ialias = int(fields[0])
        if ialias>alias_max: alias_max = ialias
        #print(fields)
    # if record for panel_id is not found yet, add it to the file and return its alias
    rec = '%04d %s %s' % (alias_max+1, panel_id, str_tstamp())
    if exp is not None: rec += ' %10s' %  exp
    if run is not None: rec += ' r%04d' %  run
    rec += ' %s\n' % get_login()
    logger.debug('file "%s" is appended with record:\n%s' % (fname, rec))
    save_textfile(rec, fname, mode='a')
    return '%04d' % (alias_max+1)


def id_for_alias(alias, fname=FNAME_PANEL_ID_ALIASES):
    """Returns Jungfrau/Epix100a/10ka panel panel_id for specified alias, 
       e.g., for alias = 0001
       returns 3925999616-0996663297-3791650826-1232098304-0953206283-2655595777-0520093719
    """
    logger.debug('search panel id for alias: %s\n  in file %s' % (alias, fname))
    recs = load_textfile(fname).strip('\n').split('\n')
    for r in recs:
        fields = r.strip('\n').split(' ')
        if fields[0] == alias: 
            logger.debug('found panel id %s' % (fields[1]))
            return fields[1]

if __name__ == "__main__":
    def test_alias_for_id(tname):
        import random
        ranlst = ['%010d'%random.randint(0,1000000) for i in range(5)]
        #panel_id = 3925999616-0996663297-3791650826-1232098304-0953206283-2655595777-0520093719
        panel_id = '-'.join(ranlst)
        alias = alias_for_id(panel_id, fname='./aliases-test.txt')
        print('alias:', alias)
  
    import sys
    print(80*'_')
    logging.basicConfig(format='[%(levelname).1s] %(filename)s L%(lineno)04d: %(message)s', level=logging.DEBUG)
    tname = sys.argv[1] if len(sys.argv)>1 else '1'
    if tname == '1': test_alias_for_id(tname)
    else: sys.exit('Not recognized test name: "%s"' % tname)
    sys.exit('End of %s' % sys.argv[0])

# EOF
