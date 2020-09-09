from SentinelTime.data_preprocessing import *
from SentinelTime.mask_stack import *
import rasterio.mask


def extract_dates(directory):
    """

    :param sen_directory:
    :return:
    """
    file_list = extract_files_to_list(path_to_folder=directory, datatype=".tif", path_bool=False)
    date_list = []
    for file in file_list:
        # date_list.append(str(file[2:6] + "-" + file[6:8] + "-" + file[8:10]))
        date_list.append(int(file[2:10]))
    return date_list


def extract_time_series(results_dir, point_path, buffer_size, export_bool):
    """

    :param results_dir:
    :param point_path:
    :param buffer_size:
    :param export_bool:
    :return:
    """
    np.set_printoptions(suppress=True)
    patches = create_point_buffer(point_path, buffer_size=buffer_size)
    layer_stacks = extract_files_to_list(path_to_folder=results_dir, datatype=".tif", path_bool=True)
    print(layer_stacks)

    for file in layer_stacks:
        src1 = rio.open(file)
        patch_mean = []
        for patch in patches:
            pixel_mean = []
            out_image, out_transform = rio.mask.mask(src1, [patch], all_touched=0, crop=True, nodata=np.nan)
            # print(np.shape(out_image))
            for pixel in out_image:
                pixel_mean.append(np.nanmean(pixel))
            # print(pixel_mean)
            patch_mean.append(pixel_mean)
        if "VH" in file and "Asc" in file:
            patch_mean.append(extract_dates(results_dir + "VH" + "/" + "Asc" + "/"))
        if "VH" in file and "Desc" in file:
            patch_mean.append(extract_dates(results_dir + "VH" + "/" + "Desc" + "/"))
        if "VV" in file and "Asc" in file:
            patch_mean.append(extract_dates(results_dir + "VV" + "/" + "Asc" + "/"))
        if "VV" in file and "Desc" in file:
            patch_mean.append(extract_dates(results_dir + "VV" + "/" + "Desc" + "/"))
        patch_mean = np.rot90(patch_mean)
        patch_mean = np.rot90(patch_mean)
        patch_mean = np.rot90(patch_mean)
        patch_mean = patch_mean.tolist()
        for elem in patch_mean:
            elem[0] = int(elem[0])
        src1.close()
        if export_bool:
            if "VH" in file and "Asc" in file:
                np.savetxt(results_dir + point_path[point_path.index("clc"):point_path.index("clc")+6] + "_VH_Asc.csv", patch_mean, delimiter=",",
                           header="date,VH1,VH2,VH3,VH4,VH5,VH6,VH7,VH8,VH9,VH10,VH11,VH12,VH13,VH14,VH15,VH16,VH17,VH18,VH19,VH20",
                           fmt='%i,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f')
            if "VH" in file and "Desc" in file:
                np.savetxt(results_dir + point_path[point_path.index("clc"):point_path.index("clc")+6] + "_VH_Desc.csv", patch_mean, delimiter=",",
                           header="date,VH1,VH2,VH3,VH4,VH5,VH6,VH7,VH8,VH9,VH10,VH11,VH12,VH13,VH14,VH15,VH16,VH17,VH18,VH19,VH20",
                           fmt='%i,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f')
            if "VV" in file and "Asc" in file:
                np.savetxt(results_dir + point_path[point_path.index("clc"):point_path.index("clc")+6] + "_VV_Asc.csv", patch_mean, delimiter=",",
                           header="date,VV1,VV2,VV3,VV4,VV5,VV6,VV7,VV8,VV9,VV10,VV11,VV12,VV13,VV14,VV15,VV16,VV17,VV18,VV19,VV20",
                           fmt='%i,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f')
            if "VV" in file and "Desc" in file:
                np.savetxt(results_dir + point_path[point_path.index("clc"):point_path.index("clc")+6] + "_VV_Desc.csv", patch_mean, delimiter=",",
                           header="date,VV1,VV2,VV3,VV4,VV5,VV6,VV7,VV8,VV9,VV10,VV11,VV12,VV13,VV14,VV15,VV16,VV17,VV18,VV19,VV20",
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
