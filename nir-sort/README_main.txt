===============================================================================
<<<>><<>><<>><<>><<>><<>><<| NIST Data Publication |>><<>><<>><<>><<>><<>><<>>>
===============================================================================

 Near Infrared Spectra of Origin-defined and Real-world Textiles (NIR-SORT):
   A spectroscopic and materials characterization dataset for known 
   provenance and post-consumer fabrics


<<<>><<>><<>><<>><<>><<>><<>>| Author and Version |<<>><<>><<>><<>><<>><<>><<>>

Authors:
  Katarina E Goodge
    National Institute of Standards and Technology
    Materials Measurement Science Division
    Georgetown University, Washington, D.C., USA
    Institute for Soft Matter Synthesis and Metrology

  Cecelia J Vederman
    National Institute of Standards and Technology
    Materials Measurement Science Division
    Montgomery College

  Radha V Patel
    National Institute of Standards and Technology
    Materials Measurement Science Division
    Georgetown University, Washington, D.C., USA
    Institute for Soft Matter Synthesis and Metrology

  Charlotte M Wentz
    National Institute of Standards and Technology
    Materials Measurement Science Division

  Zois Tsinas
    National Institute of Standards and Technology
    Materials Measurement Science Division
    Theiss Research, La Jolla, CA, USA

  Alexander K Landauer
    National Institute of Standards and Technology
    Materials Measurement Science Division

  Amanda L Forster
    National Institute of Standards and Technology
    Materials Measurement Science Division

Contact:
  Amanda Forster
    Amanda.forster@nist.gov
  
  Katarina Goodge
    katarina.goodge@nist.gov

Version 2.0.0
DOI: https://doi.org/10.18434/mds2-3325


<<>><<>><<>><<>><<>><<>><<>>| Dataset Description |<<>><<>><<>><<>><<>><<>><<>>

This database contains Near Infrared (NIR) spectroscopy and optical microscopy 
data on an assortment of fabric specimens used for applications including fiber 
content classification, systems and software development, and systems and 
process validation of textile feedstock identification systems.

The fabric sample library includes 113 fabrics total: 70 known provenance 
fabrics with known fiber content and various dyes/finishes, 20 known provenance 
fabrics with undyed, blended fiber content, 11 post-consumer fabrics with 
various fiber contents, dyes, and finishes, and 12 pre-consumer fabrics with 
various fiber contents, dyes, and finishes.

Each fabric was measured via NIR spectroscopy with nominally seven replicates 
on a benchtop instrument from 833 nm to 2500 nm and two handheld instruments 
from 1550 nm to 1950 nm. Optical microscopy images for these fabrics were 
collected on a benchtop, stereo-ocular inspection microscope with mono, color, 
or polarized cameras.

The data repository includes directories for: benchtop NIR spectral data, 
handheld NIR spectral data, and fabric-scale microscopy images.

For more information, please see the readme and data documentation in each 
sub-directory. A complete manuscript describing data collection, analysis, 
and database documentation is forthcoming. Spectroscopy data consists of about 
193 MB from ca. 4248 files. Microscopy data consists of about 10.6 GB from 
ca. 1044 files. Specimen files are .zipped at the Source directory level to 
reduce large number of files.

File Formats: .csv, .xlsx, .txt, .pdf, .bmp, .tiff, .py, .sh


<<>><<>><<>><<>><<>><<>><<>>| General Information |<<>><<>><<>><<>><<>><<>><<>>

Version 1.0 data was collected: February 2024 to July 2024.
Version 2.0 data was collected: August 2024 to December 2025.

Location of data collection: 
      National Institute of Standards and Technology
      Materials Measurement Science Division, Material Measurement Laboratory
      100 Bureau Drive, Bldg. 220, Gaithersburg, MD 20899

Funding sources: 
Verion 1.0 data was collected while Katarina E. Goodge was a 
NRC-funded post-doc and Charlotte M. Wentz was a University of Maryland PREP-
postdoc then a NRC-funded post-doc. Charlotte M. Wentz would like to 
acknowledge funding through NIST Award # 70NANB8H165. Zois Tsinas would like to 
acknowledge funding through NIST Award # 70NANB22H140. 
Version 2.0 data was collected while Katarina E. Goodge was a NRC-funded 
post-doc then a Georgetown University PREP-postdoc and Radha V. Patel was a 
Georgetown University PREP graduate researcher. Katarina E. Goodge and Radha V. 
Patel would like to acknowledge funding through NIST Aware # 70NANB23H023. 


<<>><<>><<>><<>><<>><<>><<>><<| Data Use Notes |>><<>><<>><<>><<>><<>><<>><<>>>

This data is publicly available according to the NIST statements of
copyright, fair use and licensing; see
https://www.nist.gov/director/copyright-fair-use-and-licensing-statements-srd-
data-and-software

Please cite the use of this data as follows:
K.E. Goodge, C.J. Vederman, R.V. Patel, C.M. Wentz, Z. Tsinas, A.K. Landauer, 
A.L.  Forster (2024) "Near Infrared Spectra of Origin-defined and Real-world 
Textiles (NIR-SORT): A spectroscopic and materials characterization dataset for 
known provenance and post-consumer fabrics", National Institute of Standards 
and Technology, Version 2.0.0, https://doi.org/10.18434/mds2-3325. 
(Accessed: [insert date])


<<<>><<>><<>><<>><<>><<>><<>><<>>| References |<<>><<>><<>><<>><<>><<>><<>><<>>

N/A (to be added)


<<<>><<>><<>><<>><<>><<>><<>><<| Data Overview |>><<>><<>><<>><<>><<>><<>><<>>>

File structure: data are stored in directories for each experiment type, and 
                subdirectories for each material. The main folder has a text 
                file describing naming conventions, data framework, sample 
                metadata and other notes.

Additional related data collected that was not included in the current 
data package:
      Certain method development and validation data are not included in the 
      final data package included here. Benchtop NIR data does not include, 
      for example, internal reference spectra or interferograms, beam 
      alignment, or raw temperature and relative humidity data. 


<<>><<>><<>><<>><<>><<>><<>><<| Version History |>><<>><<>><<>><<>><<>><<>><<>>

  this version (2.0.0): 2026-01-
  initial release (1.0.0): 2024-09-25


<<>><<>><<>><<>><<>><<>>| Methodological Information |<<>><<>><<>><<>><<>><<>>>

Materials
  1. Origin-defined (known provenance)
     All Source A and Source B were acquired from Testfabrics, inc. 
     (West Pittston, PA, USA). 
     Fabric specifications such as fiber content, fabric structure, dye type, 
     finishes, manufacturer's product identification code, and manufacturer's 
     lot identification code can be found in SampleInformation.csv. 

  2. Real-world (pre- or post-consumer)
     Source C was acquired from a local secondhand store, and Source D was 
     acquired as production samples from a research partner. Fabric 
     specifications such as fiber content and fabric structure can be found in 
     SampleInformation.csv. Manufacturer information is unknown. 

Methods for data collection:
  1. Benchtop_N NIR Spectroscopy
     Instrument: Nicolet iS50 FTIR, Thermo Fisher Scientific Inc., 
                 Madison, WI, USA
        Sample compartment: Integrating Sphere
        Detector: Indium Gallium Arsenide (InGaAs)
        Internal reference: Diffuse Gold
        Crystal material: Sapphire

      Measurement parameters:
         Wavenumbers range, as collected (column 1): 
                                 3999.706 cm^-1 to 11999.12 cm^-1
                                      (step size 1.928 cm^-1)
         Wavelength range, converted: 833 nm to 2500 nm
     Resolution: 4.000 cm^-1
     Y-values: Absorbance and % Reflectance (column 2)
         Number of scans: 128
         Number of replicates: nominally 7
     
     Uncertainty: All intensity values are relative to the internal diffuse 
                  gold reference. For absolute values, refer to the Fluorilon 
                  99 % reflectance target (99W) from Avian Technologies LLC 
                  (New London, NH, USA) spectra. See 'README' tab in 
                  'UncertaintyPropagation_N.xlsx' in Benchtop_N\ for 
                  explanation and '99W Raw + Uncertainty' tab for raw, mean, 
                  and standard deviation measurement data and expected values 
                  for 99 % reflectance standard. For 99W, all coefficients of 
                  variation were less than one percent (< 1 %) of the mean 
                  reflectance.

     Sample Preparation and Measurement: 
         Each fabric specimen, approximate dimensions of 10 cm by 10 cm, was 
         folded such that a total of six layers of fabric were stacked and 
         positioned on the sampling window. However, similar reflectance counts 
         can be achieved with one layer of fabric by covering the specimen with 
         a backing material (see Data Descriptor publication for more details). 
         For size-limited specimens, i.e., those unable to create six layers to 
         cover the integrating sphere spot size, a cap lined with aluminum foil 
         was placed over the single layer specimen. These specimens are noted 
         in the README file in the Benchtop subdirectory.
         
         Each replicate was measured on nonoverlapping weft and warp yarns 
         such that each measurement is an independent sampling of the yarns, 
         i.e., no two measurements contain the same set of yarns. 

  2. Handheld_F NIR Spectroscopy
     Instrument: FabriTell, Matoha Instrumentation Ltd., London, U.K.
         Sensor: Diffuse reflectance NIR
         External white reference: aluminum calibration target 
                                   included with device
     Measurement parameters:
         Wavelength range, as collected: 1550.0 nm to 1950.0 nm 
                                         (step size approx. 3.15 nm) 
         Wavenumber range, converted (column 1): 6450 cm^-1 to 5130 cm^-1
     Resolution: unknown
     Y-values: Calculated Absorbance and Reflectance counts (column 2)
         Number of scans: unknown
         Number of replicates: nominally 7
     
     Uncertainty: See 'README' tab in 'UncertaintyPropagation_F.xlsx' in 
                  Handheld_F\ for explanation and 'Estimation of 
                  Uncertainty' tab for uncertainty calculation for an example 
                  spectrum.
     
     Sample Preparation and Measurement: 
         Each fabric specimen, approximate dimensions of 10 cm by 10 cm, was 
         folded such that a total of six layers of fabric were stacked and 
         positioned on the sampling window. However, similar reflectance counts 
         can be achieved with one layer of fabric by covering the specimen with 
         a backing material (see Data Descriptor publication for more details). 
         For size-limited specimens, i.e., those unable to create six layers to 
         cover the handheld spot size, a cap lined with aluminum foil was 
         placed over the single layer specimen. These specimens are noted in 
         the README file in the Handheld subdirectory.
         
         Each replicate was measured on nonoverlapping weft and warp yarns 
         such that each measurement is an independent sampling of the yarns, 
         i.e., no two measurements contain the same set of yarns.

  3. Handheld_S NIR Spectroscopy
     Instrument: Sortile, New York, USA
         Sensor: MEMS Fabry-Perot Interferometer
         External white reference: Fluorilon gray scale standards, 
                 99 % reflectance (Avian Technologies LLC, New London, NH, USA)
     Measurement parameters:
         Wavelength range, as collected: 1550.0 nm to 1950.0 nm 
                                         (step size approx. 3.2 nm) 
         Wavenumber range, converted (column 1): 6450 cm^-1 to 5130 cm^-1
     Resolution: 15 nm - 21 nm
     Y-values: Calculated Absorbance and Reflectance counts (column 2)
         Number of scans: 30
         Number of replicates: nominally 7
     
     Uncertainty: See 'README' tab in 'UncertaintyPropagation_S.xlsx' in 
                  Handheld_S\ for explanation and 'Estimation of 
                  Uncertainty' tab for uncertainty calculation for an example 
                  spectrum.
     
     Sample Preparation and Measurement: 
         Each fabric specimen, approximate dimensions of 10 cm by 10 cm, was 
         folded such that a total of six layers of fabric were stacked and 
         positioned on the sampling window. However, similar reflectance counts 
         can be achieved with one layer of fabric by covering the specimen with 
         a backing material (see Data Descriptor publication for more details). 
         For size-limited specimens, i.e., those unable to create six layers to 
         cover the handheld spot size, a cap lined with aluminum foil was 
         placed over the single layer specimen. These specimens are noted in 
         the README file in the Handheld subdirectory.
         
         Each replicate was measured on nonoverlapping weft and warp yarns 
         such that each measurement is an independent sampling of the yarns, 
         i.e., no two measurements contain the same set of yarns. 

  4. Optical Microscopy
     Instrument: Stereo-ocular inspection microscope [unknown manufacturer]
     Imaging software application: Spinnaker SDK (Windows)
     Viewer application for Spinnaker Library: SpinView 4.0.0.116 (Windows)
         Color Camera: FLIR BlackFly S Mono, 1/1.8" CMOS, CS-Mount
            Model: BFS-U3-50S4C-CS
            Megapixels: 5 MP 
            Frame Rate: 72 FPS
            Sensor: Sony IMX547
            Spectrum: Color
            Optical filter: IR-Cut Off (670 nm)
            Image bit depth: 32 bit RGB-alpha
            Image resolution: 2 448 pixels by 2 048 pixels
            Pixel size: 2.74

         Mono Camera: FLIR BlackFly S, 1" CMOS, C-Mount
            Model: BFS-U3-89S6M-C
            Megapixels: 8.9 MP 
            Frame Rate: 42 FPS
            Sensor: Sony IMX255
            Spectrum: Mono
            Optical filter: None
            Image bit depth: 8 bit grayscale
            Image resolution: 4 096 pixels by 2 160 pixels
            Pixel size: 3.45

         Polarized Camera: FLIR BlackFly S Polarized-Mono, 2/3" CMOS, C-Mount
            Model: BFS-U3-51S5PC-C
            Megapixels: 5 MP 
            Frame Rate: 75 FPS
            Sensor: Sony IMX250MZR
            Spectrum: Polarized
            Optical filter: None
            Image bit depth: 32 bit RBG-alpha
            Image resolution: 2 448 pixels by 2 048 pixels
            Pixel size: 3.45

     See README files in respective subdirectories for image scales.

     Sample Preparation and Measurement: 
         Each fabric specimen was laid flat, centered under the objective lens, 
         and held in place by stage clips. See ImageParameters.csv in /Color 
         for details on image settings and measurement. 

  4. Data processing
     Example utility scripts are provided for the following tasks:
     1. Data Grab [data_collection_from_folders]
     2. Convert wavenumber to wavelength and write to new file 
        [data_collection_from_folders[.py, .sh]]
     3. Plot spectra based on filename values 
        [example_benchtop_data_visulaization.py]
     4. Plot interpolated Benchtop spectra to compare to Handheld 
        spectra [example_benchtop_to_handheld_comparison.py]
     5. Plot spectra based on metadata values [example_color_comparison.py]

  5. Standards and calibration information, if appropriate:
     Instruments were calibrated according to respective schedules and 
     manufacturer specifications. 

  6. Environmental/experimental conditions
     All fabrics were conditioned and all experiments were conducted under 
     ambient lab conditions. For Benchtop data collection, temperature was in 
     the approximate range [23, 26] degrees C, and relative humidity was in 
     the approximate range [14, 42] % humidity. For Handheld data collection, 
     temperature was in the approximate range [18, 26] degrees C, and relative 
     humidity was in the approximate range [38, 60] % humidity. See 
     date-specific test conditions files in the corresponding folders 
     (e.g., TestConditions_N.xlsx in Benchtop_N\).

  7. People involved with sample collection, processing, analysis, and/or 
     submission:
  
     Katarina E Goodge: project conceptualization; sample selection, 
                        acquisition, and preparation; experimental design; data 
                        collection; uncertainty estimation; code review;
                        dataset preparation and documentation.
     Cecelia  J Vederman: sample preparation; data collection
     Radha V Patel: sample preparation; data collection
     Charlotte M Wentz: project conceptualization; sample selection, 
                        acquisition, and preparation; preliminary data 
                        collection; experimental design 
     Zois Tsinas: project conceptualization; experimental setup; data 
                  interpretation; code review 
     Alexander K Landauer: uncertainty estimation; data processing scripts; 
                           dataset framework design and preparation
     Amanda L Forster: project conceptualization; sample selection, 
                       acquisition, and preparation; experimental design; 
                       dataset framework design and preparation

  8. Acknowledgements
     The authors wish to thank:
     Kate Beers for her work founding the NIST Circular Economy program, 
          supporting the CE Textiles team, and helpful discussion surrounding 
          this project. Kelsea Schumacher for all of her assistance in engaging 
          with stakeholders and identifying the needs that led to this dataset, 
          and Michelle Seitz for her continued support of this work. 
     Brayden Czapla and Heather Patrick for their insightful discussion on 
          spectroscopy, and specifically to Brayden for lending his 99W 
          reflectance sample for use as the external reference in this dataset.
     Bradley Sutliff and Constanza Gomez for their helpful discussions in how
          to prepare this dataset to be ready to be used in machine learning 
          algorithms. 


<<<>><<>><<>><<>><<>><<>><<>>| Disclaimers |>><<>><<>><<>><<>><<>><<>><<>><<>>>

Certain commercial equipment, instruments, or materials are identified in this
dataset in order to specify the experimental procedure adequately.  Such 
identification is not intended to imply recommendation or endorsement by 
NIST, nor is it intended to imply that the materials or equipment identified 
are necessarily the best available for the purpose.

The opinions, recommendations, findings, and conclusions in the dataset 
do not necessarily reflect the views or policies of NIST or the United 
States Government.


This readme.txt file was originally prepared by Katarina E Goodge on 
July 17, 2024 and updated for Version 2.0.0 on January 16, 2026.

===============================================================================