from SentinelTime.data_preprocessing import *
from SentinelTime.mask_stack import *
import rasterio.mask


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
