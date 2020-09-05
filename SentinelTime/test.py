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