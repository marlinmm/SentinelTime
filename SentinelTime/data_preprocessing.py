import os
import fiona
import rasterio as rio
import rasterio.mask
import numpy as np


def extract_files_to_list(path_to_folder, datatype, path_bool):
    """
    This functions checks a directory for all files of a certain dataype and returns a list of all found files
    :param path_to_folder: string
        Path to directory to be searched
    :param datatype: string
        Datatype of files to be searched
    :param path_bool: boolean
        append path to filename if set to TRUE, only filename if FALSE
    :return: list
        Contains paths to all files or all filenames in searched directory
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
    This function imports shapefile from given directory to python
    :param shape_path: string
        Path to shapefile
    :return: list
        Returns a list of all elements in shapefile
    """
    active_shapefile = fiona.open(shape_path, "r")
    for i in range(0, len(list(active_shapefile))):
        shapes = [feature["geometry"] for feature in active_shapefile]
    return shapes


def create_shape_buffer(shape_path, buffer_size):
    """
    This function creates a buffer around all vertex points of a given shapefile or polygon
    :param shape_path: string
        Path to the shapefile
    :param buffer_size: int
        Buffer size corresponds to the length of the square buffer around the vertex point
    :return: list
        Returns a list with buffered polygons around each vertex point of input polygon
    """
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
    This function is similar to create_shape_buffer but works for point shapefiles
    :param point_path: string
        Path to the shapefile
    :param buffer_size: int
        Buffer size corresponds to the length of the square buffer around the vertex point
    :return: list
        Returns a list with buffered polygons around each point of input polygon
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
    This function creates a list of all raster files which are fully contained within the given polygon
    :param main_dir: string
        Path to directory or subdirectories containing the input raster files
    :param shape_path: string
        Path to shapefile used to create the ROI
    :return: tuple
        Returns a tuple of 2 lists containing the overlapping filenames and corresponding paths
    """
    buffer_list = create_shape_buffer(shape_path=shape_path, buffer_size=100)
    file_list, path_list = create_overlap_file_list(path_to_folder=main_dir, datatype=".tif")
    print("Creating list of all overlapping files...")
    overlap_file_list = []
    overlap_path_list = []

    # Iterate through raster file list and import each file
    for i, files in enumerate(file_list):
        src1 = rio.open(path_list[i] + file_list[i])
        # Counter to check, if all vertex points of given shapefile contain values
        counter = 0

        # Check, if raster file is contained within given polygon:
        for j, polygons in enumerate(buffer_list):
            try:
                tmp = rio.mask.mask(src1, [buffer_list[j]], all_touched=0, crop=True, nodata=np.nan)
                if str(np.nanmean(tmp[0])) == "nan":
                    break
                # Increment counter by 1 if vertex point is covered by raster file
                counter += 1
            except ValueError:
                counter = 0
                pass
        src1.close()

        # If counter equals number of vertex points of shapefile, raster file is contained within polygon
        if counter == len(buffer_list):
            overlap_file_list.append(file_list[i])
            overlap_path_list.append(path_list[i])
    return overlap_file_list, overlap_path_list


def create_overlap_file_list(path_to_folder, datatype):
    """
    Similar function to extract_files_to_list, but also works for subdirectories
    :param path_to_folder: string
        Path to directory containing files or subdirectories of files
    :param datatype: string
        Datatype of files to be searched
    :return: tuple
        Returns tuple of lists containing paths to all files or all filenames in searched directory/directories
    """
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
