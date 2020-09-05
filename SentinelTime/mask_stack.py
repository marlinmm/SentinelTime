import fiona
import rasterio as rio
import rasterio.mask
import numpy as np
import shutil
import rasterio.plot
from SentinelTime.data_preprocessing import *

def mask_tif(shape_path, sen_directory):
    file_list = extract_files_to_list(path_to_folder=sen_directory, datatype=".tif", path_bool=True)
    file_name_list = extract_files_to_list(path_to_folder=sen_directory, datatype=".tif", path_bool=False)
    shapes = import_polygons(shape_path=shape_path)
    print(file_list)
    print(shapes)

    masked_folder = sen_directory + "masked/"
    if os.path.exists(masked_folder):
        shutil.rmtree(masked_folder)
    os.mkdir(masked_folder)

    for i, files in enumerate(file_list):
        src1 = rio.open(file_list[i])
        out_image, out_transform = rio.mask.mask(src1, [shapes[0]], all_touched=0, crop=True, nodata=np.nan)
        # print(np.shape(src1))
        # print(np.shape(out_image))
        out_meta = src1.meta
        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})

        with rasterio.open(
                masked_folder + file_name_list[i][0:len(file_name_list)-4] + "_masked.tif", "w", **out_meta) as dest:
            dest.write(out_image)


def raster_stack(sen_directory):
    file_list = extract_files_to_list(path_to_folder=sen_directory + "masked/", datatype=".tif", path_bool=True)

    # Read metadata of first file
    with rasterio.open(file_list[0]) as src0:
        meta = src0.meta

    # Update meta to reflect the number of layers
    meta.update(count=len(file_list))

    # Read each layer and write it to stack
    with rasterio.open(sen_directory + 'masked/stack.tif', 'w', **meta) as dst:
        for id, layer in enumerate(file_list, start=1):
            with rasterio.open(layer) as src1:
                dst.write_band(id, src1.read(1))