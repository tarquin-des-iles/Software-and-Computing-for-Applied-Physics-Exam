# -*- coding: utf-8 -*-
"""
Auteur : Louis Moreau-Brefe
Date : 13/08/2026
Description : Pollinic diagrams 
"""

import pandas as pd
import numpy as np
from pathlib import Path

def extract(file_path):
    """
    Use Pandas library to extract the excel file to generate
    a Data Frame, excluding the header structure beacause useless

    Parameter : 
        file_path : path to the excel file
    
    Return : 
        A Pandas Data Frame

    Raise : 
        TypeError if the file_path is not a string
        AssertionError if the file do not lead to a Excel file 

    """
    # Testing the type
    if type(file_path) != str :
        raise TypeError("The path is not a string")

    # Test the existence and pertinence of the path
    path = Path(file_path)
    assert path.exists(), "No such path"
    assert path.is_file(), "No file at the end of the path"
    assert path.suffix.lower() in [".xlsx", ".xls"], "The extension do not seem to be the one of an Excel file"

    # Testing if we effectively have a Excel file
    try : 
        pd.ExcelFile(path)
    except Exception as e:
        raise AssertionError("The document is not a valid Excel file") from e

    # If everything is fine, extract the excel file with pandas and print the Data Frame
    data = pd.read_excel(file_path, header = None)
    print("The excel file treated by pandas is : ")
    print(data)
    print()
    return data

# For the depth, we select the first line, we transform each value in an integer and exclude the NaN type due to the first empty cell.

def gen_data(data_frame): 
    """
        Generate an appropriate dictionnary including for keys the plant names and as values the quantity
        of pollen found for each layer, and an array of the layer lengths 
    
        Parameter : 
            data : Pandas Data Frame
        
        Return : 
            A dictionnary and a numpy array
    
        Raise : 
           TypeError if data is not a Data Frame
           TypeError if the first line is not composed of floating or integer object
    """
    # Testing if the argument is a Data Frame
    assert isinstance(data_frame, pd.DataFrame), f"{data_frame} is not a Data Frame. Check gen_data argument."

    # Generating the numpy array of layer lengths : we take the first line and convert into a numpy array 
    depth = np.array(data_frame.iloc[0])
    depth = depth[1:].astype(float)
    n_depth = len(depth)
    print("For the data Test_1, we obtain the following depth array : ", depth)
    print(f"It contains {n_depth} layers.")
    print()

    # Generating the dictionnary : we isolate the first column with the taxa names, that will correspond to the 
    # keys of the dict, we verify that they are all strings and we generate all the arrays corresponding to every 
    # sampling in our core. 

    # Keys
    keys = np.array(data_frame[0])[1:]
    assert np.all(keys == keys.astype(str)), "The column of the taxas names is not fully composed of names. Check it values."
    n_keys = len(keys)
    print("The taxa studied in Test_1 are the following :", keys)
    print()

    # Values : we go on all the line of the Data Frame, excluding the name and converting the NaN data into 0
    values = [data_frame.iloc[i][1:].fillna(0).astype(float).to_numpy() for i in range(1, n_keys)]

    # Generating the dictionnary 
    dictio = {}
    dictio = dict(zip(keys, values))
    print("We obtain the following dictionnary for Test_1 data : ", dictio)
    print()

    return dictio, depth
