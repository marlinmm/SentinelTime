import rasterio.mask
import shutil
import rasterio.plot
from SentinelTime.data_preprocessing import *


def mask_tif(shape_path, sen_directory):
    """

    :param shape_path:
    :param sen_directory:
    :return:
    """
    file_list = extract_files_to_list(path_to_folder=sen_directory, datatype=".tif", path_bool=True)
    file_name_list = extract_files_to_list(path_to_folder=sen_directory, datatype=".tif", path_bool=False)
    shapes = import_polygons(shape_path=shape_path)
    masked_folder = sen_directory + "masked/"
    if os.path.exists(masked_folder):
        shutil.rmtree(masked_folder)
    os.mkdir(masked_folder)

    for i, files in enumerate(file_list):
        src1 = rio.open(file_list[i])
        out_image, out_transform = rio.mask.mask(src1, [shapes[0]], all_touched=0, crop=True, nodata=np.nan)
        out_meta = src1.meta
        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})
        with rasterio.open(
                masked_folder + file_name_list[i][0:len(file_name_list)-4] + "_masked.tif", "w", **out_meta) as dest:
            dest.write(out_image)


def raster_stack(sen_directory):
    """
    :param sen_directory:
    :return:
    """
    file_list = extract_files_to_list(path_to_folder=sen_directory + "masked/", datatype=".tif", path_bool=True)

    # Read metadata of first file
    with rasterio.open(file_list[0]) as src0:
        meta = src0.meta

    # Update meta to reflect the number of layers
    meta.update(count=len(file_list))

    # Read each layer and write it to stack
    with rasterio.open(sen_directory + 'AAA_stack.tif', 'w', **meta) as dst:
        for id, layer in enumerate(file_list, start=1):
            with rasterio.open(layer) as src1:
                dst.write_band(id, src1.read(1))


def extract_dates(sen_directory):
    """

    :param sen_directory:
    :return:
    """
    file_list = extract_files_to_list(path_to_folder=sen_directory + "masked/", datatype=".tif", path_bool=False)
    date_list = []
    for file in file_list:
        # date_list.append(str(file[2:6] + "-" + file[6:8] + "-" + file[8:10]))
        date_list.append(int(file[2:10]))
    return date_list


def extract_time_series(layer_stack, point_path, buffer_size, sen_directory, export_bool):
    """

    :param sen_directory:
    :param buffer_size:
    :param layer_stack:
    :param point_path:
    :return:
    """
    np.set_printoptions(suppress=True)
    patches = create_point_buffer(point_path, buffer_size=buffer_size)
    src1 = rio.open(layer_stack)
    patch_mean = []
    for patch in patches:
        pixel_mean = []
        out_image, out_transform = rio.mask.mask(src1, [patch], all_touched=0, crop=True, nodata=np.nan)
        for pixel in out_image:
            pixel_mean.append(np.nanmean(pixel))
        patch_mean.append(pixel_mean)
    patch_mean.append(extract_dates(sen_directory))
    patch_mean = np.rot90(patch_mean)
    patch_mean = np.rot90(patch_mean)
    patch_mean = np.rot90(patch_mean)
    patch_mean = patch_mean.tolist()
    for elem in patch_mean:
        elem[0] = int(elem[0])
    if export_bool:
        np.savetxt(sen_directory + "export/VH_Asc.csv", patch_mean, delimiter=",",
                   header="date,VH1,VH2,VH3,VH4,VH5,VH6,VH7,VH8,VH9,VH10,VH11,VH12,VH13,VH14,VH15,VH16,VH17,VH18,VH19,VH20",
                   fmt='%i,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f')
    return patch_mean


def plot_test(layer_stack, point_path, buffer_size, sen_directory):
    import matplotlib.pyplot as plt
    dataframe = extract_time_series(layer_stack=layer_stack, point_path=point_path, buffer_size=buffer_size,
                                    sen_directory=sen_directory, export_bool=False)
    time_mean = []
    dates = []
    for elem in dataframe:
        # print(elem)
        # print(len(elem))
        col_mean = np.mean(elem[1:len(elem)])
        time_mean.append(col_mean)
        dates.append(elem[0])
    plt.plot(time_mean)
    plt.show()


