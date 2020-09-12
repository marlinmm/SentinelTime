
test1 = "VV"
test2 = "VV"
test3 = ","
for i in range(0, 20):
    test2 = test2 + str(i) + test3 + test1
    #print(test2)

print(test2[0:len(test2)-3])
