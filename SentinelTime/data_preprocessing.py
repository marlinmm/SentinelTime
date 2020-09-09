import os
import fiona
import rasterio as rio
import rasterio.mask
import numpy as np


def extract_files_to_list(path_to_folder, datatype, path_bool):
    """
    """
    new_list = []
    for filename in os.listdir(path_to_folder):
        if filename.endswith(datatype):
            if path_bool:
                new_list.append(os.path.join(path_to_folder, filename))
            else:
                new_list.append(filename)
        else:
            continue
    return new_list


def import_polygons(shape_path):
    """
    """
    active_shapefile = fiona.open(shape_path, "r")
    for i in range(0, len(list(active_shapefile))):
        shapes = [feature["geometry"] for feature in active_shapefile]
    return shapes


def create_shape_buffer(shape_path, buffer_size):
    import_list = import_polygons(shape_path=shape_path)
    buffer_size = buffer_size / 2
    buffer_list = []
    for i in range(0, len(import_list[0]["coordinates"][0]) - 1):
        lon = import_list[0]["coordinates"][0][i][0]
        lat = import_list[0]["coordinates"][0][i][1]
        upper_left = (lon - buffer_size, lat + buffer_size)
        upper_right = (lon + buffer_size, lat + buffer_size)
        lower_left = (lon - buffer_size, lat - buffer_size)
        lower_right = (lon + buffer_size, lat - buffer_size)
        buffer_coord = [[upper_left, upper_right, lower_right, lower_left, upper_left]]
        buffer = {"type": "Polygon", "coordinates": buffer_coord}
        buffer_list.append(buffer)
    return buffer_list


def create_point_buffer(point_path, buffer_size):
    """

    :param point_path:
    :param buffer_size:
    :return:
    """
    import_list = import_polygons(shape_path=point_path)
    buffer_size = buffer_size / 2
    buffer_list = []
    for i in range(0, len(import_list)):
        lon = import_list[i]["coordinates"][0]
        lat = import_list[i]["coordinates"][1]
        upper_left = (lon - buffer_size, lat + buffer_size)
        upper_right = (lon + buffer_size, lat + buffer_size)
        lower_left = (lon - buffer_size, lat - buffer_size)
        lower_right = (lon + buffer_size, lat - buffer_size)
        buffer_coord = [[upper_left, upper_right, lower_right, lower_left, upper_left]]
        buffer = {"type": "Polygon", "coordinates": buffer_coord}
        buffer_list.append(buffer)
    return buffer_list


def eliminate_nanoverlap(main_dir, shape_path):
    """

    :param sen_directory:
    :param shape_path:
    :return:
    """
    buffer_list = create_shape_buffer(shape_path=shape_path, buffer_size=100)
    file_list, path_list = create_overlap_file_list(path_to_folder=main_dir, datatype=".tif")
    print("Creating list of all overlapping files...")
    overlap_file_list = []
    overlap_path_list = []

    for i, files in enumerate(file_list):
        src1 = rio.open(path_list[i] + file_list[i])
        test_bool = 0
        for j, polygons in enumerate(buffer_list):
            try:
                tmp = rio.mask.mask(src1, [buffer_list[j]], all_touched=0, crop=True, nodata=np.nan)
                if str(np.nanmean(tmp[0])) == "nan":
                    break
                test_bool += 1
            except ValueError:
                test_bool = 0
                pass
        src1.close()
        if test_bool == 4:
            overlap_file_list.append(file_list[i])
            overlap_path_list.append(path_list[i])
    return overlap_file_list, overlap_path_list


def create_overlap_file_list(path_to_folder, datatype):
    file_list = []
    path_list = []
    for filename in os.listdir(path_to_folder):
        full_path = os.path.join(path_to_folder, filename)
        if filename.endswith(datatype):
            file_list.append(filename)
            path_list.append(full_path[0:full_path.index("S1") - 1] + "/")
        if os.path.isdir(full_path):
            tmp1, tmp2 = create_overlap_file_list(full_path, datatype)
            file_list = file_list + tmp1
            path_list = path_list + tmp2
    return file_list, path_list
