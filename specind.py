'''
Name: spec_ind

Created: June 5, 2012

Author: Jocelyn Ferrara

Repository: https://github.com/jociferr/Spectral-Indices

Requirements: numpy, astrotools, csv, matplotlib, input file of
spectral indices (currently 'indices_nir.txt') formatted as comma
separated values.
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

def spec_ind(indices_file, specData, targetinfo, plot=True):
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
    with open(indices_file) as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            if row[0][0] != "#":
                indices.append(row)
    
    # Store indices info in list of names and numerator/denominator ranges.
    namelist = []
    rangelist = []
    for x in range(len(indices)):
        namelist.append(indices[x][1])
        rangelist.append(map(float,indices[x][2:]))

    opt_type = []
    nir_ind_type = []

    #Get Data
    #specData = astrotools.read_spec(specFiles,errors=True)
    for y in range(len(specData)):
    
        #objname = specFiles[y].rsplit('/',1)[1].split('.')[0]
        objname = targetinfo[y].unum
        
        # Initialize numerator and denominator arrays according to number
        # of spectral indices to be measured.
        length = len(namelist)
        numarray = numpy.zeros((length,1))
        denarray = numpy.zeros((length,1))
        signum = [0]*length
        sigden = [0]*length
        
        # Use PERSONAL avg_flux function (outputs [avgflux,stddev]) over numerator and
        # denominator ranges, then calculate indices by dividing.
        for x in range(len(rangelist)):
            [numarray[x],signum[x]] = astrotools.avg_flux(rangelist[x][0], rangelist[x][1], specData[y])
            [denarray[x],sigden[x]] = astrotools.avg_flux(rangelist[x][2], rangelist[x][3], specData[y])
    
        indexarray = numarray/denarray

        # Put everything into a list of list, with first element the name
        # of the index, and second element the value.
        specind = []
        for x in range(len(namelist)):
            specind.append([namelist[x], indexarray[x][0]])
    
        #Polynomials:
        poly_list = ['H2O_A07','H2OJ','H2OH','CH4K']
        polyind = [0]*len(specind)
        for name in poly_list:
            for x in range(len(specind)):
                if name == specind[x][0]:
                    polyind[x] = specind[x][0]
                
        H2O_A07=specind[polyind.index('H2O_A07')][1]
        H2OJ=specind[polyind.index('H2OJ')][1]
        H2OH=specind[polyind.index('H2OH')][1]
        CH4K=specind[polyind.index('CH4K')][1]
        #Allers07
        spt_H2O_A07=(H2O_A07-0.77)/0.04
        #Burgasser07
        spt_H2OJ=1.949e1 -3.919e1*H2OJ + 1.312e2* H2OJ**2 -2.156e2* H2OJ**3 + 1.038e2* H2OJ**4 + 10
        spt_H2OH=2.708e1 - 8.45e1*H2OH + 2.424e2* H2OH**2 - 3.381e2* H2OH**3 + 1.491e2* H2OH**4 + 10
        spt_CH4K=1.885e1 - 2.246e1*CH4K + 2.534e1* CH4K**2 - 4.734* CH4K**3 - 1.259e1* CH4K**4 + 10
        
        polyind[polyind.index('H2OJ')] = spt_H2OJ
        polyind[polyind.index('H2O_A07')] = spt_H2O_A07
        polyind[polyind.index('H2OH')] = spt_H2OH
        polyind[polyind.index('CH4K')] = spt_CH4K

        predicted = numpy.mean([spt_H2OJ,spt_H2O_A07,spt_H2OH,spt_CH4K])
        predicted_wo_CH4K = numpy.mean([spt_H2OJ,spt_H2O_A07,spt_H2OH])
        

        for x in range(len(specind)):
            specind[x] = ([namelist[x], indexarray[x][0], polyind[x]])

        #Make Plots
        colors = ['blue','darkblue','dodgerblue','darkcyan','darkgreen','green','darkred','red']
        fig = plt.figure(figsize=(19,11))
        plt.plot(specData[y][0],specData[y][1],c='k')
        plt.xlim(specData[y][0][0],specData[y][0][-1])
        patches = []
        lo = plt.ylim()[1]/12
        for x in range(len(rangelist)):
            yindex1 = numpy.where(specData[y][0]>=rangelist[x][0])
            yindex2 = numpy.where(specData[y][0]<=rangelist[x][1])
            ymedian = yindex1[0][0] + (yindex2[0][-1]-yindex1[0][0])/2
            numx = rangelist[x][0]
            numy = specData[y][1][ymedian]-signum[x]
            numwidth = rangelist[x][1]-rangelist[x][0]
            numheight = signum[x]*2
            numrec = Rectangle((numx,numy),numwidth,numheight,color=colors[x])
            patches.append(numrec)
            plt.gca().add_patch(numrec)
            
            yindex1 = numpy.where(specData[y][0]>=rangelist[x][2])
            yindex2 = numpy.where(specData[y][0]<=rangelist[x][3])
            ymedian = yindex1[0][0] + (yindex2[0][-1]-yindex1[0][0])/2
            denx = rangelist[x][2]
            deny = specData[y][1][ymedian]-sigden[x]
            denwidth = rangelist[x][3]-rangelist[x][2]
            denheight = sigden[x]*2
            denrec = Rectangle((denx,deny),denwidth,denheight,color=colors[x])
            patches.append(denrec)
            plt.gca().add_patch(denrec)
            
            plt.figtext(0.15,0.86,objname)
            plt.figtext(0.15,0.84,targetinfo[y].name)

            spnum = float(targetinfo[y].sptype[1:])
            if targetinfo[y].sptype[0] == 'L':
                spnum = spnum + 10
            plt.figtext(0.15,0.82,targetinfo[y].sptype+", "+"%.1f"%spnum)

            plt.text(denx,deny-0.6*lo,namelist[x],color=colors[x])
            plt.text(denx,deny-lo,"%.2f" % specind[x][1],color=colors[x])
            heights = [0.8,0,0.78,0.76,0.74]
            plt.figtext(0.75,0.82,"NIR Index Predicted Type",color='r')
            if polyind[x] != 0:
                plt.text(denx,deny-1.3*lo,"%.2f" % polyind[x],color=colors[x])
                plt.figtext(0.75,heights[x],namelist[x]+' = '+"%.2f"%polyind[x],color=colors[x])
            plt.figtext(0.75,0.72,'Overall Average = '+"%.2f"%predicted)
            plt.figtext(0.75,0.7,'Average w/o CH4K = '+"%.2f"%predicted_wo_CH4K)

            plt.show()

        if plot:
            figpath = '/Users/Joci/Research/specind_plots/' + objname + '.pdf'
            plt.savefig(figpath)
        
        filepath = '/Users/Joci/Research/specind_plots/'+objname+'_specind.txt'
        with open(filepath, 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(specind)

        opt_type.append(spnum)
        nir_ind_type.append(predicted)
