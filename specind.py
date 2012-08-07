'''
Name: spec_ind

Created: June 5, 2012

Author: Jocelyn Ferrara

Repository: https://github.com/jociferr/Spectral-Indices

Requirements: numpy, astrotools, csv, matplotlib, input file of
spectral indices (currently 'indices_nir.txt') formatted as comma
separated values. specData & targetinfo are specific outputs from
pull_data function.
'''

import numpy
import csv
from matplotlib.patches import Rectangle
import matplotlib
import matplotlib.pyplot as plt
import astrotools
# astrotools module can be found at:
# https://github.com/BDNYC/astrotools
# We will use the avg_flux function to measure our indices.

def spec_ind(indices_file, specData, objname, plot=True):
    '''
    Measure the spectral indices as specified by an input file. The
    output is a dictionary containing the name of the spectral index
    and its value.
    
      *indices_file*
        File formatted as comma separated values that contains, in
        the following order:
          Author&Year,Line,NumMin,NumMax,DenMin,DenMax
    
      *specData*
        Spectrum as a Python list or array with wavelength in position
        0 and flux in position 1. Use either read_spec (fits files) or
        pull_data (from database) to get these arrays.

      *targetinfo*
        Target instance of the object, from the BDNYC Python Database.

      *plot*
        Boolean: Save output plot.
    
    '''

    # Read indices file.
    indices = []
    try:
        with open(indices_file, 'rb') as f:
            csvreader = csv.reader(f)
            for row in csvreader:
                if row[0][0] != "#":
                    indices.append(row)
        f.close()
    except IOError:
        print str(indices_file) + ' not found.'
        return
    
    # Store indices info in list of names and numerator/denominator ranges.
    index_name = []
    index_range = []
    for x in range(len(indices)):
        index_name.append(indices[x][1])
        index_range.append(map(float,indices[x][2:]))
    
    for y in range(len(specData)):
        
        # Initialize numerator and denominator arrays according to number
        # of spectral indices to be measured.
        length = len(index_name)
        numarray = numpy.zeros((length,1))
        denarray = numpy.zeros((length,1))
        signum = [0]*length
        sigden = [0]*length
        sig_ind = []


        # Use avg_flux function (outputs [avgflux,stddev]) over numerator and
        # denominator ranges, then calculate indices by dividing.
        for x in range(len(index_range)):
            [numarray[x],signum[x]] = astrotools.avg_flux(index_range[x][0], index_range[x][1], specData[y])
            [denarray[x],sigden[x]] = astrotools.avg_flux(index_range[x][2], index_range[x][3], specData[y])
            sig_ind.append(numpy.sqrt((signum[x]/denarray[x])**2+(numarray[x]*sigden[x])**2/denarray[x]**4))
        
        indexarray = numarray/denarray
        
        #Polynomials:
        
        H2O_A07=indexarray[index_name.index('H2O_A07')][0]
        sig_H2O_A07=sig_ind[index_name.index('H2O_A07')]
        H2OJ=indexarray[index_name.index('H2OJ')][0]
        sig_H2OJ=sig_ind[index_name.index('H2OJ')]
        H2OH=indexarray[index_name.index('H2OH')][0]
        sig_H2OH=sig_ind[index_name.index('H2OH')]
        CH4K=indexarray[index_name.index('CH4K')][0]
        sig_CH4K=sig_ind[index_name.index('CH4K')]
        
        #Allers07
        spt_H2O_A07=(H2O_A07-0.77)/0.04
        sig_spt_H2O_A07=sig_H2O_A07/0.04
        #Burgasser07
        spt_H2OJ=1.949e1 -3.919e1*H2OJ + 1.312e2* H2OJ**2 -2.156e2* H2OJ**3 + 1.038e2* H2OJ**4 + 10
        sig_spt_H2OJ=numpy.absolute(sig_H2OJ*(-3.919e1 + 1.312e2*2*H2OJ - 2.156e2*3*H2OJ**2 + 1.038e2*4*H2OJ**3))
        spt_H2OH=2.708e1 - 8.45e1*H2OH + 2.424e2* H2OH**2 - 3.381e2* H2OH**3 + 1.491e2* H2OH**4 + 10
        sig_spt_H2OH=numpy.absolute(sig_H2OH*(-8.45e1 + 2.424e2*2*H2OH - 3.381e2*3*H2OH**2 + 1.491e2*4*H2OH**3))
        spt_CH4K=1.885e1 - 2.246e1*CH4K + 2.534e1* CH4K**2 - 4.734* CH4K**3 - 1.259e1* CH4K**4 + 10
        sig_spt_CH4K=numpy.absolute(sig_CH4K*(-2.246e1 + 2.534e1*2*CH4K - 4.734*3*CH4K**2 - 1.259e1*4*CH4K**3))
        
        spt_ind = [0]*length
        spt_ind[index_name.index('H2OJ')] = spt_H2OJ
        spt_ind[index_name.index('H2O_A07')] = spt_H2O_A07
        spt_ind[index_name.index('H2OH')] = spt_H2OH
        spt_ind[index_name.index('CH4K')] = spt_CH4K
        
        sig_spt = [0]*length
        sig_spt[index_name.index('H2OJ')] = sig_spt_H2OJ[0]
        sig_spt[index_name.index('H2O_A07')] = sig_spt_H2O_A07[0]
        sig_spt[index_name.index('H2OH')] = sig_spt_H2OH[0]
        sig_spt[index_name.index('CH4K')] = sig_spt_CH4K[0]
        
        spt_avg = numpy.mean([spt_H2OJ,spt_H2O_A07,spt_H2OH])
        spt_stddev = numpy.std([spt_H2OJ,spt_H2O_A07,spt_H2OH])
        spt_sigavg = numpy.mean([sig_spt_H2OJ,sig_spt_H2O_A07,sig_spt_H2OH])
        
#        if len(targetinfo[y].sptype) >= 3 and targetinfo[y].sptype[-3] in ('p',':'):
#            spnum = float(targetinfo[y].sptype[1:-3])
#        elif targetinfo[y].sptype[-2]==':':
#            spnum = float(targetinfo[y].sptype[1:-2])
#        elif targetinfo[y].sptype[-1] in ('g','b',':','d'):
#            spnum = float(targetinfo[y].sptype[1:-1])
#        else:
#            spnum = float(targetinfo[y].sptype[1:])
#        if targetinfo[y].sptype[0] == 'L':
#            sptype = spnum + 10
#        if targetinfo[y].sptype[0] == 'T':
#            sptype = spnum + 20
#        if targetinfo[y].sptype[0] == 'M':
#            sptype = spnum
        

        specind = [[0]*len(index_name)]*len(specData)
        for x in range(len(index_name)):
            specind[y][x] = ([index_name[x], indexarray[x][0],spt_ind[x]])
        #note, add sptype back to end of specind
        
        #Make Plots
        colors = ['blue','darkblue','dodgerblue','darkcyan','darkgreen','green','darkred','red']
        fig = plt.figure(figsize=(19,11))
        plt.plot(specData[y][0],specData[y][1],c='k')
        plt.xlim(specData[y][0][0],specData[y][0][-1])
        patches = []
        lo = plt.ylim()[1]/12
        for x in range(len(index_range)):

            # Make rectangle for numerator range.
            yindex1 = numpy.where(specData[y][0]>=index_range[x][0])
            yindex2 = numpy.where(specData[y][0]<=index_range[x][1])
            ymedian = yindex1[0][0] + (yindex2[0][-1]-yindex1[0][0])/2
            numx = index_range[x][0]
            numy = specData[y][1][ymedian]-signum[x]
            numwidth = index_range[x][1]-index_range[x][0]
            numheight = signum[x]*2
            numrec = Rectangle((numx,numy),numwidth,numheight,color=colors[x])
            patches.append(numrec)
            plt.gca().add_patch(numrec)
            
            # Make rectangle for denominator range.
            yindex1 = numpy.where(specData[y][0]>=index_range[x][2])
            yindex2 = numpy.where(specData[y][0]<=index_range[x][3])
            ymedian = yindex1[0][0] + (yindex2[0][-1]-yindex1[0][0])/2
            denx = index_range[x][2]
            deny = specData[y][1][ymedian]-sigden[x]
            denwidth = index_range[x][3]-index_range[x][2]
            denheight = sigden[x]*2
            denrec = Rectangle((denx,deny),denwidth,denheight,color=colors[x])
            patches.append(denrec)
            plt.gca().add_patch(denrec)
            
            # Put object info in top left corner.
#            objname = targetinfo[y].unum
#            plt.figtext(0.1115,0.86,objname)
#            plt.figtext(0.15,0.84,targetinfo[y].name)
#            plt.figtext(0.15,0.82,targetinfo[y].sptype+", "+"%.1f"%sptype)

            # Put NIR index predicted spectral type info in top right corner.
            plt.text(denx,deny-0.6*lo,index_name[x],color=colors[x])
            plt.text(denx,deny-lo,"%.2f" % specind[y][x][1],color=colors[x])
            heights = [0.8,0,0.78,0.76,0.74]
            plt.figtext(0.75,0.82,"NIR Index Predicted Type",color='r')
            if spt_ind[x] != 0:
                plt.text(denx,deny-1.3*lo,"%.2f" % spt_ind[x],color=colors[x])
                plt.figtext(0.75,heights[x],index_name[x]+' = '+"%.2f"%spt_ind[x]+"$\pm$"+"%.2f"%sig_spt[x],color=colors[x])
            plt.figtext(0.75,0.72,'Overall Average = '+"%.2f"%spt_avg)
            plt.figtext(0.75,0.7,'Std Dev = '+"%.2f"%spt_stddev)
            plt.figtext(0.75,0.68,'Uncertainty = '+"%.2f"%spt_sigavg)

            plt.title(objname)
        print y

        if plot:
            # Save plot with UNum.pdf as name.
            figpath = '/Users/Joci/Research/Data/Templates/' + objname + '.pdf'
            plt.savefig(figpath)
        
        # Save index data with UNum_specind.txt as name.
        filepath = '/Users/Joci/Research/Data/Templates/'+objname+'_specind.txt'
        with open(filepath, 'wb') as f:
            writer = csv.writer(f)
            writer.writerow(['Index Name','Index Value','NIR Index Predicted Type','Optical Type'])
            writer.writerows(specind[y])
