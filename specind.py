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

def spec_ind(indices_file, specData, plot=True, verbose=True):
    '''
    Measure the spectral indices as specified by an input file. The
    output is a dictionary containing the name of the spectral index
    and its value.
    
      *indices_file*
        File formatted as comma separated values that contains, in
        the following order:
          Author&Year,Line,NumMin,NumMax,DenMin,DenMax
    
      *spec_data*
        Spectrum as a Python list or array with wavelength in position
        0 and flux in position 1.

      *plot*
        Boolean: Output spectrum with indices marked.
    
      *verbose*
        Boolean: Print warning messages.
    
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
    
    # Initialize numerator and denominator arrays according to number
    # of spectral indices to be measured.
    length = len(namelist)
    numarray = numpy.zeros((length,1))
    denarray = numpy.zeros((length,1))
    signum = [0]*length
    sigden = [0]*length
    
    # Use avg_flux function from astrotools over numerator and
    # denominator ranges, then calculate indices by dividing.
    for x in range(len(rangelist)):
        [numarray[x],signum[x]] = astrotools.avg_flux(rangelist[x][0], rangelist[x][1], specData)
        [denarray[x],sigden[x]] = astrotools.avg_flux(rangelist[x][2], rangelist[x][3], specData)
    
    indexarray = numarray/denarray
    
    print signum
    print sigden

    # Put everything into a dictionary.
    spec_ind = [0]*length
    for x in range(len(namelist)):
        spec_ind[x] = [namelist[x], "%.2f" % indexarray[x][0]]


    if plot == True:
        colors = ['red','darkred','purple','blue','darkgreen','orange','green','darkblue']
        fig = plt.figure()
        plt.plot(specData[0],specData[1])
        plt.xlim(specData[0][0],specData[0][-1])
        patches = []
        lo = 2E-16
        for x in range(len(rangelist)):
            yindex = numpy.where(specData[0]>=rangelist[x][0])
            numx = rangelist[x][0]
            numy = specData[1][yindex[0][0]]-signum[x]
            numwidth = rangelist[x][1]-rangelist[x][0]
            numheight = signum[x]*2
            numrec = Rectangle((numx,numy),numwidth,numheight,color=colors[x])
            patches.append(numrec)
            plt.gca().add_patch(numrec)

            yindex = numpy.where(specData[0]>=rangelist[x][2])
            denx = rangelist[x][2]
            deny = specData[1][yindex[0][0]]-sigden[x]
            denwidth = rangelist[x][3]-rangelist[x][2]
            denheight = sigden[x]*2
            denrec = Rectangle((denx,deny),denwidth,denheight,color=colors[x])
            patches.append(denrec)
            plt.gca().add_patch(denrec)

            plt.text(denx,deny+lo,namelist[x],color=colors[x],ha='center')
            plt.text(denx,deny-lo,spec_ind[x][1],color=colors[x],ha='center')

        plt.show()

    return spec_ind

#options: plots- filenames, directory, indices(file or dictionary)
#include polynomials to predict spectral type using the indices

#polynomials:
#Allers07
#spt_H2O_A07=(H2O_A07-0.77)/0.04
#Burgasser07                                                                       
#spt_H2OJ=1.949e1 -3.919e1*H2OJ + 1.312e2*H2OJ^2 -2.156e2*H2OJ^3 + 1.038e2*H2OJ^4
#spt_H2OH=2.708e1 - 8.45e1 * H2OH + 2.424e2 * H2OH^2 - 3.381e2 *
#H2OH^3 + 1.491e2 * H2OH^4
#spt_CH4K=1.885e1 - 2.246e1* CH4K + 2.534e1 * CH4K^2 - 4.734 * CH4K^3
#- 1.259e1 * CH4K^4
#Testi                                                                             
#spt_sH2OJ=10*((1.54 * sH2OJ) + 0.98)
#
