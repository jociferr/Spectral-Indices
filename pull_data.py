import pickle
import BDNYC
import asciitable

def pull_data(sampletable):
    '''
    Function that pulls data from the BDNYC database. Run this in the same directory
    in which you have the Python Database stored!

    Input: 
    ASCII table with unum, type, resolution, instrument, date,
    and filter/order for each data set in the sample.

    Outputs:
    specData: list of arrays with wavelength in position 0, flux is position 1,
    and uncertainty in position 2 if included in database.
    targetinfo: lost of each target instance of the objects.
    '''
    f=open('BDNYCData.txt','rb')
    bdnyc=pickle.load(f)
    f.close()
    
    objects = asciitable.read(sampletable)

    specData = []
    targetinfo = []

    for x in range(len(objects)):
        target = bdnyc.match_unum(objects.unum[x])
        res = objects.res[x]
        instrument = objects.inst[x]
        filter = objects.filter[x]
        date = objects.date[x]
        if objects.type[x] == 'nir':
            data = bdnyc.targets[target].nir[res][instrument][date][filter]
        if objects.type[x] == 'mir':
            data = bdnyc.targets[target].mir[res][instrument][date][filter]
        if objects.type[x] == 'opt':
            data = bdnyc.targets[target].opt[res][instrument][date][filter]
        wl_array = data['wl']
        flux_array = data['flux']
        objData = [wl_array,flux_array]
        if len(data.keys()) >= 3:
            if data.keys()[2] == 'uncertainty':
                uncertainty_array = data['uncertainty']
                objData.append(uncertainty_array)
        
        targetinfo.append(bdnyc.targets[target])
        specData.append(objData)

    return [specData,targetinfo]
