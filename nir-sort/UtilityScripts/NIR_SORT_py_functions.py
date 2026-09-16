import os
import sys
import shutil
import glob
import re
import numpy as np
import pandas as pd


def generate_path_list(path_type_list):
#This function generates a complete list of target paths to search from 
# a list of path option in the format: 
#   path_types_list = [instrument_type,modality,instrument,datatype,sourceid,suffixes]
    
    #Loop through each list and generate a complete list of target paths to search
    pathlist_full = []
    for it in path_type_list[0]:
        for m in path_type_list[1]:
            for inst in path_type_list[2]:
                for dt in path_type_list[3]:
                    for sid in path_type_list[4]:
                        for s in path_type_list[5]:
                                pathlist_full.append("../" + it + "/" + m  + "/" + inst + "/" + dt + "/" + sid + "/*." + s)
    
    return pathlist_full


def load_csv_to_df(full_filenames):
#This function generates a dataframe with columns for the wavenumber,
# wavelength, intensity and each type descriptor from a list of file 
# names. Each field name in the list should be a csv with the first column 
# the wavenumber and the second column the intensity. 
#   full_filenames = list of each filename (including path) to include in the 
#                    output dataframe


    df_dataset_layers = []
    cnt = 0
    for cur_file in full_filenames:
        #print(cur_file)
        path_parts = splitall(cur_file)
        cur_name = os.path.split(cur_file)[-1][0:-8]
        
        #Load the CSV file into a pandas DataFrame
        cur_data = pd.read_csv(cur_file)
        cur_data.columns = ['wavenumber','intensity']
        cur_data.insert(1,'wavelength', round(1e7/cur_data['wavenumber'],2))
        cur_data.insert(3,'instrument_type', path_parts[1])
        cur_data.insert(4,'modality', path_parts[2])
        cur_data.insert(5,'instrument', path_parts[3])
        cur_data.insert(6,'datatype', path_parts[4])
        cur_data.insert(7,'sourceid', path_parts[5])        
        cur_data.insert(8,'dataset_num', cnt)
        cur_data.insert(9,'name', cur_name)
        cnt = cnt + 1
        df_dataset_layers.append(cur_data)
    
    df_dataset = pd.concat(df_dataset_layers)

    return df_dataset

def get_filename_subset(pathlist_full,fiber_type,data_range):
    #get a subset of the files according to the specified fiber type and range 
    #of experiments.
    #   pathlist_full = list of file paths from "generate_path_list"
    #   fiber_type = regular expersion pattern for the fiber type code
    #   data_range = range variable for the experiment instances to grab
    
    #For each path in the list, look for a file with the correct extension for type a
    filenames_sub = []
    for cur_path in pathlist_full:
        file_glob = glob.glob(cur_path)
        fiber_file_matches = [fiber_type.match(x[-28]) for x in file_glob]
        
        cnt = 0
        fnum = 0
        for fnum,n in enumerate(fiber_file_matches):
            if n:
                if cnt in data_range:
                    filenames_sub.append(file_glob[fnum])
                cnt = cnt + 1
            
    return filenames_sub

def splitall(path):
    #Use split function to get each subfolder name from a path string
    #   path = complete path to a file of interest
    
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    
    return allparts
