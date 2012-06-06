'''
Code to measure the nir spectra of L-dwarfs. Not quite flexible yet.
For use by Kelle Cruz's team at Hunter College and AMNH.

Created: June 5, 2012

Author: Jocelyn Ferrara

Repository: https://github.com/jociferr/Spectral-Indices

Requirements: numpy, astrotools
'''

# For now, spectral indices will be hard coded into the program. Goal
# for the future is to read in a file (like 'indices_nir.lis') that
# contains the spectral index information, and allow user to choose
# which to measure.

# Spectral indices to use:
# Allers07,H2O_A07,1.55,1.56,1.492,1.502
# Allers07,Na,1.15,1.16,1.134,1.144
# Burgasser06,H2OJ,1.140,1.165,1.260,1.285
# Burgasser06,H2OH,1.480,1.520,1.560,1.600
# Burgasser06,CH4K,2.215,2.255,2.080,2.120
# ModMcLean03,FeH-z,0.965, 0.985, 0.990, 1.01

import numpy
import scipy

import astrotools as at
# astrotools module can be found at:
# https://github.com/BDNYC/astrotools
# We will use the avg_flux function to measure our indices.

# Current goal: Just measure spectral indices. No pretty plots or
# inputs or anything yet.

def spec_ind(spec_data):
    '''
    First giant monster function that is going to do everything!

    Spectral indices hard coded in-- using above list.

    Parameters:
    *wl_array*
      The array containing wavelength data.
    *flux_array*
      The array containing flux data.

    Returns:
    List including the name & value of the index! (for now)
    '''
    
    namelist = ['H2OA07', 'Na', 'H20J', 'H2OH', 'CH4K', 'FeH-z']
    rangelist = [[1.55,1.56,1.492,1.502],[1.15,1.16,1.134,1.144],[1.140,1.165,1.260,1.285],[1.480,1.520,1.560,1.600],[2.215,2.255,2.080,2.120],[0.965,0.985,0.990,1.01]]    
    
    # Initialize numerator and denominator arrays according to number
    # of spectral indices to be measured.
    length = len(namelist)
    numarray = numpy.zeros((length,1))
    denarray = numpy.zeros((length,1))
    
    # Use avg_flux function from astrotools over numerator and
    # denominator ranges, then calculate indices
    for x in range(len(rangelist)):
        numarray[x] = at.avg_flux(rangelist[x][0], rangelist[x][1], spec_data)
        denarray[x] = at.avg_flux(rangelist[x][2], rangelist[x][3], spec_data)
    
    indexarray = numarray/denarray
    
    # Put everything into a list of dictionaries.
    spec_ind = []
    for x in range(len(namelist)):
        dictionary = {namelist[x]:indexarray[x][0]}
        spec_ind.append(dictionary)
    
    return spec_ind

# if __name__ == "__main__":
# defines our main method
