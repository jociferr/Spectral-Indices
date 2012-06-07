'''
Code to measure the nir spectra of L-dwarfs. Not quite flexible yet.
For use by Kelle Cruz's team at Hunter College and AMNH.

Created: June 5, 2012

Author: Jocelyn Ferrara

Repository: https://github.com/jociferr/Spectral-Indices

Requirements: numpy, astrotools, csv
'''

# Takes in an input file of spectral indices.
# At this moment, 'indices_nir.txt' - must be formatted as csv (comma
# separated values) for proper reading.

import numpy
import csv
import astrotools
# astrotools module can be found at:
# https://github.com/BDNYC/astrotools
# We will use the avg_flux function to measure our indices.

def spec_ind(indices_file, spec_data, verbose=True):
    '''
    Second giant monster function that is going to do everything!
    
    Parameters:
    
      *indices_file*
        File formatted as comma separated values that contains, in
        the following order:
          Author&Year,Line,NumMin,NumMax,DenMin,DenMax
    
      *spec_data*
        Spectrum as a Python list or array with wavelength in position
        0 and flux in position 1.
    
      *verbose*
        Boolean: Print warning messages.
    
    Returns:
      
      List including the name & value of the index! (for now)
    
    '''
    
    
    indices = []
    with open(indices_file) as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            if row[0][0] != "#":
                indices.append(row)
    
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
    
    # Use avg_flux function from astrotools over numerator and
    # denominator ranges, then calculate indices
    for x in range(len(rangelist)):
        numarray[x] = astrotools.avg_flux(rangelist[x][0], rangelist[x][1], spec_data)
        denarray[x] = astrotools.avg_flux(rangelist[x][2], rangelist[x][3], spec_data)
    
    indexarray = numarray/denarray
    
    # Put everything into a dictionary.
    spec_ind = {}
    for x in range(len(namelist)):
        spec_ind[namelist[x]] = indexarray[x][0]
    
    return spec_ind

# if __name__ == "__main__":
# defines our main method
