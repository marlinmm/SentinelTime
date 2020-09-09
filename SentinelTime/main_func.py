from SentinelTime.mask_stack import *
from SentinelTime.time_series import *


def main():
    # Main directory of original raster files:
    main_dir = "G:/Processed/original_data/"

    # Create results folder outside of main_dir:
    results_dir = "G:/Processed/results/"

    # Location of Shapefile to mask the ROI:
    shape_path = "G:/Shapes/Polygons/extend_of_points.shp"

    # Location of the point shapefile to extract data from timeseries with:
    point_path = "G:/Shapes/Points/clc312_reproj.shp"

    layer_stack = "G:/Processed/results/VH_Asc_stack.tif"

#####------ NOT NEEDED ------#####
    # eliminate_nanoverlap(sen_directory=sen_directory, shape_path=shape_path)
    # eliminate_nanoverlap(main_dir=main_dir, shape_path=shape_path)
    # mask_tif(shape_path=shape_path, main_dir=main_dir, results_dir=results_dir)
    # create_point_buffer(point_path=point_path, buffer_size=100)
    # tmp1, tmp2 = create_overlap_file_list(path_to_folder=main_dir, datatype=".tif")
#####------ NOT NEEDED ------#####

    # raster_stack(shape_path=shape_path, main_dir=main_dir, results_dir=results_dir)


    # extract_time_series(layer_stack=layer_stack, point_path=point_path, buffer_size=100, sen_directory=VH_asc)

    extract_time_series(results_dir=results_dir, point_path=point_path, buffer_size=100, export_bool=True)

    # plot_test(layer_stack=results_dir, point_path=point_path, buffer_size=100, sen_directory=VH_asc)
    # extract_dates(sen_directory=VH_asc)


if __name__ == '__main__':
    main()
