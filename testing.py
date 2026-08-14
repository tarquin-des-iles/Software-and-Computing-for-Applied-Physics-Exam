# -*- coding: utf-8 -*-
"""
Auteur : Louis Moreau-Brefe
Date : 13/08/2026
Description : Pollinic diagrams 
"""

import pandas as pd
import numpy as np

## Write the testing code, importing the excel files

# Example 1

data_1 = pd.read_excel("./excel/Test_1_pollen.xlsx", header = None)
print("The excel file treated by pandas of the Test_1 is : ", data_1)
print()


# Example 2

# data_2 = 

# Example 3

# data_3 = 

# Effective data 

# data_eff = 

## Appropriate storage of the information

# We want to store the data in the following manner : for each excel we obtain a dictionnary, of which the keys are
# the taxa and for each taxa corresponds a list of integers. For each dictionnary, we link another list (depth)
# from which the cells correspond to the depth of the pollen found. Thus, the values and the depth-list are both arrays of same 
# size. 

# For the depth, we select the first line, we transform each value in an integer and exclude the NaN type due to the first empty cell.

depth_1 = np.array(data_1.iloc[0])
depth_1 = depth_1[1:].astype(int)
n_depth_1 = len(depth_1)
print("For the data Test_1, we obtain the following depth array : ", depth_1)
print()

# To generate the dictionnary, we need to isolate the first column with the taxa names, which will become the keys and associate to each key the 
# rest of the line 

keys_1 = np.array(data_1[0])[1:]
n_keys_1 = len(keys_1)
print("The taxa studied in Test_1 are the following :", keys_1)
print()

values_1 = [np.array(data_1.iloc[i])[1:].astype(int) for i in range(1,n_keys_1) ]

dict_1 = dict(zip(keys_1, values_1))
print(dict_1)





