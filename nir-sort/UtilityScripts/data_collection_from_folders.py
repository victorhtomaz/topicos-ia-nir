import os
import shutil
import glob
import csv
import pandas as pd
import NIR_SORT_py_functions as ns

# -----------------------------
#This Python script copies files from multiple subdirectories in the 
# NIR-SORT dataset to a common folder with the option to convert from  
# wavenumber to wavelength
#
#A. Landauer; revised July 12, 2024; Material Measurement Lab, NIST
# -----------------------------

#List of categories from which to collect data. 
#
#Note that the selection is full factorial within the lists 
# specified. To exclude data from a sub-folder either rename the
# folder in the file explorer, run this script multiple times 
# (once for each subset, changing the list options), or find 
# another solution more clever than mine.
#

#Write out files as wavenumber of wavelength
write_out_units = "wavenumber" #change to "wavelength" for wavelength

#Valid list entries are the folder names in the dataset.
instrument_type = ["Spectroscopy"] 
modality = ["NearInfrared"]
instrument = ["Benchtop_N"]
datatype = ["Absorbance"]
sourceid = ["Source_A","Source_B"]


#Data file types to grab
suffixes = ["CSV","csv"]

#Make a nested list of them
path_type_list = [instrument_type,modality,instrument,datatype,sourceid,suffixes]

#Used the helper function to make the full list of paths 
pathlist_full = ns.generate_path_list(path_type_list)


#Common folder to extract data files into (if it does not exist, make it)
data_dump = "../DataGrabs"
isExist = os.path.exists(data_dump)
if not isExist:
   os.makedirs(data_dump)

print('Starting copy to ' + data_dump)
#For each path in the list, look for files with the correct extension and copy 
# them into the target folder
for cur_path in pathlist_full:
    print(cur_path)
    file_glob = glob.glob(cur_path)
    for cur_file in file_glob:
        if write_out_units == "wavenumber":
            #if keeping wavenumber units, simply copy the files over
            shutil.copy2(cur_file, data_dump)
            
        elif write_out_units == "wavelength":
            #If switching units, read in the data, convert, and write out new files
            cur_data = pd.read_csv(cur_file)
            cur_data.columns = ['wavenumber','intensity']
            cur_data.insert(1,'wavelength', round(1e7/cur_data['wavenumber'],2))
            cur_data_lambda = cur_data.drop("wavenumber",axis=1)
            
            #Get the files name to write out
            cur_file_split = os.path.split(cur_file)
            file_to_write = [data_dump + "/" + cur_file_split[1]]
            
            #Write out the file
            cur_data_lambda.to_csv(file_to_write[0],header=False,index=False)

        else:
            #in case of typo, warn the user
            print("Improper units entered for write-out")

print('Copy to ' + data_dump + ' complete')