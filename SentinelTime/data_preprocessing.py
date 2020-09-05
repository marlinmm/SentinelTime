import os
import fiona
import rasterio as rio
import rasterio.mask
import numpy as np


def extract_files_to_list(path_to_folder, datatype):
    """
    finds all .tif-files in the corresponding directory
    :return:
    """
    new_list = []
    for filename in os.listdir(path_to_folder):
        if filename.endswith(datatype):
            new_list.append(os.path.join(path_to_folder, filename))
        else:
            continue
    return new_list


def import_polygons(shape_path):
    """
    imports the 3x3km polygons of the DWD weather stations
    :return:
    """
    active_shapefile = fiona.open(shape_path, "r")
    for i in range(0,len(list(active_shapefile))):
        shapes = [feature["geometry"] for feature in active_shapefile]
    return shapes


def eliminate_nanoverlap(sen_directory, shape_path):
    """
    eliminates the scenes which would'nt match with all weather stations
    :return:
    """
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

    file_list = extract_files_to_list(path_to_folder=sen_directory, datatype=".tif")

    for i, files in enumerate(file_list):
        src1 = rio.open(file_list[i])
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
            os.rename(file_list[i], file_list[i][0:len(file_list[i])-4] + "_overlap.tif")
            # os.rename(file_list[i], file_list[i][0:len(file_list[i]) - 12] + ".tif")
