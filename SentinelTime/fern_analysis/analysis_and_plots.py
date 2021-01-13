from SentinelTime.time_series import *
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def dataframe_difference_calc(path_to_csv_folder, results_dir, plot_bool, frost_bool):
    all_data_list = []
    VH_Asc, VH_Desc, VV_Asc, VV_Desc, df_list = temporal_statistics(path_to_csv_folder, results_dir, plot_bool,
                                                                    frost_bool)
    all_data_list.append(VH_Asc)
    all_data_list.append(VH_Desc)
    all_data_list.append(VV_Asc)
    all_data_list.append(VV_Desc)
    title_list = ["VH_Asc", "VH_Desc", "VV_Asc", "VV_Desc"]
    label_list = ["zero-max", "zero-medium", "zero-min"]

    zero_max_diff_list = []
    zero_medium_diff_list = []
    zero_min_diff_list = []

    # print(VH_Asc)
    for i, elem in enumerate(all_data_list):
        title = title_list[i]

        zero_max_diff = np.subtract(elem[0], elem[3])
        zero_medium_diff = np.subtract(elem[0], elem[2])
        zero_min_diff = np.subtract(elem[0], elem[1])

        zero_max_diff_list.append(zero_max_diff.tolist())
        print(zero_max_diff_list)
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        zero_medium_diff_list.append(zero_medium_diff)
        zero_min_diff_list.append(zero_min_diff)
        if plot_bool:
            plt.figure(figsize=(16, 9))
            plt.rcParams.update({'font.size': 14})
            plt.xlabel("Date")
            plt.ylabel("Backscatter (dB)")
            plt.title('Fern_density_difference: ' + title)
            plt.plot(df_list[i]['date'], zero_max_diff, marker='', color='green', linewidth=2, label=label_list[0])
            plt.plot(df_list[i]['date'], zero_medium_diff, marker='', color='red', linewidth=2, label=label_list[1])
            plt.plot(df_list[i]['date'], zero_min_diff, marker='', color='blue', linewidth=2, label=label_list[2])
            plt.legend()
            plt.show()
    return zero_max_diff_list, zero_medium_diff_list, zero_min_diff_list, df_list


def boxplots(path_to_csv_folder, results_dir, plot_bool, season, frost_bool, input_data):

    all_data_list = []
    fern_class_name_list = ["Fern_0", "Fern_1", "Fern_2", "Fern_3"]
    title_list = ["VH_Asc", "VH_Desc", "VV_Asc", "VV_Desc"]

    if input_data == "mean":
        VH_Asc, VH_Desc, VV_Asc, VV_Desc, df_list = temporal_statistics(path_to_csv_folder, results_dir, plot_bool,
                                                                        frost_bool)
        all_data_list.append(VH_Asc)
        all_data_list.append(VH_Desc)
        all_data_list.append(VV_Asc)
        all_data_list.append(VV_Desc)
        print(len(all_data_list))
    if input_data == "diff":
        zero_max_diff_list, zero_medium_diff_list, zero_min_diff_list, df_list = dataframe_difference_calc(path_to_csv_folder,
                                                                                                           results_dir,
                                                                                                           plot_bool=False,
                                                                                                           frost_bool=False)
        # print(zero_max_diff_list)
        all_data_list = zero_max_diff_list
    for i, elem in enumerate(all_data_list):
        print(len(elem))
        df = pd.DataFrame.from_dict(dict(zip(fern_class_name_list, elem)))
        # df = pd.DataFrame(elem)
        print(df)
        for seasons in season:
            title = title_list[i]
            # plt.figure(figsize=(16, 12))
            # plt.rcParams.update({'font.size': 14})
            if "Asc" in title:
                # plt.ylim([-16, -12])
                df["date"] = df_list[i]["date"]
            if "Desc" in title:
                # plt.ylim([-11, -7.5])
                df["date"] = df_list[i]["date"]

            # clean frozen days:
            # df = import_weather_for_fern(radar_df=df)

            if seasons == "spring":
                df_season = df[(df['date'] > '2017-03-01') & (df['date'] <= '2017-05-31')
                    | (df['date'] > '2018-03-01') & (df['date'] <= '2018-05-31')
                    | (df['date'] > '2019-03-01') & (df['date'] <= '2019-05-31')
                    | (df['date'] > '2020-03-01') & (df['date'] <= '2020-05-31')]
                title = title + "_" + seasons
                df_spring = df_season
                print(seasons + " " + str(len(df_season)))
            if seasons == "summer":
                df_season = df[(df['date'] > '2016-06-01') & (df['date'] <= '2016-08-31')
                    | (df['date'] > '2017-06-01') & (df['date'] <= '2017-08-31')
                    | (df['date'] > '2018-06-01') & (df['date'] <= '2018-08-31')
                    | (df['date'] > '2019-06-01') & (df['date'] <= '2019-08-31')
                    | (df['date'] > '2020-06-01') & (df['date'] <= '2020-08-31')]
                title = title + "_" + seasons
                df_summer = df_season
                print(seasons + " " + str(len(df_season)))
            if seasons == "autumn":
                df_season = df[(df['date'] > '2016-09-01') & (df['date'] <= '2016-11-30')
                    | (df['date'] > '2017-09-01') & (df['date'] <= '2017-11-30')
                    | (df['date'] > '2018-09-01') & (df['date'] <= '2018-11-30')
                    | (df['date'] > '2019-09-01') & (df['date'] <= '2019-11-30')
                    | (df['date'] > '2020-09-01') & (df['date'] <= '2020-11-30')]
                title = title + "_" + seasons
                df_autumn = df_season
                print(seasons + " " + str(len(df_season)))
            if seasons == "winter":
                df_season = df[(df['date'] > '2016-12-01') & (df['date'] <= '2017-02-28')
                   | (df['date'] > '2017-12-01') & (df['date'] <= '2018-02-28')
                   | (df['date'] > '2018-12-01') & (df['date'] <= '2019-02-28')
                   | (df['date'] > '2019-12-01') & (df['date'] <= '2020-02-28')
                   | (df['date'] > '2020-12-01') & (df['date'] <= '2021-02-28')]
                title = title + "_" + seasons
                df_winter = df_season
                print(seasons + " " + str(len(df_season)))

            df_season = df_season.drop("date", axis=1)
            print(df_season)
            df_melt = pd.melt(df_season)
            df_melt = df_melt.rename(columns={'variable': 'Fern_density', 'value': 'Backscatter (dB)'})
            print(df_melt)
            sns.boxplot(x="Fern_density", y="Backscatter (dB)", data=df_melt).set_title(title)
            plt.show()
