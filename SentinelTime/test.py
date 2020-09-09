import numpy as np
test1 = "abc"
test2 = [test1]
print(type(test1))
print(type(test2))

test = 1

test += 1

print(test)


test_arr = [[[np.nan, np.nan, np.nan],
             [np.nan, np.nan, np.nan],
             [np.nan, np.nan, np.nan]]]

print(test_arr)
print(test_arr[0])
print(np.nanmean(test_arr[0]))

for j in range(0,3):
    for i in range(0,10):
        print(i)
        if str(np.nanmean(test_arr[0])) == "nan":
            break
        print(i+1)


test_name = 'G:/Processed/test_folder/processed_existing_subset\\S1A__IW___A_20160705T165932_VH_grd_mli_norm_geo_db.tif'
print(test_name[0:test_name.index("S1A")-1])



correct_shape = "[{'type': 'Polygon', 'coordinates': [[(661297.9576407432, 5652850.307079568), (755797.7931697434, 5656841.327960808), (719412.666978868, 5602745.2659186805), (663535.3048818082, 5603920.857014434), (661297.9576407432, 5652850.307079568)]]}]"
