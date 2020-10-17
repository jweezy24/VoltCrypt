import os,sys
import numpy as np
import matplotlib.pyplot as plt
import subprocess


def find_biggest_change(data):
    max_change = [0 , 0, 0, 0]
    max_change_discard = ['', '', '' , '']
    for ele in data.keys():
        data_type = swtich_satement(ele)
        if data_type:
            if 'raw' in data_type and float(data[ele]) >= float(max_change[0]): 
                max_change[0] = float(data[ele])
                max_change_discard[0] = ele[1:]
                
            elif 'Car' in data_type  and float(data[ele]) >= float(max_change[1]):
                max_change[1] = float(data[ele])
                max_change_discard[1] = ele[1:]
               
            elif 'Office' in data_type and float(data[ele]) >= float(max_change[2]):
                max_change[2] = float(data[ele])
                max_change_discard[2] = ele[1:]
               
            elif 'Mobile' in data_type and float(data[ele]) >= float(max_change[3]):
                max_change[3] = float(data[ele])
                max_change_discard[3] = ele[1:]
               

    return (max_change, max_change_discard)

def swtich_satement(data_type):
    
    if 'before' in data_type.lower():
        return None
    elif 'raw' in data_type.lower():
        return 'raw'
    elif 'office' in data_type.lower():
        return 'Office'
    elif 'mobile' in data_type.lower():
        return 'Mobile'
    elif 'car' in data_type.lower():
        return 'Car'


def parse_files():
    data_to_file = {}
    for (dirpath, dirnames, filenames) in os.walk('./nist_test_results'):
        for file_name in filenames:
            with open(f'{dirpath}/{file_name}', 'r') as f:
                all_data = []
                for line in f:
                    if '/' in line and '<' not in line:
                        split_line = line.split(' ')
                        data = []
                        for ele in split_line:
                            if ele != '':
                                data.append(ele)
                        all_data.append(data)
                data_to_file[file_name] = all_data

    return data_to_file

def examine_data(data):
    failure_rate = {}
    for key in data:
        passes = 0
        fails = 0
        for ele in data.get(key):
            stars = [i for i, e in enumerate(ele) if e == '*']
            if 12 in stars or 13 in stars or 11 in stars:
                fails +=1
            else:
                passes += 1
        failure_rate[key] = (passes/(passes+fails))
    #print(failure_rate)
    
    return failure_rate

def create_bar_graph(data):
    #This first loop maps a data source to a list iter
    #print(data)
    #print(find_biggest_change(data))
    font = {'family' : 'normal',
            'size'   : 10}

    plt.rc('font', **font)
    plt.rc('text', usetex=True)
    stuff = find_biggest_change(data)
    x = {}
    count = 0
    for ele in stuff[1]:
        tmp = ele.split("_")[0]
        tmp = tmp.lower()
        if tmp not in x.keys():
            #Arbitrary setup
            #x.update({tmp: count})

            #fixed setup
            if 'raw' in tmp:
                x.update( {tmp : 0} )
            elif 'car' in tmp:
                x.update( {tmp : 1} )
            elif 'office' in tmp:
                x.update( {tmp : 2} )
            elif 'mobile' in tmp:
                x.update( {tmp : 3} )
            
            count+=1

    y_axises = []
    for i in range(0,2):
        tmp = []
        for i in range(0, 4):
            tmp.append(0)    
        y_axises.append(tmp)

    print(y_axises)
    
    y_axises[1] = find_biggest_change(data)[0]
    print(find_biggest_change(data)[1])
    for ele in data.keys():
        tmp = ele.split("_")[0]
        tmp = tmp.lower()
        #print(loc)
        if 'before' in ele and tmp in x.keys():
            loc = x[tmp]
            y_axises[0][loc] = data[ele]
    

    # y = [4, 9, 2]
    # z = [1, 2, 3]
    # k = [11, 12, 13]

    ax = plt.subplot(111)
    x_vals = ['Voltkey', 'Car', 'Office', 'Mobile']
    count = 0
    separator = 0.3

    eles = np.arange(len(x_vals))
    plt.xticks( eles+(separator/2), x_vals, rotation='horizontal')
    for i in y_axises:
        if count == 0:
            ax.bar(eles+separator, i, color='r', align='center', width=separator,label='Pre-Algorithm', FaceColor='#FEBD18', EdgeColor='k')
            count+=1
        else:
            ax.bar(eles, i, color='b', align='center', width=separator, label='Post-Algorithm', FaceColor='#922247', EdgeColor='k')

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    ax.set_title("NIST Pass Rate for Pre-algorithm vs Post-algorithm")
    ax.set_ylabel('Test Pass Rate')
    ax.set_xlabel('Datasets')
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    # ax.bar(x-0.2, y, width=0.2, color='b', align='center')
    # ax.bar(x, z, width=0.2, color='g', align='center')
    # ax.bar(x+0.2, k, width=0.2, color='r', align='center')
    # ax.xaxis_date()

    plt.savefig("./figures/NIST_Dataset_Comparison.pdf")


if __name__ == '__main__':
    data = parse_files()
    failure_data = examine_data(data)
    create_bar_graph(failure_data)

