# import
import psana
import PSCalib.GlobalUtils as gu


def init_psana(tname) :
    """initialize psana
    """
    dsname, src = None, None
    
    if   tname == '1' :
        #dsname = '/reg/g/psdm/detector/data_test/types/0018-MfxEndstation.0-Epix100a.0.xtc' # 'exp=mfxm5116:run=20'
        dsname = 'exp=mfxm5116:run=20'
        src = psana.Source('MfxEndstation.0:Epix100a.0') # or 'VonHamos'

    elif tname == '2' :
        dsname = '/reg/g/psdm/detector/data_test/types/0019-XppGon.0-Epix100a.0.xtc' # 'exp=xppl1316:run=193'
        src = psana.Source('XppGon.0:Epix100a.0')

    elif tname == '3' :
        dsname = '/reg/g/psdm/detector/data_test/types/0007-NoDetector.0-Epix100a.0.xtc' # 'exp=xppi0614:run=74'
        src = psana.Source('NoDetector.0:Epix100a.0')
 
    ds  = psana.DataSource(dsname)
    evt = ds.events().next()
    env = ds.env()

    print 'calib_dir: %s' % gu.calib_dir(env)
    print 'exp_name : %s' % gu.exp_name(env)
    print 'alias_for_src_name : %s' % gu.alias_for_src_name(env)

    #print 'src_name_from_alias:\n'
    #gu.src_name_from_alias(env)

    #for i, evt in enumerate(ds.events()) :
    #    print 'event %d' % i
    #    o = evt.get(psana.CsPad.DataV2, src)
    #    if o is not None : 
    #        print o.data()
    #        break
    #runnum = evt.run()

    print 80*'_', '\nenv.configStore().keys():\n'
    for k in env.configStore().keys() : print k

    print 80*'_', '\nevt.keys():\n'
    for k in evt.keys() : print k

    print 80*'_'

    return ds, src, evt, env

#------------------------------

def get_epix_config_object(e, s) :
    """get epix config object
    """
    cs = e.configStore()
    o = cs.get(psana.Epix.Config100aV2, s)
    if o is not None : return o

    o = cs.get(psana.Epix.Config100aV1, s)
    if o is not None : return o

    return None

#------------------------------

def print_epix100_id(tname) :

    ds, src, evt, env = init_psana(tname)

    o = get_epix_config_object(env, src)
    
    if o is None :
        print 'get_epix_config_object returns None'
        return

    print 'version         :', o.version()   
    print 'Version         :', o.Version
    print 'numberOfColumns :', o.numberOfColumns()
    print 'numberOfRows    :', o.numberOfRows()
    print 'TypeId          :', o.TypeId
    print 'digitalCardId0/1:', o.digitalCardId0(), '/', o.digitalCardId1()
    print 'analogCardId0/1 :', o.analogCardId0(), '/', o.analogCardId1()
    print 'carrierId0/1    :', o.carrierId0(), '/', o.carrierId1()

#------------------------------

def print_epix100_id_cpo(tname) :
    """cpo version of epix100_id
    """
    ds, src, evt, env = init_psana('2')
    o = get_epix_config_object(env, src)

    print 'carrierId0/1     :', str(o.carrierId0())+'/'+str(o.carrierId1())
    print 'digitalCardId0/1 :', str(o.digitalCardId0())+'/'+str(o.digitalCardId1())
    print 'analogCardId0/1  :', str(o.analogCardId0())+'/'+str(o.analogCardId1())
    print 'version          :', o.version()   

#------------------------------

if __name__ == "__main__" :
    import sys

    tname = '1' if len(sys.argv) < 2 else sys.argv[1]
    if tname in ('1', '2', '3') : print_epix100_id(tname)
    elif tname == '4' : print_epix100_id_cpo(tname)
    else : sys.exit ('Not recognized test name: "%s"' % tname)

    sys.exit ('End of %s' % sys.argv[0])

#------------------------------
