from SentinelTime.mask_stack import *
from SentinelTime.time_series import *
from SentinelTime.weather_data import *


def main():
    ###################################     INPUT    ########################################
    # Main directory of original raster files and/or subdirectories containing the original raster files:
    main_dir = "G:/Processed/original_data/"

    # Location of Shapefile to mask the ROI (must be polygon shapefile, simple polygon shapes are faster!):
    shape_path = "G:/Shapes/Polygons/new_extent.shp"

    # Location of the point shapefile to extract data from time series with (must be point shapefile!):
    point_path = "G:/Shapes/Points"

    csv_folder = "G:/Processed/results/CSV/"

    # Location of weatherdata in csv file format to calculate evapotranspiration:
    weather_data = "G:/Weather_data/"
    station_heights = [442, 228, 682, 421]

    ###################################     OUTPUT    ########################################
    # Create results folder outside of main_dir:
    results_dir = "G:/Processed/results/"

    ########################### USER-DEPENDENT FUNCTIONS TO BE USED ##########################
    # Creating a raster stack clipped to the extents of the specified shapefile:
    # raster_stack(shape_path=shape_path, main_dir=main_dir, results_dir=results_dir, overwrite=False)

    # Extract time series information based on point shapefiles and export information to csv file:
    # point_list = extract_files_to_list(path_to_folder=point_path, datatype=".shp", path_bool=True)
    # print(point_list)
    # for shapefile in point_list:
    #     extract_time_series(results_dir=results_dir, shapefile=shapefile, buffer_size=50, point_path=point_path)

    # Extract temporal statistics from time series with possibility to plot Mean and Std.Dev. values of time series for
    # each class:
    # temporal_statistics(path_to_csv_folder=csv_folder, results_dir=results_dir, plot_bool=True)

    # Calculate VH/VV Ratio for each class and flight direction:
    # ratio_calc(path_to_folder=results_dir, plot_bool=True)

    # clean_weather_df(path_to_weather_folder=weather_data, path_to_csv_folder=csv_folder,
    #                  station_heights=station_heights)

    eliminate_nanoverlap(main_dir=main_dir, shape_path=shape_path)


if __name__ == '__main__':
    main()
