from SentinelTime.mask_stack import *
from SentinelTime.time_series import *
from SentinelTime.weather_data import *
from SentinelTime.fern_analysis.analysis_and_plots import *
from SentinelTime.relative_orbit_calculation import *


def main():
    ###################################     INPUT    ########################################
    # Main directory of original raster files and/or subdirectories containing the original raster files:
    main_dir = "G:/Processed/original_data/"

    # Location of Shapefile to mask the ROI (must be polygon shapefile, simple polygon shapes are faster!):
    # shape_path = "G:/Shapes/Polygons/new_extent.shp"
    shape_path = "G:/FuerMarlin_BoFEuFarnkraut/extent/fern_extent.shp"

    # Location of the point shapefile to extract data from time series with (must be point shapefile!):
    # point_path = "G:/Shapes/Points"
    point_path = "G:/FuerMarlin_BoFEuFarnkraut"
    # point_path = "G:/Shapes/Points/clc312_close_to_stations"

    csv_folder = "G:/Processed/results/CSV/"
    # csv_folder = "G:/Processed/results/AAA_Weather_Stations_2016-2019/CSV/"

    fig_folder = "G:/Processed/results/Figures/"
    if not os.path.exists(fig_folder):
        os.mkdir(fig_folder)

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
    #     extract_time_series(results_dir=results_dir, shapefile=shapefile, buffer_size=20, point_path=point_path)

    # Extract temporal statistics from time series with possibility to plot Mean and Std.Dev. values of time series for
    # each class:
    # temporal_statistics(path_to_csv_folder=csv_folder, results_dir=results_dir, fig_folder=fig_folder, plot_bool=True,
    #                     frost_bool=False)

    # dataframe_difference_calc(path_to_csv_folder=csv_folder, results_dir=results_dir, fig_folder=fig_folder,
    #                           plot_bool=True, frost_bool=False)

    boxplots(path_to_csv_folder=csv_folder, results_dir=results_dir, fig_folder=fig_folder, plot_bool=False,
             season=["Spring", "Summer", "Autumn", "Winter"], frost_bool=False, input_data="diff")

    # import_weather_for_fern(radar_df="")

    # Calculate VH/VV Ratio for each class and flight direction:
    # ratio_calc(path_to_folder=results_dir, plot_bool=True, frost_bool=False)

    # clean_weather_df(path_to_weather_folder=weather_data, path_to_csv_folder=csv_folder,
    #                  station_heights=station_heights)

    # eliminate_nanoverlap(main_dir=main_dir, shape_path=shape_path)

    # TEST!!!!!!!!!!!!!!!!!!
    # calculate_relative_orbit_S1(absolute_orbit_number=36115, S1_satellite="A")
    # calculate_relative_orbit_S1(absolute_orbit_number=36166, S1_satellite="A")
    # calculate_relative_orbit_S1(absolute_orbit_number=25168, S1_satellite="B")


if __name__ == '__main__':
    main()
