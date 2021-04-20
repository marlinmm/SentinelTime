from SentinelTime.time_series import *
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def dataframe_difference_calc(path_to_csv_folder, results_dir, fig_folder, plot_bool, weather_bool, frost_bool):
    all_data_list = []
    VH_Asc, VH_Desc, VV_Asc, VV_Desc, df_list = temporal_statistics(path_to_csv_folder, results_dir, fig_folder,
                                                                    plot_bool, weather_bool, frost_bool)
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
        print(len(elem))

        # zero_max_diff = np.subtract(elem[0], elem[3])
        # zero_medium_diff = np.subtract(elem[0], elem[2])
        # zero_min_diff = np.subtract(elem[0], elem[1])

        zero_max_diff = np.abs(elem[0] - elem[1])
        # zero_medium_diff = np.abs(elem[0] - elem[2])
        # zero_min_diff = np.abs(elem[0] - elem[1])

        zero_max_diff_list.append(zero_max_diff.tolist())
        # print(zero_max_diff_list)
        # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        # zero_medium_diff_list.append(zero_medium_diff)
        # zero_min_diff_list.append(zero_min_diff)
        if plot_bool:
            plt.figure(figsize=(16, 9))
            plt.rcParams.update({'font.size': 14})
            plt.xlabel("Date")
            plt.ylabel("Backscatter (dB)")
            plt.title('Fern_density_difference: ' + title)
            plt.plot(df_list[i]['date'], zero_max_diff, marker='', color='green', linewidth=2, label=label_list[0])
            # plt.plot(df_list[i]['date'], zero_medium_diff, marker='', color='red', linewidth=2, label=label_list[1])
            # plt.plot(df_list[i]['date'], zero_min_diff, marker='', color='blue', linewidth=2, label=label_list[2])
            plt.legend()
            plt.savefig(fig_folder + "Fern_density_difference_" + title + ".png", dpi=300)
            plt.show()
    return zero_max_diff_list, zero_medium_diff_list, zero_min_diff_list, df_list


def boxplots(path_to_csv_folder, results_dir, fig_folder, plot_bool, season, weather_bool, frost_bool, input_data):
    from matplotlib import rcParams
    all_data_list = []
    # fern_class_name_list = ["0", "1", "2", "3"]
    fern_class_name_list = ["0", "3"]
    title_list = ["VH_Asc", "VH_Desc", "VV_Asc", "VV_Desc"]

    if input_data == "mean":
        VH_Asc, VH_Desc, VV_Asc, VV_Desc, df_list = temporal_statistics(path_to_csv_folder, results_dir, fig_folder,
                                                                        plot_bool, weather_bool, frost_bool)
        all_data_list.append(VH_Asc)
        all_data_list.append(VH_Desc)
        all_data_list.append(VV_Asc)
        all_data_list.append(VV_Desc)
        # print(len(all_data_list))

    if input_data == "diff":
        zero_max_diff_list, zero_medium_diff_list, zero_min_diff_list, df_list = dataframe_difference_calc(
            path_to_csv_folder, results_dir, fig_folder, plot_bool, weather_bool, frost_bool)

        all_data_list = zero_max_diff_list
    rcParams['figure.figsize'] = 9, 12
    for i, elem in enumerate(all_data_list):
        # print(len(elem))
        if input_data == "mean":
            df = pd.DataFrame.from_dict(dict(zip(fern_class_name_list, elem)))
        if input_data == "diff":
            df = pd.DataFrame({title_list[i]: elem})

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

            # create dataframe for all meteorological spring values
            if seasons == "Spring":
                title = title + " " + seasons
                df_season = df[(df['date'] > '2017-03-01') & (df['date'] <= '2017-05-31')
                               | (df['date'] > '2018-03-01') & (df['date'] <= '2018-05-31')
                               | (df['date'] > '2019-03-01') & (df['date'] <= '2019-05-31')
                               | (df['date'] > '2020-03-01') & (df['date'] <= '2020-05-31')]

                # df_season = df[(df['date'] > '2020-03-01') & (df['date'] <= '2020-05-31')]

                # append data to dict for difference boxplots
                if input_data == "diff":
                    season_dict = {"Spring": df_season[title_list[i]].values.tolist()}

            # create dataframe for all meteorological summer values:
            if seasons == "Summer":
                title = title + " " + seasons
                df_season = df[(df['date'] > '2016-06-01') & (df['date'] <= '2016-08-31')
                               | (df['date'] > '2017-06-01') & (df['date'] <= '2017-08-31')
                               | (df['date'] > '2018-06-01') & (df['date'] <= '2018-08-31')
                               | (df['date'] > '2019-06-01') & (df['date'] <= '2019-08-31')
                               | (df['date'] > '2020-06-01') & (df['date'] <= '2020-08-31')]

                # df_season = df[(df['date'] > '2020-06-01') & (df['date'] <= '2020-08-31')]

                # append data to dict for difference boxplots
                if input_data == "diff":
                    season_dict["Summer"] = df_season[title_list[i]].values.tolist()

            # create dataframe for all meteorological autumn values:
            if seasons == "Autumn":
                title = title + " " + seasons
                df_season = df[(df['date'] > '2016-09-01') & (df['date'] <= '2016-11-30')
                               | (df['date'] > '2017-09-01') & (df['date'] <= '2017-11-30')
                               | (df['date'] > '2018-09-01') & (df['date'] <= '2018-11-30')
                               | (df['date'] > '2019-09-01') & (df['date'] <= '2019-11-30')
                               | (df['date'] > '2020-09-01') & (df['date'] <= '2020-11-30')]

                # df_season = df[(df['date'] > '2020-09-01') & (df['date'] <= '2020-11-30')]

                # append data to dict for difference boxplots
                if input_data == "diff":
                    season_dict["Autumn"] = df_season[title_list[i]].values.tolist()

            # create dataframe for all meteorological winter values:
            if seasons == "Winter":
                title = title + " " + seasons
                df_season = df[(df['date'] > '2016-12-01') & (df['date'] <= '2017-02-28')
                               | (df['date'] > '2017-12-01') & (df['date'] <= '2018-02-28')
                               | (df['date'] > '2018-12-01') & (df['date'] <= '2019-02-28')
                               | (df['date'] > '2019-12-01') & (df['date'] <= '2020-02-28')
                               | (df['date'] > '2020-12-01') & (df['date'] <= '2021-02-28')]

                # df_season = df[(df['date'] > '2019-12-01') & (df['date'] <= '2020-02-28')
                #                | (df['date'] > '2020-12-01') & (df['date'] <= '2021-02-28')]

                # append data to dict for difference boxplots
                if input_data == "diff":
                    season_dict["Winter"] = df_season[title_list[i]].values.tolist()

            # Plot Boxplots for all fern density classes for VH/VV/Desc/Asc and seasons:
            if input_data == "mean":
                if "VH" in title:
                    plt.ylim([-14, -12])
                if "VV" in title:
                    plt.ylim([-10, -7.5])

                df_season = df_season.drop("date", axis=1)
                df_melt = pd.melt(df_season)
                df_melt = df_melt.rename(columns={'variable': 'Fern Density Class', 'value': 'Backscatter (dB)'})

                rcParams['figure.figsize'] = 9, 12
                # colors = ["#179AFF", "#13F3EC", "#EFCE14", "#EE6922"]
                # sns.set(font_scale=2)

                # print(seasons)
                print(title)
                print(np.median(df_melt["Backscatter (dB)"]))
                x = sns.boxplot(x="Fern Density Class", y="Backscatter (dB)", data=df_melt)
                x.set_title(title, fontsize=20)
                x.set_xlabel("Fern Density Class", fontsize=20)
                x.set_ylabel("Backscatter (dB)", fontsize=20)
                x.set_yticklabels(x.get_yticks(), size=16)
                x.set_xticklabels(x.get_xticks(), size=16)
                # plt.set_figheight(6)
                # fig.set_figwidth(4)

                plt.savefig(fig_folder + "Fern Class Comparison_ " + title + ".svg", dpi=300, format="svg")

                df_melt.to_csv(fig_folder + "csv_out/" + title + ".csv", index=False)

                plt.show()

        # Plot Boxplots for Zero-Max fern density difference for VH/VV/Desc/Asc and all seasons:
        if input_data == "diff":
            import csv
            fig, ax = plt.subplots()
            fig.set_figheight(9)
            fig.set_figwidth(6)
            plt.ylim([0, 1.75])
            rcParams['axes.labelsize'] = 13
            rcParams['axes.titlesize'] = 13
            title = 'Fern Density Difference: ' + title_list[i]
            plt.title(title)
            plt.ylabel("Backscatter Difference (dB)")

            print(season_dict.values())
            print(len(season_dict.values()))
            median_list = []
            with open(fig_folder + "csv_out/" + title[24:] + ".csv", 'w') as myfile:
                for elem in season_dict.values():
                    print(title)
                    temp_median = np.median(elem)
                    median_list.append(temp_median)
                    wr = csv.writer(myfile)
                    wr.writerow(elem)
                print(median_list)
                print(np.mean(median_list))

            ax.boxplot(season_dict.values())
            ax.set_xticklabels(season_dict.keys())
            plt.savefig(fig_folder + "Difference_" + title_list[i] + ".svg", dpi=300)
            plt.show()


def singlepixel_vs_multipixel(path_to_csv_folder, results_dir, fig_folder, plot_bool, weather_bool, frost_bool):
    single_folder = path_to_csv_folder + "individual_patches_20m/"
    # multi_folder = path_to_csv_folder + "20m/"
    multi_folder = path_to_csv_folder

    S_VH_Asc, S_VH_Desc, S_VV_Asc, S_VV_Desc, df_list = temporal_statistics(single_folder, results_dir, fig_folder,
                                                                            plot_bool, weather_bool, frost_bool)

    M_VH_Asc, M_VH_Desc, M_VV_Asc, M_VV_Desc, df_list = temporal_statistics(multi_folder, results_dir, fig_folder,
                                                                            plot_bool, weather_bool, frost_bool)
    name_list = ["VH_Asc", "VH_Desc", "VV_Asc", "VV_Desc"]
    class_list = ["Fern Class 0", "Fern Class 3"]
    print("!")
    fern_class_list = [0, 1]

    for i, fern_class in enumerate(fern_class_list):
        fig, ax1 = plt.subplots()

        fig.set_figheight(6)
        fig.set_figwidth(10)

        ax1.set_xlabel('Date')
        ax1.set_ylabel('Backscatter Difference (dB)')

        VH_Asc_diff = S_VH_Asc[fern_class] - M_VH_Asc[fern_class]
        VH_Desc_diff = S_VH_Desc[fern_class] - M_VH_Desc[fern_class]
        VV_Asc_diff = S_VV_Asc[fern_class] - M_VV_Asc[fern_class]
        VV_Desc_diff = S_VV_Desc[fern_class] - M_VV_Desc[fern_class]

        print(class_list[i] + " VH_Asc_Mean: " + str(np.mean(VH_Asc_diff)))
        print(class_list[i] + " VH_Desc_Mean: " + str(np.mean(VH_Desc_diff)))
        print(class_list[i] + " VV_Asc_Mean: " + str(np.mean(VV_Asc_diff)))
        print(class_list[i] + " VV_Desc_Mean: " + str(np.mean(VV_Desc_diff)))

        ax1.plot(df_list[0]["date"], VH_Asc_diff, color='k', label=name_list[0])
        ax1.plot(df_list[1]["date"], VH_Desc_diff, color='forestgreen', label=name_list[1])
        ax1.plot(df_list[2]["date"], VV_Asc_diff, color='b', label=name_list[2])
        ax1.plot(df_list[3]["date"], VV_Desc_diff, color='firebrick', label=name_list[3])
        ax1.legend(loc='upper center', ncol=4, fancybox=True, shadow=True)
        plt.xticks(rotation=45, ha='right')
        plt.show()
