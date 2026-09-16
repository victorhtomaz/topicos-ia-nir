import re
import seaborn as sns
import matplotlib.pyplot as plt

import NIR_SORT_py_functions as ns

# -----------------------------
#This Python script plots FTIR traces from the main dataset, overlaying requested 
# experiments. If using data from the Data Grabs folder, adjust 'collect data 
# from the database' section accordingly.
#
#A. Landauer; July 8, 2024; Material Measurement Lab, NIST
# -----------------------------

#  ----------------------------------------------------------------------------
#  ---------------- USER SPECIFIED PARAMETERS ---------------------------------
#  ----------------------------------------------------------------------------

#Note that the selection is full factorial within the lists 
# specified. To exclude data from a sub-folder either rename the
# folder in the file explorer, run this script multiple times 
# (once for each subset, changing the list options), or find 
# another solution in Python.
#Valid list entries are the folder names in the dataset.
instrument_type = ["Spectroscopy"] 
modality = ["NearInfrared"]
instrument = ["Benchtop_N"]
datatype = ["Reflectance","Absorbance"]
sourceid = ["Source_A","Source_B"]

#Data file types to grab
sufixes = ["csv"]

#Specify the data range and fiber type to collect traces from
data_range = range(2,4) # or, e.g., = [0,3,7]
fiber_type = re.compile('a') # for example, grab from type "a"

#  ----------------------------------------------------------------------------
#Collect data from the database
#  ----------------------------------------------------------------------------

#Make a nested list of paths
path_type_list = [instrument_type,modality,instrument,datatype,sourceid,sufixes]

#Used the helper function to make the full list of paths                
pathlist_full = ns.generate_path_list(path_type_list)

#Get the subset of file names
filenames_sub = ns.get_filename_subset(pathlist_full,fiber_type,data_range)

#Load the data from that subset of files
NIR_data = ns.load_csv_to_df(filenames_sub)

#  ----------------------------------------------------------------------------
#Set up plotting and plot with Seaborn
#  ----------------------------------------------------------------------------

#Page format
sns.set_theme(style="white")

#Set up plotting space with matplotlib
fig, ax1 = plt.subplots(ncols=2,nrows=2,figsize=(14,9),layout='constrained')
fig.suptitle('Basic data examples')

#Loop through the conditions selected - this needs to be edited for a specific 
# set of folders/data subsetting 

#Loop on absorbance vs reflectance
for AorR in [0,1]:
    #Loop on wavelength vs wavenumber
    for NumorLng in [0,1]:
        #grab out the appropriate subset of data from the complete dataframe
        subset_of_NIR_data = NIR_data[NIR_data["datatype"].isin([datatype[AorR]])]
        
        #adjust plotting - axis labels etc
        if NumorLng == 0:
            sns.lineplot(ax=ax1[AorR,NumorLng],data=subset_of_NIR_data, estimator=None, errorbar=None, x="wavelength", y="intensity", hue="sourceid", style="dataset_num")
            if subset_of_NIR_data.iloc[0].datatype == 'Absorbance':
                ax1[AorR,NumorLng].set(xlabel='Wavelength [nm]', ylabel='Absorbance [a.u.]')
            elif subset_of_NIR_data.iloc[0].datatype == 'Reflectance':
                ax1[AorR,NumorLng].set(xlabel='Wavelength [nm]', ylabel='Reflectance [% reflectance]')
            else:
                print("incorrect datatype found")
        else:
            sns.lineplot(ax=ax1[AorR,NumorLng],data=subset_of_NIR_data, estimator=None, errorbar=None, x="wavenumber", y="intensity", hue="sourceid", style="dataset_num")
            ax1[AorR,NumorLng].invert_xaxis()
            if subset_of_NIR_data.iloc[0].datatype == 'Absorbance':
                ax1[AorR,NumorLng].set(xlabel='Wavenumber [cm$^{-1}$]', ylabel='Absorbance [a.u.]')
            elif subset_of_NIR_data.iloc[0].datatype == 'Reflectance':
                ax1[AorR,NumorLng].set(xlabel='Wavenumber [cm$^{-1}$]', ylabel='Reflectance [% reflectance]')
            else:
                print("incorrect datatype found")
