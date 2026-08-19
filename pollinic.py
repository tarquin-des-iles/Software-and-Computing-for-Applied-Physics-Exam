# -*- coding: utf-8 -*-
"""
Auteur : Louis Moreau-Brefe
Date : 13/08/2026
Description : Pollinic excell data treatment
"""

import numpy as np 
import matplotlib.pyplot as plt
import copy

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
            TypeError if core_length is an Numpy array
            ValueError if the length of the sample for each taxa do not match the core length
    """
    if not isinstance(pollen_dict, dict) : 
        raise TypeError("You must insert the Data Frame dictionnary as first argument")
    if not isinstance(core_length, np.ndarray) : 
        raise TypeError("You must insert the depth array as second argument")
    for taxa in pollen_dict:
        if len(pollen_dict[taxa]) != len(core_length):
            raise ValueError(f"The number of values for {taxa} does not match core_length")
    
    # We want to obtain the percentage occupied by each taxa in the sample : we first need to find the total quantity 
    # of grains in each layer to calculate the relative quantity occupied by each taxa quantity
    for i in range(len(core_length)):
        total = 0
        # We sum all the grains for a single layer
        for taxa in pollen_dict : 
            total += pollen_dict[taxa][i]
        # We calculate the relative quantity of grains for each taxa
        for taxa in pollen_dict:
            pollen_dict[taxa][i] = (pollen_dict[taxa][i]/total)
    return pollen_dict


def pollinic_diag(pollen_dict_percent, core_length):
    """
    Generate pollinic diagrams of the entire core.

    Parameters:
        pollen_dict_percent (dict) : Dictionary containing the percentage of pollen for each taxa.
        core_length (Numpy array) : Depth array containing the depth of each layer.

    Returns:
        A series of matplotlib figures.

    Raises:
        TypeError if pollen_dict_percent is not a dictionary orcore_length is not a numpy array.
        ValueError if the length of the data for a taxa does not match core_length.
    """

    if not isinstance(pollen_dict_percent, dict):
        raise TypeError("You must insert the Data Frame dictionary as first argument")
    if not isinstance(core_length, np.ndarray):
        raise TypeError("You must insert the depth array as second argument")

    for taxa in pollen_dict_percent:
        if len(pollen_dict_percent[taxa]) != len(core_length):
            raise ValueError(f"The number of values for {taxa} does not match core_length")

    # We want to control the number of graphics that we display in a single page : we fix the size of the page. 
    PAGE_WIDTH = 15
    PAGE_HEIGHT = 8

    # Then, we want each graphic to be of a specific size : we fix a scale limit for which : 
    # Above this value, we will have fewer graphs per page
    # Under this value, we will display more graphs per page
    SCALE = 8
    MIN_WIDTH = 2

    # Convert dictionary into a list : it will contain lists of tuples 
    taxa_data = list(pollen_dict_percent.items())

    # We want every graph to be restricted on a value of x for the graphs to be all comparable
    global_max = max(max(values)for taxa, values in taxa_data)
    X_MAX = global_max * 1.05

    i = 0
    while i < len(taxa_data):
        # We determine which taxa can fill in a single page
        page_data = []
        total_width = 0
        # In fact, we fill page_data as much as possible
        while i + len(page_data) < len(taxa_data):
            taxa, values = taxa_data[i + len(page_data)]
            max_value = max(values)
            # Physical width of the graph in the loop
            graph_width =  max(MIN_WIDTH, max_value * SCALE)
            # Particular case : small graphs must still have a width to be observable
            graph_width = max(graph_width, 0.5)
            # We control the if this data can effectively fill
            if total_width + graph_width <= PAGE_WIDTH:
                page_data.append((taxa, values))
                total_width += graph_width
            else:
                break

        # Now that we have the data that can effectively fit in one page, we need to create it

        # We want two things for the fixed number of graphs in our page :
        # 1. Each graph must occupy a certain space in the page, proportionaly to it size
        # 2. The x-axis for each graph must remain the same for the comparaison between them to be pertinent

        # We print the entire page
        fig = plt.figure(figsize = (PAGE_WIDTH, PAGE_HEIGHT))

        # We define such ratios to give it own space to each graph 
        width_ratios =  [max(MIN_WIDTH, max(values) * SCALE) for taxa, values in page_data]
        # We use gridspec (gs) to display correcty the data with the appropriate ratios
        gs = fig.add_gridspec(1, len(page_data), width_ratios = width_ratios)
        # Each axis has it own length and we want the plots to share there y axis 
        axis = []
        for j in range(len(page_data)):
            if j == 0:
                ax = fig.add_subplot(gs[0, j])
            else:
                ax = fig.add_subplot(gs[0, j], sharey=axis[0])
            axis.append(ax)

        # Now let's effecticely plot the data
        for j, (taxa, values) in enumerate(page_data):
            ax = axis[j]
            # Plot the curve
            ax.plot(values, core_length)
            # Fill area between y-axis and curve
            ax.fill_betweenx(core_length, 0, values, alpha = 0.3)
            # Adapt x-axis to the data
            ax.set_xlim(0, X_MAX)
            # Title
            ax.set_title(taxa, rotation = 45,)
            # Grid
            ax.grid()

        # All diagrams must have the same depth scale because in the core all the pollen are 
        # hypothetical sampled  
        for ax in axis:
            ax.set_ylim(max(core_length), min(core_length))

        plt.tight_layout()
        plt.show()

        # Move to the next page
        i += len(page_data)


