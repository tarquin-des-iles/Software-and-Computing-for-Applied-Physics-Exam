# -*- coding: utf-8 -*-
"""
Auteur : Louis Moreau-Brefe
Date : 13/08/2026
Description : Pollinic excell data treatment
"""

import numpy as np 
import matplotlib.pyplot as plt

# Based on the file opening.py, we will use dictionnaries based on pollinic excel files. Example : 
# data = {'Taxa_1' : [1, 4, 5, 2], 
#         'Taxa_2' : [6, 2, 5, 1]}
#

def percentage(pollen_dict, core_length): 
    """
        Convert the data in the arrays for each taxa : from the absolute quantity of pollen grains
        found in a layer, we obtain the percentage this quantity reprensents with respect to the total 
        grains found
    
        Parameter : 
            pollen_dict : Data Frame of pollen excel file converted into a dictionnary 
        
        Return : 
            A dictionnary
    
        Raise : 
            TypeError if pollen_dict is not a dictionnary
            TypeError if core_length
    """
    if not isinstance(pollen_dict, dict) : 
        raise TypeError("You must insert the Data Frame dictionnary as first argument")
    if not isinstance(core_length, list) : 
        raise TypeError("You must insert the depth array as second argument")
    
    # We want to obtain the percentage occupied by each taxa in the sample : we first need to find the total quantity 
    # of grains in each layer to calculate the relative quantity occupied by each taxa quantity
    for i in range(len(core_length)):
        total = 0
        # We sum all the grains for a single layer
        for taxa in pollen_dict : 
            total += pollen_dict[taxa][i]
        # We calculate the relative quantity of grains for each taxa
        for taxa in pollen_dict : 
            pollen_dict[taxa][i] = pollen_dict[taxa][i]/total
    return pollen_dict

# # Test for the function percentage 
# data = {'Taxa_1' : [1, 4, 5, 2],  'Taxa_2' : [6, 2, 5, 1]}
# print(percentage(data, [1, 3, 6, 8]))


def single_pollinic_diag(ax, taxa, percent_pollen_list, depth_list): 
    """
        Generate a pollinic diagram for a single taxa.
    
        Parameters : 
            ax (matplotlib.axes.Axes)
            taxa (str) : take the name of a taxa for the associated title (keys of the Data Frame dictionnary)  
            pollen_list (np.array) : percentage array of grains
            depth_list (np.array) : array of layer depth
    
        Raise :   
    """

    ax.plot(percent_pollen_list, depth_list)
    if hide_labels:
        ax.set_xticklabels([])
        ax.set_yticklabels([])
    else:
        ax.set_xlabel('Abundance', fontsize=fontsize)
        ax.set_ylabel('Depth', fontsize=fontsize)
        ax.set_title(r'{taxa}', fontsize=fontsize)

# AJOUTER single_polinic A LA FONCTION SUIVANTE

def pollinic_diag(pollen_dict_percent, core_length) : 
   """
    Generate a pollinic diagram of the entire core

    Parameter : 
        pollen_dict_percent : dictionnary of the pollen Data Frame including for each taxa the percentage of it grains at each layer
        core_length : numpy array in which each cell 
    
    Return : 
        A serie of matplotlib graphics

    Raise : 
    
    """
   # We can have a big quantity of pollens to treat, so let's set that the maximum of pollens to print in the same page
   # is 10. Therefore, we will print the pollen diagrams by packs of 10, maximum.  
   n_dict = len(pollen_dict_percent)
   n_packs = n_dict//10
   n_rest = n_dict%10

   total = 0
   for i in range(n_dict):
       fig, axs = plt.subplots(1, 10, layout="constrained", sharey=True)
       for ax in axs.flat:
            example_plot(ax)
       axs[0].plot(np.arange(10))

    fig, axs = plt.subplots(1, n_rest, layout="constrained")
    


