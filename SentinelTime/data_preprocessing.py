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
    for i in range(0,len(list(active_shapefile))):
        shapes = [feature["geometry"] for feature in active_shapefile]
    return shapes


def create_shape_buffer(shape_path):
    import_list = import_polygons(shape_path=shape_path)

    buffer_list = []
    for i in range(0, len(import_list[0]["coordinates"][0])-1):
        lon = import_list[0]["coordinates"][0][i][0]
        lat = import_list[0]["coordinates"][0][i][1]
        upper_left = (lon - 100, lat + 100)
        upper_right = (lon + 100, lat + 100)
        lower_left = (lon - 100, lat - 100)
        lower_right = (lon + 100, lat - 100)
        buffer_coord = [[upper_left, upper_right, lower_right, lower_left, upper_left]]
        buffer = {"type": "Polygon", "coordinates": buffer_coord}
        buffer_list.append(buffer)
    return buffer_list


def create_point_buffer(point_path):
    """

    :param point_path:
    :return:
    """
    import_list = import_polygons(shape_path=point_path)

    buffer_list = []
    print(len(import_list))
    print(import_list)
    print(import_list[1]["coordinates"])
    for i in range(0, len(import_list)):
        lon = import_list[i]["coordinates"][0]
        lat = import_list[i]["coordinates"][1]
        print(lon)
        upper_left = (lon - 100, lat + 100)
        upper_right = (lon + 100, lat + 100)
        lower_left = (lon - 100, lat - 100)
        lower_right = (lon + 100, lat - 100)
        buffer_coord = [[upper_left, upper_right, lower_right, lower_left, upper_left]]
        buffer = {"type": "Polygon", "coordinates": buffer_coord}
        buffer_list.append(buffer)
    print(buffer_list)
    return buffer_list


def eliminate_nanoverlap(sen_directory, shape_path):
    """

    :param sen_directory:
    :param shape_path:
    :return:
    """
    buffer_list = create_shape_buffer(shape_path=shape_path)
    file_list = extract_files_to_list(path_to_folder=sen_directory, datatype=".tif", path_bool=False)

    for i, files in enumerate(file_list):
        src1 = rio.open(sen_directory + file_list[i])
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
            # os.rename(sen_directory + file_list[i], sen_directory + file_list[i][0:len(file_list[i])-4] + "_overlap.tif")
            # os.rename(sen_directory + file_list[i], sen_directory + file_list[i][0:len(file_list[i]) - 12] + ".tif")
            print(file_list[i])
            # os.rename(sen_directory + file_list[i], sen_directory + file_list[i][10:len(file_list[i])])
