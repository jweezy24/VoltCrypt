import os
import numpy as np
import database_communication as db


def create_ascii_file():
    for i in range(73, 379):
        data1,data2 = db.get_raws_single_instance(i)
        #os.remove("../Ascii_files/key1.txt")

        #the first entry in the dataset is a test value so I remove it
        buff1 = [key[1] for key in data1]
        buff2 = [key[1] for key in data2]
        #print(buff1)
        current_alg(buff1,buff2)
        
        
def current_alg(buffer_values1,buffer_values2):
    size = len(buffer_values1)
    tmp_list1 = []
    tmp_list2 = []
    x_axis = []
    y_axis = []

    ave1 = 0
    ave2 = 0
    #print(size)

    buff_arr1 = np.array(buffer_values1)
    buff_arr2 = np.array(buffer_values2)
    
    count = 0

    key_coeffs1 = []
    key_coeffs2 = []
    
    sum_1 = 0
    sum_2 = 0
    k = 10
    for i in range(0, size, k):
        tmp_list1 = []
        tmp_list2 = []
        if i < size-k+1:
            for j in range(i, i+k):
                tmp_list1.append(buffer_values1[j])
                sum_1 += buffer_values1[j]

            for j in range(i, i+k):
                tmp_list2.append(buffer_values2[j])
                sum_2 += buffer_values2[j]
            arr1 = np.array(tmp_list1)
            arr2 = np.array(tmp_list2)

            # std1 = np.std(arr1)
            # std2 = np.std(arr2)
            # print(arr1)
            # print(arr2)
            num1 = sum_1/len(tmp_list1)
            num2 = sum_2/len(tmp_list1)

            max1 = max(np.max(arr1), abs(np.min(arr1)))
            max2 = max(np.max(arr2), abs(np.min(arr2)))
            

            # print(f"STD1 = {std1}\t Average1 = {num1}")
            # print(f"STD2 = {std2}\t Average2 = {num2}")

            if num1 >= max1:
                key_coeffs1.append('1')
            else:
                key_coeffs1.append('0')
            
            if num2 >= max2:
                key_coeffs2.append('1')
            else:
                key_coeffs2.append('0')


    with open("../Ascii_files/key1.txt", "a") as f:
        f.write(''.join(key_coeffs1))
    with open("../Ascii_files/key2.txt", "a") as f:
        f.write(''.join(key_coeffs2))
        


if __name__ == "__main__":
    create_ascii_file()