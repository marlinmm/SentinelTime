from SentinelTime import time_series, data_preprocessing, mask_stack


def import_weather_csv(path_to_weather_folder):
    """
    """
    import pandas as pd
    csv_list = data_preprocessing.extract_files_to_list(path_to_weather_folder, datatype=".csv", path_bool=False)
    df_list = []
    for csv in csv_list:
        df = pd.read_csv(path_to_weather_folder + csv, sep=";", decimal=',')
        df_list.append(df)
    return df_list


def calc_evapotranspiration(path_to_weather_folder, station_heights):
    import numpy as np
    import matplotlib.pyplot as plt
    csv_list = import_weather_csv(path_to_weather_folder)
    print(csv_list)
    df_list = []
    for i, df in enumerate(csv_list):
        r = df['SUM_GS200'].multiply(0.0036)
        g = 0
        z = station_heights[i]
        p = 101.3 * ((293 - 0.0065 * z) / 293) ** 5.26
        gamma = (133 / 200000) * p
        t = df['AVG_TA200']
        t_min = df['MIN_TA200']
        wind = df['AVG_WV200']

        t1 = t.multiply(17.27)
        t2 = t.add(237.3)

        t_min1 = t_min.multiply(17.27)
        t_min2 = t_min.add(237.3)

        es = 0.6108 * np.exp(t1 / t2)
        ea = 0.6108 * np.exp(t_min1 / t_min2)

        delta = (4089 * es) / (t2 ** 2)

        ETc = 0.95 * (0.408 * delta * (r - g) + gamma * (900 / (t + 273)) * wind * (es - ea)) / (delta + gamma
                                                                                                 * (1 + 0.34 * wind))

        df['ETc'] = ETc
        df_list.append(df)
    return df_list


def clean_weather_df(path_to_weather_folder, path_to_csv_folder, station_heights):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.stats
    import seaborn as sns
    import scipy.signal as sig
    from scipy.ndimage.filters import gaussian_filter1d

    weather_df = calc_evapotranspiration(path_to_weather_folder, station_heights)

    sentinel_dfs = time_series.import_time_series_csv(path_to_csv_folder)

    r_squared_list = []

    for i, weather_data in enumerate(weather_df):

        weather_data = weather_data.rename({"Tag": "date"}, axis=1)
        weather_data['date'] = pd.to_datetime(weather_data['date'], format='%d.%m.%Y')

        ETc_df = pd.DataFrame(columns=['date', 'ETc'])
        ETc_df['date'] = weather_data['date']
        ETc_df['t_min'] = weather_data['MIN_TA200']
        ETc_df['ETc'] = weather_data['ETc']
        tmp = 0
        for j, sen_df in enumerate(sentinel_dfs[1]):

            sen_df["patches_mean"] = sen_df.mean(axis=1)

            tmp_sen_df = pd.DataFrame(columns=['date', 'patches_mean'])
            tmp_sen_df['date'] = sen_df["date"]
            tmp_sen_df['patches_mean'] = sen_df['patches_mean']

            combine = pd.merge(tmp_sen_df, ETc_df, on='date')
            combine = combine.query("t_min >= 0")
            combine = combine.reset_index(drop=True)

            kernel = 5
            kernel_half = kernel//2

            # Mean - Filter:
            kernel = (1 / float(kernel)) * np.ones(kernel)
            # ATTENTION: np.convolve with mode set to "valid" will cut n//2 values (kernel size = n) off the beginning
            # and end of the time series, bigger kernel sizes produces shorter time series with more data loss.
            patches_filt = np.float32(np.convolve(combine['patches_mean'].to_numpy(), kernel, "valid"))
            # patches_filt = np.append(patches_filt, [-14.5]*2)
            etc_filt = np.float32(np.convolve(combine['ETc'].to_numpy(), kernel, "valid"))
            # etc_filt = np.append(etc_filt, [1]*4)

            # Median - Filter
            # patches_filt = np.float32(sig.medfilt(combine['patches_mean'].to_numpy(), kernel_size=kernel))
            # etc_filt = np.float32(sig.medfilt(combine['ETc'].to_numpy(), kernel_size=kernel))

            # Gauss - Filter:
            # patches_filt = gaussian_filter1d(combine['patches_mean'].to_numpy(), sigma=1.5)
            # etc_filt = gaussian_filter1d(combine['ETc'].to_numpy(), sigma=1.5)

            # use the function regplot to make a scatterplot
            sns.regplot(x=patches_filt, y=etc_filt, fit_reg=False)

            fig, ax1 = plt.subplots()
            fig.set_figheight(9)
            fig.set_figwidth(21)
            color = 'tab:red'
            ax1.set_xlabel('Time', fontsize=20)
            ax1.set_ylabel('Mean Backscatter', color=color, fontsize=20)
            ax1.plot(combine['date'][kernel_half:len(combine['date'])-kernel_half], patches_filt, color=color, linewidth=2)
            ax1.tick_params(axis='y', labelcolor=color)

            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

            color = 'tab:blue'
            ax2.set_ylabel('ETc', color=color, fontsize=20)  # we already handled the x-label with ax1
            ax2.plot(combine['date'][kernel_half:len(combine['date'])-kernel_half], etc_filt, color=color, linewidth=2)
            ax2.tick_params(axis='y', labelcolor=color)

            fig.tight_layout()  # otherwise the right y-label is slightly clipped
            plt.show()

            slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(combine["patches_mean"], y=combine["ETc"])
            r_squared_list.append(r_value ** 2)
            print(j)
            tmp = tmp + 1
            if tmp == 4:
                break

    print(len(r_squared_list))
    print(r_squared_list)
