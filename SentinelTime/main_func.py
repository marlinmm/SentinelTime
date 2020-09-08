from SentinelTime.mask_stack import *

def main():
    # sen_directory = "G:/Processed/processed_existing/VH"
    # sen_overlap_dir = "G:/Processed/processed_existing/VH_overlap/"

    sen_directory = "G:/Processed/processed_new_per_year/VH/"
    sen_overlap_dir = "G:/Processed/processed_new_per_year/VH_overlap/"

    VH_asc = "G:/Processed/preprocessd/VH_overlap/Asc/"
    VH_desc = "G:/Processed/preprocessd/VH_overlap/Desc/"

    shape_path = "G:/Shapes/Polygons/extend_of_points.shp"
    point_path = "G:/Shapes/Points/clc111_reproj.shp"

    layer_stack = "G:/Processed/preprocessd/VH_overlap/Asc/AAA_stack.tif"

    # eliminate_nanoverlap(sen_directory=sen_directory, shape_path=shape_path)
    # eliminate_nanoverlap(sen_directory=sen_overlap_dir, shape_path=shape_path)
    # mask_tif(shape_path=shape_path, sen_directory=VH_asc)
    # raster_stack(sen_directory=VH_asc)
    # create_point_buffer(point_path=point_path, buffer_size=100)
    # extract_time_series(layer_stack=layer_stack, point_path=point_path, buffer_size=100)
    extract_dates(sen_directory=VH_asc)

if __name__ == '__main__':
    main()
