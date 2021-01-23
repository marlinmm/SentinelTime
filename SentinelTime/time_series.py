from SentinelTime.data_preprocessing import *
from SentinelTime.mask_stack import *
import rasterio.mask
import matplotlib.pyplot as plt
import pandas as pd


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


def extract_time_series(results_dir, shapefile, buffer_size, point_path):
    """
    Extracts time series information from patches of pixels using points and a buffer size to specify the size of the
    patch
    :param shapefile: string
        Path to point shapefile including name of shapefile
    :param results_dir: string
        Path to results directory, where layerstacks are stored and csv files will be stored
    :param point_path: string
        Path to point shapefile directory
    :param buffer_size: int
        Buffer size specifies the length of the rectangular buffer around the point
    """
    # Import Patches for each class and all 4 layerstacks (VH/VV/Asc/Desc)
    patches = create_point_buffer(shapefile, buffer_size=buffer_size)
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

        # Append dates of acquisition to each list (will be stored as float, doesnt matter for processing):
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

        # Create CSV export directory and create header string with length equal to the number of patcher per class:
        csv_result_dir = results_dir + "CSV/"
        if not os.path.exists(csv_result_dir):
            os.mkdir(csv_result_dir)
        if "VH" in file:
            pol1 = "VH"
            vh_head_string = "VH"
            tmp = ","
            for i, elem in enumerate(patches):
                vh_head_string = vh_head_string + str(i) + tmp + pol1
        if "VV" in file:
            pol1 = "VV"
            vv_head_string = "VV"
            tmp = ","
            for i, elem in enumerate(patches):
                vv_head_string = vv_head_string + str(i) + tmp + pol1

        # Export patch means to csv files for each class, polarization and flight direction:
        if "VH" in file and "Asc" in file:
            np.savetxt(csv_result_dir + shapefile[len(point_path):len(shapefile) - 4] + "_VH_Asc.csv",
                       patch_mean, delimiter=",", header="date," + vh_head_string[0:len(vh_head_string) - 3], fmt='%f')
        if "VH" in file and "Desc" in file:
            np.savetxt(csv_result_dir + shapefile[len(point_path):len(shapefile) - 4] + "_VH_Desc.csv",
                       patch_mean, delimiter=",", header="date," + vh_head_string[0:len(vh_head_string) - 3], fmt='%f')
        if "VV" in file and "Asc" in file:
            np.savetxt(csv_result_dir + shapefile[len(point_path):len(shapefile) - 4] + "_VV_Asc.csv",
                       patch_mean, delimiter=",", header="date," + vv_head_string[0:len(vv_head_string) - 3], fmt='%f')
        if "VV" in file and "Desc" in file:
            np.savetxt(csv_result_dir + shapefile[len(point_path):len(shapefile) - 4] + "_VV_Desc.csv",
                       patch_mean, delimiter=",", header="date," + vv_head_string[0:len(vv_head_string) - 3], fmt='%f')


def import_time_series_csv(path_to_folder, frost_bool):
    """
    Imports csv files from results folder
    :param frost_bool:
    :param path_to_folder: string
        Path to folder, where csv files are stored
    :return: tuple
        returns tuple of lists containing the dataframe names and the dataframes itself
    """
    csv_list = extract_files_to_list(path_to_folder, datatype=".csv", path_bool=False)
    df_name_list = []
    df_list = []
    for csv in csv_list:
        df = pd.read_csv(path_to_folder + csv)
        df = df.rename({"# date": "date"}, axis=1)
        # Change datatype of date from float to date object:
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

        # if frost_bool:
        #     df, precip = import_weather_for_fern(radar_df=df)

        if frost_bool:
            df, weather = import_weather_for_fern(radar_df=df, frost_bool=frost_bool)
        if not frost_bool:
            weather = import_weather_for_fern(radar_df=df, frost_bool=frost_bool)

        df_name_list.append(csv[0:len(csv) - 4])
        df_list.append(df)
    return df_name_list, df_list, weather


def temporal_statistics(path_to_csv_folder, results_dir, fig_folder, plot_bool, frost_bool):
    """
    Function calculates temporal statistics for all classes, polarizations and flight directions
    :param fig_folder:
    :param frost_bool:
    :param path_to_csv_folder:
        Path to folder, where csv files are stored
    :param results_dir:

    :param plot_bool: boolean
        If set to True, charts of mean and std.dev. are plotted
    :return: dict
        Returns dictionary containing dictionaries with the temporal statistics for all classes, polarizations and
        flight directions
    """
    import csv
    from scipy.ndimage.filters import gaussian_filter1d
    df_name_list, df_list, weather = import_time_series_csv(path_to_csv_folder, frost_bool)
    statistics_dict = {}
    # print(df_name_list)

    # Iterate through all dataframes and compute temporal statistics
    for i, df in enumerate(df_list):
        # print(df)
        # Temporal Mean:
        df["patches_mean"] = df.mean(axis=1)
        # print(df_name_list[i])
        statistics_dict[df_name_list[i]] = {"Temporal Mean": round(df["patches_mean"].mean(), 3)}

        # Temporal Standard Deviation:
        df["patches_std"] = df.std(axis=1)
        statistics_dict[df_name_list[i]]["Temporal Stdev."] = round(df["patches_std"].mean(), 3)

        # Max., Min. and Amplitude:
        statistics_dict[df_name_list[i]]["Temporal Max."] = round(df["patches_mean"].max(), 3)
        statistics_dict[df_name_list[i]]["Temporal Min."] = round(df["patches_mean"].min(), 3)
        statistics_dict[df_name_list[i]]["Temporal Amp."] = round(df["patches_mean"].max()
                                                                  - df["patches_mean"].min(), 3)

    dataframe_list1 = []
    dataframe_list2 = []
    dataframe_list3 = []
    dataframe_list4 = []
    tmp = 0
    # Iterate through a quarter of the csv files to account for all four possible options of VH/VV/Asc/Desc
    for j in range(0, int(len(df_name_list) / 4)):
        # Iterate through Mean and Std.Dev.:
        for k, elem in enumerate(["patches_mean"]):
            # Plot mean of all patches over time if boolean is TRUE
            if plot_bool:
                plt.figure(figsize=(16, 9))
                plt.rcParams.update({'font.size': 14})

                # TODO: make weather data stuff optional!!!!

                def make_patch_spines_invisible(ax):
                    ax.set_frame_on(True)
                    ax.patch.set_visible(False)
                    for sp in ax.spines.values():
                        sp.set_visible(False)

                fig, ax1 = plt.subplots()
                fig.subplots_adjust(right=0.75)

                fig.set_figheight(9)
                fig.set_figwidth(15)
                ax2 = ax1.twinx()
                ax3 = ax1.twinx()

                ax3.spines["right"].set_position(("axes", 1.1))

                make_patch_spines_invisible(ax3)
                ax3.spines["right"].set_visible(True)

                # plt.figure(figsize=(16, 9))
                # plt.rcParams.update({'font.size': 14})
                if k == 0:
                    # ax1.figure(figsize=(16, 9))
                    plt.title('Mean of all Patches for class: ' + str(df_name_list[tmp][0:17]))
                if k == 1:
                    # ax1.figure(figsize=(16, 9))
                    plt.title('Std.Dev. of all Patches for class: ' + str(df_name_list[tmp][0:17]))
                ax1.plot('date', elem, data=df_list[tmp], marker='', color='k', linewidth=0.7, label="")
                ax1.plot('date', elem, data=df_list[tmp + 1], marker='', color='forestgreen', linewidth=0.7, label="")
                # print(df_name_list[tmp + 3])
                # print(df_name_list[tmp + 2])
                ax1.plot('date', elem, data=df_list[tmp + 2], marker='', color='b', linewidth=0.7, label="")
                ax1.plot('date', elem, data=df_list[tmp + 3], marker='', color='firebrick', linewidth=0.7, label="")

            # filter time series using gaussian filter:
            arr1 = gaussian_filter1d(df_list[tmp]["patches_mean"].to_numpy(), sigma=2)
            arr2 = gaussian_filter1d(df_list[tmp + 1]["patches_mean"].to_numpy(), sigma=2)
            arr3 = gaussian_filter1d(df_list[tmp + 2]["patches_mean"].to_numpy(), sigma=2)
            arr4 = gaussian_filter1d(df_list[tmp + 3]["patches_mean"].to_numpy(), sigma=2)

            # append filterd datasets to lists for further use:
            dataframe_list1.append(arr1)
            dataframe_list2.append(arr2)
            dataframe_list3.append(arr3)
            dataframe_list4.append(arr4)

            # Plot filtered mean of all patches over time if boolean is TRUE
            if plot_bool:
                #
                ax1.plot(df_list[tmp]['date'], arr1, marker='', color='k', linewidth=3,
                         label=df_name_list[tmp][18:len(df_name_list[tmp])])

                ax1.plot(df_list[tmp + 1]['date'], arr2, marker='', color='forestgreen', linewidth=3,
                         label=df_name_list[tmp + 1][18:len(df_name_list[tmp + 1])])

                ax1.plot(df_list[tmp + 2]['date'], arr3, marker='', color='b', linewidth=3,
                         label=df_name_list[tmp + 2][18:len(df_name_list[tmp + 2])])

                ax1.plot(df_list[tmp + 3]['date'], arr4, marker='', color='firebrick', linewidth=3,
                         label=df_name_list[tmp + 3][18:len(df_name_list[tmp + 3])])

                # TODO: make weather data stuff optional!!!!

                print(df_name_list[tmp + 3][18:len(df_name_list[tmp + 3])])
                # plt.xlabel("Date")
                ax1.set_xlabel('Date')
                ax1.set_ylabel('Backscatter (dB)')
                # plt.ylabel("Backscatter (dB)")
                ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.005),
                           ncol=4, fancybox=True, shadow=True)
                plt.ylim((-18, -7))

                print(weather)

                ax2.plot(weather['date'], weather['precip'], color="silver")
                # plt.ylabel("Precipitation (mm)")
                ax2.set_ylabel('Precipitation (mm)', color="silver")
                # plt.ylim((-10, 50))
                ax2.set_ylim(-10, 110)

                ax3.plot(weather['date'], weather['temp'], color="orange")
                # plt.ylabel("Precipitation (mm)")
                ax3.set_ylabel('Avg_Temp (°C)', color="orange")
                # plt.ylim((-10, 110))
                ax3.set_ylim(-10, 110)

                plt.savefig(fig_folder + "Mean_for_Class_test" + str(df_name_list[tmp][0:17]) + ".png", dpi=300)
                plt.show()

        # Increase tmp by 4 to get to the next class
        tmp = tmp + 4
    # Export temporal statistics to csv file:
    with open(results_dir + 'Temp_Statistics.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in statistics_dict.items():
            # print(value)
            writer.writerow([key, value])
    return dataframe_list1, dataframe_list2, dataframe_list3, dataframe_list4, df_list


def ratio_calc(path_to_folder, plot_bool, frost_bool):
    """
    This function calculates the VH/VV ratio for all classes and flight directions and allows the user to plot the data
    :param frost_bool: XXXXXXXXXXXXXXXXXXXXXXXX
    :param path_to_folder: string
        Path to folder, where csv files are stored
    :param plot_bool: boolean
        If set to TRUE, the plots are calculated and shown
    :return: list
        Returns a list of dataframes containing VH/VV ratios for all classes and flight directions
    """
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('max_colwidth', -1)

    df_name_list, df_list, weather = import_time_series_csv(path_to_folder + "CSV/", frost_bool)
    tmp = 0
    Asc_ratio_list = []
    Desc_ratio_list = []
    for i in range(int(len(df_list) / 4)):

        VH_Asc_df = df_list[tmp]
        VH_Asc_df["patches_mean"] = df_list[tmp].mean(axis=1)

        VH_Desc_df = df_list[tmp + 1]
        VH_Desc_df["patches_mean"] = df_list[tmp + 1].mean(axis=1)

        VV_Asc_df = df_list[tmp + 2]
        VV_Asc_df["patches_mean"] = df_list[tmp + 2].mean(axis=1)

        VV_Desc_df = df_list[tmp + 3]
        VV_Desc_df["patches_mean"] = df_list[tmp + 3].mean(axis=1)

        tmp = tmp + 4
        Asc_ratio = pd.DataFrame()
        Asc_ratio["date"] = VH_Asc_df["date"]
        Asc_ratio["VH_VV"] = VH_Asc_df["patches_mean"] - VV_Asc_df["patches_mean"]
        # print(Asc_ratio)

        Desc_ratio = pd.DataFrame()
        Desc_ratio["date"] = VH_Desc_df["date"]
        Desc_ratio["VH_VV"] = VH_Desc_df["patches_mean"] - VV_Desc_df["patches_mean"]
        # print(Desc_ratio)

        Asc_ratio_list.append(Asc_ratio)
        Desc_ratio_list.append(Desc_ratio)

        if plot_bool:
            plt.title('Std.Dev. of all Patches for class: ' + str(df_name_list[tmp][0:6]))
            plt.plot('date', "VH_VV", data=Asc_ratio, marker='', color='blue', linewidth=2,
                     label="VH_VV_ratio for Asc")
            plt.plot('date', "VH_VV", data=Desc_ratio, marker='', color='black', linewidth=2,
                     label="VH_VV_ratio for Desc")
            plt.legend()
            plt.show()
    return Asc_ratio_list, Desc_ratio_list


def import_weather_for_fern(radar_df, frost_bool):
    fern_weather_station_data = "G:/Weather_data/Tageswerte_Lotschen_002.csv"
    lotschen_weather_df = pd.read_csv(fern_weather_station_data, sep=";", decimal=',')

    lotschen_weather_df = lotschen_weather_df.rename({"Tag": "date"}, axis=1)
    lotschen_weather_df['date'] = pd.to_datetime(lotschen_weather_df['date'], format='%d.%m.%Y')

    weather_df = pd.DataFrame(columns=['date', 't_min', 'precip'])
    weather_df['date'] = lotschen_weather_df['date']
    weather_df['t_min'] = lotschen_weather_df['MIN_TA200']
    weather_df['precip'] = lotschen_weather_df['SUM_NN050']
    weather_df['temp'] = lotschen_weather_df['AVG_TA200']

    combine = pd.merge(radar_df, weather_df, on='date')
    weather = combine
    if frost_bool:
        combine = combine.query("t_min >= -1")
        combine = combine.reset_index(drop=True)
        combine = combine.drop("t_min", axis=1)
        combine = combine.drop("precip", axis=1)
        combine = combine.drop("temp", axis=1)
        return combine, weather
    if not frost_bool:
        return weather
