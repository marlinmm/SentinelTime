# SentinelTime

#### Tool creating raster time series stacks from S-1 GRD scenes 

This tool allows the user to specify a folder as well as subfolders containing lots of preprocessed Sentinel-1 GRD files
and a shapefile as Region of Interest (ROI). The tool checks, if the files are contained within the ROI and clips all
overlapping raster data to the extents of the ROI. A raster time series stack is created with the clipped files. 

Furthermore, the user can specify Points of Interest (POI) using a point shapefile to extract time series information 
for this POI and also specify a buffer size to include more pixels around the POI (Note: the buffer size corresponds to
the length of the square buffer around the point). The time series information can be exported to csv files

This tools also allows for calculation of multitemporal statistics of the exported time series as well as creating plots 

Basic functionality includes:
* Checking if raster data overlap with ROI
* Creating raster time series stacks using ROIs
* Extracting time series data from stack and exporting as csv
* Basic statistical analysis 

# Installation
In case you have git installed you can install the package as follows:

    pip install git+https://github.com/marlinmm/SentinelTime.git

If you have trouble installing _rasterio_, _fiona_ or the needed _GDAL_ package on Windows, download and install the 
.whl files directly from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/).

_Developed in Python 3.8_

# TODO:
* ~~point shapefile import as a list~~
* RVI oder VH/VV ratio
* boxplots
