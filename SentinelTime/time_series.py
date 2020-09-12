from SentinelTime.data_preprocessing import *
from SentinelTime.mask_stack import *
import rasterio.mask


def extract_dates(directory):
    """
    Extracts dates from list of preprocessed S-1 GRD files (need to be in standard pyroSAR exported naming scheme!)
    :param directory: string
        Path to folder, where files are stored
    :return: list
        returns list of acquisition dates of S-1 GRD files
    """
    file_list = extract_files_to_list(path_to_folder=directory, datatype=".tif", path_bool=False)
    date_list = []
    for file in file_list:
        date_list.append(int(file[2:10]))
    return date_list


def extract_time_series(results_dir, point_path, buffer_size):
    """
    Extracts time series information from patches of pixels using points and a buffer size to specify the size of the
    patch
    :param results_dir: string
        Path to results directory, where layerstacks are stored and csv files will be stored
    :param point_path: string
        Path to point shapefile directory
    :param buffer_size: int
        Buffer size specifies the length of the rectangular buffer around the point
    """
    # Import Patches for each class and all 4 layerstacks (VH/VV/Asc/Desc)
    patches = create_point_buffer(point_path, buffer_size=buffer_size)
    layer_stacks = extract_files_to_list(path_to_folder=results_dir, datatype=".tif", path_bool=True)

    # Iterate through all layerstacks:
    for file in layer_stacks:
        src1 = rio.open(file)
        patch_mean = []
        # Iterate through all patches of current class
        for patch in patches:
            pixel_mean = []
            out_image, out_transform = rio.mask.mask(src1, [patch], all_touched=1, crop=True, nodata=np.nan)
            # Calculate Mean for each patch:
            for pixel in out_image:
                pixel_mean.append(np.nanmean(pixel))
            patch_mean.append(pixel_mean)

        # Append dates of acquisition to each list:
        if "VH" in file and "Asc" in file:
            patch_mean.append(extract_dates(results_dir + "VH" + "/" + "Asc" + "/"))
        if "VH" in file and "Desc" in file:
            patch_mean.append(extract_dates(results_dir + "VH" + "/" + "Desc" + "/"))
        if "VV" in file and "Asc" in file:
            patch_mean.append(extract_dates(results_dir + "VV" + "/" + "Asc" + "/"))
        if "VV" in file and "Desc" in file:
            patch_mean.append(extract_dates(results_dir + "VV" + "/" + "Desc" + "/"))

        # Rotate array, so csv file will have correct orientation:
        patch_mean = np.rot90(patch_mean)
        patch_mean = np.rot90(patch_mean)
        patch_mean = np.rot90(patch_mean)
        patch_mean = patch_mean.tolist()
        src1.close()

        # Export patch means to csv files for each class, polarization and flight direction:
        if "VH" in file and "Asc" in file:
            np.savetxt(results_dir + point_path[point_path.index("clc"):point_path.index("clc")+6] + "_VH_Asc.csv",
                       patch_mean, delimiter=",", header="date,VH1,VH2,VH3,VH4,VH5,VH6,VH7,VH8,VH9,VH10,VH11,VH12,VH13,"
                                                         "VH14,VH15,VH16,VH17,VH18,VH19,VH20", fmt='%f')
        if "VH" in file and "Desc" in file:
            np.savetxt(results_dir + point_path[point_path.index("clc"):point_path.index("clc")+6] + "_VH_Desc.csv",
                       patch_mean, delimiter=",", header="date,VH1,VH2,VH3,VH4,VH5,VH6,VH7,VH8,VH9,VH10,VH11,VH12,VH13,"
                                                         "VH14,VH15,VH16,VH17,VH18,VH19,VH20", fmt='%f')
        if "VV" in file and "Asc" in file:
            np.savetxt(results_dir + point_path[point_path.index("clc"):point_path.index("clc")+6] + "_VV_Asc.csv",
                       patch_mean, delimiter=",", header="date,VV1,VV2,VV3,VV4,VV5,VV6,VV7,VV8,VV9,VV10,VV11,VV12,VV13,"
                                                         "VV14,VV15,VV16,VV17,VV18,VV19,VV20", fmt='%f')
        if "VV" in file and "Desc" in file:
            np.savetxt(results_dir + point_path[point_path.index("clc"):point_path.index("clc")+6] + "_VV_Desc.csv",
                       patch_mean, delimiter=",", header="date,VV1,VV2,VV3,VV4,VV5,VV6,VV7,VV8,VV9,VV10,VV11,VV12,VV13,"
                                                         "VV14,VV15,VV16,VV17,VV18,VV19,VV20", fmt='%f')


def import_csv(path_to_folder):
    """
    Imports csv files from results folder
    :param path_to_folder: string
        Path to folder, where csv files are stored
    :return: tuple
        returns tuple of lists containing the dataframe names and the dataframes itself
    """
    import pandas as pd
    csv_list = extract_files_to_list(path_to_folder, datatype=".csv", path_bool=False)
    df_name_list = []
    df_list = []
    for csv in csv_list:
        df = pd.read_csv(path_to_folder + csv)
        df = df.rename({"# date": "date"}, axis=1)
        # Change datatype of date from float to date object:
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
        df_name_list.append(csv[0:len(csv)-4])
        df_list.append(df)
    return df_name_list, df_list


def temporal_statistics(path_to_folder, plot_bool):
    """
    Function calculates temporal statistics for all classes, polarizations and flight directions
    :param path_to_folder: string
        Path to folder, where csv files are storec
    :param plot_bool: boolean
        If set to True, charts of mean and std.dev. are plotted
    :return: dict
        Returns dictionary containing dictionaries with the temporal statistics for all classes, polarizations and
        flight directions
    """
    import matplotlib.pyplot as plt
    df_name_list, df_list = import_csv(path_to_folder)
    statistics_dict = {}

    # Iterate through all dataframes and compute temporal statistics
    for i, df in enumerate(df_list):
        # Temporal Mean:
        df["patches_mean"] = df.mean(axis=1)
        statistics_dict[df_name_list[i]] = {"Temporal Mean": df["patches_mean"].mean()}

        # Temporal Standard Deviation:
        df["patches_std"] = df.std(axis=1)
        statistics_dict[df_name_list[i]]["Temporal Stdev."] = df["patches_std"].mean()

        # Max., Min. and Amplitude:
        statistics_dict[df_name_list[i]]["Temporal Max."] = df["patches_mean"].max()
        statistics_dict[df_name_list[i]]["Temporal Min."] = df["patches_mean"].min()
        statistics_dict[df_name_list[i]]["Temporal Amp."] = df["patches_mean"].max() - df["patches_mean"].min()

    # Plot mean of all patches over timne if boolean is TRUE
    if plot_bool:
        tmp = 0
        # Iterate through a quarter of the csv files to account for all four possible options of VH/VV/Asc/Desc
        for j in range(0, int(len(df_name_list)/4)):
            # Iterate through Mean and Std.Dev.:
            for k, elem in enumerate(["patches_mean", "patches_std"]):
                if k == 0:
                    plt.title('Mean of all Patches for class: ' + str(df_name_list[tmp][0:6]))
                if k == 1:
                    plt.title('Std.Dev. of all Patches for class: ' + str(df_name_list[tmp][0:6]))
                plt.plot('date', elem, data=df_list[tmp+0], marker='', color='blue', linewidth=2,
                         label=df_name_list[tmp+0])
                plt.plot('date', elem, data=df_list[tmp+1], marker='', color='black', linewidth=2,
                         label=df_name_list[tmp+1])
                plt.plot('date', elem, data=df_list[tmp+2], marker='', color='green', linewidth=2,
                         label=df_name_list[tmp+2])
                plt.plot('date', elem, data=df_list[tmp+3], marker='', color='red', linewidth=2,
                         label=df_name_list[tmp+3])
                plt.legend()
                plt.show()
            # Increase tmp by 4 to get to the next class
            tmp = tmp + 4
    print(statistics_dict)
    return statistics_dict
