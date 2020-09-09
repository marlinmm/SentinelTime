import rasterio.mask
import shutil
import rasterio.plot
from SentinelTime.data_preprocessing import *


def mask_tif(shape_path, main_dir, results_dir):
    """

    :param shape_path:
    :param sen_directory:
    :return:
    """
    file_name_list, path_list = eliminate_nanoverlap(main_dir, shape_path)
    shapes = import_polygons(shape_path)

    print("Cliping overlapping files to ROI...")

    VH_folder = results_dir + "VH/"
    VH_Asc_folder = VH_folder + "Asc/"
    VH_Desc_folder = VH_folder + "Desc/"
    if not os.path.exists(VH_folder):
        os.mkdir(VH_folder)
        os.mkdir(VH_Asc_folder)
        os.mkdir(VH_Desc_folder)

    VV_folder = results_dir + "VV/"
    VV_Asc_folder = VV_folder + "Asc/"
    VV_Desc_folder = VV_folder + "Desc/"
    if not os.path.exists(VV_folder):
        os.mkdir(VV_folder)
        os.mkdir(VV_Asc_folder)
        os.mkdir(VV_Desc_folder)

    for i, files in enumerate(file_name_list):
        file_name = path_list[i] + file_name_list[i]
        src1 = rio.open(file_name)
        out_image, out_transform = rio.mask.mask(src1, [shapes[0]], all_touched=0, crop=True, nodata=np.nan)
        out_meta = src1.meta
        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})

        flight_dir = file_name_list[i][file_name_list[i].index("___") + 3:file_name_list[i].index("___") + 4]
        polarization = file_name_list[i][file_name_list[i].index("grd") - 3:file_name_list[i].index("grd") - 1]
        if polarization == "VH":
            if flight_dir == "A":
                with rasterio.open(
                        VH_Asc_folder + file_name_list[i][10:len(file_name_list[i])], "w", **out_meta) as dest:
                    dest.write(out_image)
            if flight_dir == "D":
                with rasterio.open(
                        VH_Desc_folder + file_name_list[i][10:len(file_name_list[i])], "w", **out_meta) as dest:
                    dest.write(out_image)
        if polarization == "VV":
            if flight_dir == "A":
                with rasterio.open(
                        VV_Asc_folder + file_name_list[i][10:len(file_name_list[i])], "w", **out_meta) as dest:
                    dest.write(out_image)
            if flight_dir == "D":
                with rasterio.open(
                        VV_Desc_folder + file_name_list[i][10:len(file_name_list[i])], "w", **out_meta) as dest:
                    dest.write(out_image)
    return [VH_Asc_folder, VH_Desc_folder, VV_Asc_folder, VV_Desc_folder]


def raster_stack(shape_path, main_dir, results_dir):
    """
    :param sen_directory:
    :return:
    """
    result_folder = mask_tif(shape_path, main_dir, results_dir)
    print("Creating time series stack...")

    for folder in result_folder:
        file_list = extract_files_to_list(path_to_folder=folder, datatype=".tif", path_bool=True)

        # Read metadata of first file
        with rasterio.open(file_list[0]) as src0:
            meta = src0.meta

        # Update meta to reflect the number of layers
        meta.update(count=len(file_list))

        # Read each layer and write it to stack
        with rasterio.open(folder + '_AAA_stack.tif', 'w', **meta) as dst:
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
