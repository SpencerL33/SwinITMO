import utils.utils_image as util
import os
import stat
import numpy as np

def remove_baby(path_lst):
    path_lst[:] = [p for p in path_lst if os.stat(p)[stat.ST_SIZE] > 5000000]
    return path_lst


def match_files(path_lst1, path_lst2):
    lst1 = [os.path.basename(p1) for p1 in path_lst1]
    lst2 = [os.path.basename(p2) for p2 in path_lst2]
    paths1 = [p1 for p1 in path_lst1 if os.path.basename(p1) in lst2]
    paths2 = [p2 for p2 in path_lst2 if os.path.basename(p2) in lst1]
    #lst2[:] = [f2 for f2 in lst2 if f2 in lst1]
    return paths1, paths2


def match_files2(path_lst1, path_lst2):
    lst1 = [os.path.basename(p1)[:-7] for p1 in path_lst1]
    lst2 = [os.path.basename(p2)[:-7] for p2 in path_lst2 if os.path.basename(p2) in lst1]
    lst1[:] = [f1 for f1 in lst1 if f1 in lst2]
    #lst2[:] = [f2 for f2 in lst2 if f2 in lst1]
    return lst1, lst2


paths_H1=None
paths_H2=None
paths_L1=None
paths_L2=None


#test = "/lustre06/project/6003167/SharedProject4Kto8K_SDRfixedReinhard/4K_Stelios/c06_Drama_standingup_4K/001_c06_Drama_standingup_4K_PQ.exr"

paths_H1 = util.get_image_paths("/lustre06/project/6003167/Share_4K8K/4K_PQ_EXR")
paths_H2 = util.get_image_paths("/lustre06/project/6003167/shared_itmo_fixed/Garden/HDR")
paths_L1 = util.get_image_paths("/lustre06/project/6003167/SharedProject4Kto8K_SDRfixedReinhard/4K_Stelios")
paths_L2 = util.get_image_paths("/lustre06/project/6003167/shared_itmo_fixed/Garden/SDR")

#test_H = util.get_image_paths("/lustre06/project/6003167/ECE_571_2023/iTMO/Test_data_from_teaching_team/HDR/")
#test_L = util.get_image_paths("/lustre06/project/6003167/ECE_571_2023/iTMO/Test_data_from_teaching_team/SDR/")

#print("Number of images in H1 before trim = "+str(len(paths_H1)))
#print("Number of images in H2 before trim = "+str(len(paths_H2)))
#print("Number of images in L1 before trim = "+str(len(paths_L1)))
#print("Number of images in L2 before trim = "+str(len(paths_L2)))

paths_L1 = remove_baby(paths_L1)
paths_L2 = remove_baby(paths_L2)

#print(paths_H1[10])
#os.path.basename(paths_H1[10])
#print(paths_H1[10])

#print(os.path.basename(paths_H2[50])[:-7])
#print(os.path.basename(paths_L2[50])[:-7])

#paths_H1[:] = [h for h in paths_H1 if h in 
#full_name = os.path.basename(file_path)
paths_H1, paths_L1 = match_files(paths_H1, paths_L1)
paths_H2, paths_L2 = match_files2(paths_H2, paths_L2)

#print("Number of images in H1 = "+str(len(paths_H1)))
#print("Number of images in H2 = "+str(len(paths_H2)))
#print("Number of images in L1 = "+str(len(paths_L1)))
#print("Number of images in L2 = "+str(len(paths_L2)))


print("Number of images in test_H = "+str(len(test_H)))
print("Number of images in test_L = "+str(len(test_L)))

test_H, test_L = match_files(test_H, test_L)

print("Number of images in test_H = "+str(len(test_H)))
print("Number of images in test_L = "+str(len(test_L)))

paths_H = paths_H1 + paths_H2
paths_L = paths_L1 + paths_L2

# tests = np.array(tuple(zip(test_H, test_L)))
# np.random.shuffle(tests)
# tests = list(map(tuple, tests))

paths = np.array(tuple(zip(paths_H, paths_L)))
np.random.shuffle(paths)

#print(paths.shape)
paths.reshape(-1,2)
#print(paths.shape)

paths = list(map(tuple, paths))

#print(round(0.9*(len(paths))))
#print(round(0.9*(len(paths)))+1)
#data_split = round(0.9*(len(paths)))+1

#print(tests[1])
#print(tests[-1])

with open('iTMO_dirs.txt', 'w') as fp:
    fp.write('\n'.join('%s,%s' % x for x in tests))

#with open('test_itmo_dirs.txt', 'w') as fp:
#    fp.write('\n'.join('%s,%s' % x for x in paths[data_split+1:]))

#print("Sample path in H1: " + str(paths_H1[0]))
#print("Size of sample image: " + str(os.stat(test)[stat.ST_SIZE]))



