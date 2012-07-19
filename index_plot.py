'''
Name: index_plot

Created: July 11, 2012

Author: Jocelyn Ferrara

Repository: https://github.com/jociferr/Spectral-Indices

Requirements: matplotlib
'''

import matplotlib
import csv
import asciitable
import matplotlib.pyplot as plt
import os

def index_plot(sampletable):
    '''
    Expects output from specind.py -- the resulting .txt files.
    Format:
    Index Name,Index Value,NIR Index Predicted Type,Optical Type
    '''

    # Initialize data structures for specified indices.
    H2OJ = [[],[]]
    H2O_A07 = [[],[]]
    H2OH = [[],[]]

    # Read out the input table (that was also used for pull_data)
    objects = asciitable.read(sampletable)
    for x in range(len(objects)):
        unum = objects.unum[x]
        spt_ind = unum + '_specind.txt'
        try:
            with open(spt_ind, 'rb') as f:
                csvreader = csv.reader(f)
                for row in csvreader:
                    if row[0] == 'H2OJ':
                        H2OJ[0].append(float(row[3]))
                        H2OJ[1].append(float(row[2]))
                    if row[0] == 'H2O_A07':
                        H2O_A07[0].append(float(row[3]))
                        H2O_A07[1].append(float(row[2]))
                    if row[0] == 'H2OH':
                        H2OH[0].append(float(row[3]))
                        H2OH[1].append(float(row[2]))
            f.close()
        except IOError:
            print str(unum)+'_specind.txt not found. Please check that present working directory contains these outputs.'
            return
    # Plot the data for each index.
    plt.figure(1,figsize=(19,11))
    
    plt.subplot(221)
    plt.scatter(H2OJ[0],H2OJ[1],marker='^',c='k',facecolor='none',s=30,label='H$_2$O-J Burgasser')
    plt.scatter(H2O_A07[0],H2O_A07[1],marker='+',c='k',s=30,label='H$_2$O Allers')
    plt.scatter(H2OH[0],H2OH[1],marker='o',c='k',facecolor='none',s=30,label='H$_2$O-H Burgasser')
    plt.legend(loc=2,scatterpoints=1,frameon=False)

    # Set limits- M8 to T0 on y-axis, L0 to L8 on x-axis                                                                                                                                                  
    plt.ylim((7.5,21))
    plt.xlim((9.5,18.5))
    plt.xlabel('Optical Type',size='large')
    plt.ylabel('NIR Index Predicted Type',size='large')
    y_ticks = ['M8','L0','L2','L4','L6','L8','T0']
    x_ticks = ['L0','L1','L2','L3','L4','L5','L6','L7','L8']
    plt.yticks(range(8,21,2),y_ticks)
    plt.xticks(range(10,19),x_ticks)

    # Plot x=y line, and +/- 1 spectral type lines.                                                                                                                                                       
    plt.plot([9,19],[9,19],'k')
    plt.plot([9,19],[10,20],'k--')
    plt.plot([9,19],[8,18],'k--')


    plt.subplot(222)
    plt.scatter(H2OJ[0],H2OJ[1],marker='^',c='k',facecolor='none',s=30,label='H$_2$O-J Burgasser')
    
    plt.legend(loc=2,scatterpoints=1,frameon=False)
    
    # Set limits- M8 to T0 on y-axis, L0 to L8 on x-axis
    plt.ylim((7.5,21))
    plt.xlim((9.5,18.5))
    plt.xlabel('Optical Type',size='large')
    plt.ylabel('NIR Index Predicted Type',size='large')
    y_ticks = ['M8','L0','L2','L4','L6','L8','T0']
    x_ticks = ['L0','L1','L2','L3','L4','L5','L6','L7','L8']
    plt.yticks(range(8,21,2),y_ticks)
    plt.xticks(range(10,19),x_ticks)

    # Plot x=y line, and +/- 1 spectral type lines.
    plt.plot([9,19],[9,19],'k')
    plt.plot([9,19],[10,20],'k--')
    plt.plot([9,19],[8,18],'k--')

    plt.subplot(223)
    plt.scatter(H2O_A07[0],H2O_A07[1],marker='+',c='k',s=30,label='H$_2$O Allers')
    
    plt.legend(loc=2,scatterpoints=1,frameon=False)
    
    # Set limits- M8 to T0 on y-axis, L0 to L8 on x-axis
    plt.ylim((7.5,21))
    plt.xlim((9.5,18.5))
    plt.xlabel('Optical Type',size='large')
    plt.ylabel('NIR Index Predicted Type',size='large')
    y_ticks = ['M8','L0','L2','L4','L6','L8','T0']
    x_ticks = ['L0','L1','L2','L3','L4','L5','L6','L7','L8']
    plt.yticks(range(8,21,2),y_ticks)
    plt.xticks(range(10,19),x_ticks)

    # Plot x=y line, and +/- 1 spectral type lines.
    plt.plot([9,19],[9,19],'k')
    plt.plot([9,19],[10,20],'k--')
    plt.plot([9,19],[8,18],'k--')

    plt.subplot(224)
    plt.scatter(H2OH[0],H2OH[1],marker='o',c='k',facecolor='none',s=30,label='H$_2$O-H Burgasser')
    
    plt.legend(loc=2,scatterpoints=1,frameon=False)
    
    # Set limits- M8 to T0 on y-axis, L0 to L8 on x-axis
    plt.ylim((7.5,21))
    plt.xlim((9.5,18.5))
    plt.xlabel('Optical Type',size='large')
    plt.ylabel('NIR Index Predicted Type',size='large')
    y_ticks = ['M8','L0','L2','L4','L6','L8','T0']
    x_ticks = ['L0','L1','L2','L3','L4','L5','L6','L7','L8']
    plt.yticks(range(8,21,2),y_ticks)
    plt.xticks(range(10,19),x_ticks)

    # Plot x=y line, and +/- 1 spectral type lines.
    plt.plot([9,19],[9,19],'k')
    plt.plot([9,19],[10,20],'k--')
    plt.plot([9,19],[8,18],'k--')


    plt.show()
    filename = os.path.splitext(sampletable)[0]
    plt.savefig('/Users/Joci/Research/specind_plots/'+filename+'_indiv.pdf')
