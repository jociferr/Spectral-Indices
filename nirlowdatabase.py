import asciitable
import BDNYC
import pickle
f = open('BDNYCData.txt','rb')
bdnyc = pickle.load(f)
f.close()
specData=[]
targetinfo=[]
UNUM = []
INST = []
DATE = []
RES = []
TYPE = []
FILTER = []
for x in range(len(bdnyc.targets)):
    inst =  bdnyc.targets[x].nir['low'].keys()
    if len(inst) > 0:
        for y in range(len(inst)):
            date = bdnyc.targets[x].nir['low'][inst[y]].keys()
            if len(date) > 0:
                for z in range(len(date)):
                    filter = bdnyc.targets[x].nir['low'][inst[y]][date[z]].keys()
                    if len(filter) > 0:
                        for t in range(len(filter)):
                            wl = bdnyc.targets[x].nir['low'][inst[y]][date[z]][filter[t]]['wl']
                            flux = bdnyc.targets[x].nir['low'][inst[y]][date[z]][filter[t]]['flux']
                            data = bdnyc.targets[x].nir['low'][inst[y]][date[z]][filter[t]].keys()
                            if wl[0] < 0.965 and wl[-1] > 2.120:
                                specData.append([[wl],[flux]])
                                targetinfo.append(bdnyc.targets[x])
                                UNUM.append(bdnyc.targets[x].unum)
                                INST.append(inst[y])
                                TYPE.append('nir')
                                RES.append('low')
                                DATE.append(date[z])
                                FILTER.append(filter[t])
asciitable.write({'unum':UNUM,'type':TYPE,'res':RES,'inst':INST,'date':DATE,'filter':FILTER},'sampletable.dat')
return [specData,targetinfo]
