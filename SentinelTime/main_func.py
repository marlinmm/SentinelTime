from SentinelTime.mask_stack import *
from SentinelTime.time_series import *


def main():
    ###################################     INPUT    ########################################
    # Main directory of original raster files and/or subdirectories containing the original raster files:
    main_dir = "G:/Processed/original_data/"

    # Location of Shapefile to mask the ROI (must be polygon shapefile, simple polygon shapes are faster!):
    shape_path = "G:/Shapes/Polygons/extend_of_points.shp"

    # Location of the point shapefile to extract data from timeseries with (must be point shapefile!):
    point_path = "G:/Shapes/Points/"

    ###################################     OUTPUT    ########################################
    # Create results folder outside of main_dir:
    results_dir = "G:/Processed/results/"

    ########################### USER-DEPENDENT FUNCTIONS TO BE USED ##########################
    # Creating a raster stack clipped to the extents of the specified shapefile:
    raster_stack(shape_path=shape_path, main_dir=main_dir, results_dir=results_dir, overwrite=False)

    # Extract time series information based on point shapefiles and export information to csv file:
    point_list = extract_files_to_list(path_to_folder=point_path, datatype=".shp", path_bool=True)
    for shapefile in point_list:
        extract_time_series(results_dir=results_dir, point_path=shapefile, buffer_size=100)

    # Extract temporal statistics from time series with possibility to plot Mean and Std.Dev. values of time series for
    # each class:
    temporal_statistics(path_to_folder=results_dir, plot_bool=True)


if __name__ == '__main__':
    main()
