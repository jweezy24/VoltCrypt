import os,sys
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import matplotlib.image as mpimg
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition

def find_biggest_change(data):
    max_change = [0 , 0, 0, 0]
    max_change_discard = ['', '', '' , '']
    for ele in data.keys():
        data_type = swtich_satement(ele)
        if data_type:
            try:
                if 'raw' in data_type and float(data[ele]) >= float(max_change[0]): 
                    max_change[0] = float(data[ele])
                    max_change_discard[0] = ele
                    
                elif 'Office' in data_type and float(data[ele]) >= float(max_change[1]):
                    max_change[1] = float(data[ele])
                    max_change_discard[1] = ele

                elif 'Mobile' in data_type and float(data[ele]) >= float(max_change[2]):
                    max_change[2] = float(data[ele])
                    max_change_discard[2] = ele

                elif 'Car' in data_type and float(data[ele]) >= float(max_change[2]):
                    max_change[3] = float(data[ele])
                    max_change_discard[3] = ele
            except:
                continue
    # print(max_change_discard)
    # exit(0)
               

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
        nonoverlapping = 126
        nonoverlapping_fails = 0    
        for ele in data.get(key):
            stars = [i for i, e in enumerate(ele) if '*' in e]
            if (11 in stars and 13 in stars) and 'NonOverlappingTemplate\n' not in ele[-1]:
                fails +=1
            elif 'NonOverlappingTemplate\n' in ele[-1] and ( 11 in stars and 13 in stars):
                nonoverlapping_fails += 1
            elif 'NonOverlappingTemplate\n' in ele[-1]:
                continue
            else:
                passes += 1
        
        if nonoverlapping_fails/nonoverlapping >= .5:
            fails += 1
        else:
            passes += 1

        try:        
            failure_rate[key] = (passes/(passes+fails))
        except:
            failure_rate[key] = "NA"
    #print(failure_rate)
    
    return failure_rate

def find_number_in_string(string):
    for letter in string:
        if ord(letter) >= 48 and ord(letter) <= 57:
            return letter

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
                x.update( {tmp[1:] : 0} )
            elif 'office' in tmp:
                x.update( {tmp[1:] : 1} )
            elif 'mobile' in tmp:
                x.update( {tmp[1:] : 2} )
            elif 'car' in tmp:
                x.update( {tmp[1:] : 3} )
            
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
        if 'before' in ele and tmp in x.keys():
            # print(tmp)
            # print(data[ele])
            # print(ele)
            # exit(0)
            if tmp != 'raw' and 'SH' in ele:
                # print(tmp)
                # print(data[ele])
                # print(x)
                # exit(0) 
                loc = x[tmp]

                y_axises[0][loc] = data[ele]
            if tmp == 'raw':
                loc = x[tmp]
                y_axises[0][loc] = data[ele]

    # y = [4, 9, 2]
    # z = [1, 2, 3]
    # k = [11, 12, 13]
    plt.figure(figsize=(6,2.5))
    ax = plt.subplot(111)
    x_vals = ['Voltkey', 'Office', 'Mobile', 'Car']
    count = 0
    separator = 0.3

    eles = np.arange(len(x_vals))
    plt.xticks( eles+(separator/2), x_vals, rotation='horizontal')
    for i in y_axises:
        if count == 0:
            ax.bar(eles+separator, i, color='r', align='center', width=separator,label='Pre-VoltCrypt', FaceColor='#FEBD18', EdgeColor='k')
            count+=1
        else:
            ax.bar(eles, i, color='b', align='center', width=separator, label='Post-VoltCrypt', FaceColor='#922247', EdgeColor='k')

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    ax.set_title("NIST Pass Rate for Pre-VoltCrypt vs Post-VoltCrypt")
    ax.set_ylabel('Test Pass Rate')
    ax.set_xlabel('Datasets')
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    
    # ax.bar(x-0.2, y, width=0.2, color='b', align='center')
    # ax.bar(x, z, width=0.2, color='g', align='center')
    # ax.bar(x+0.2, k, width=0.2, color='r', align='center')
    # ax.xaxis_date()

    plt.savefig("./NIST_Dataset_Comparison.pdf")


def new_figure_6(data):
    best_error_rates = []
    best_for_all_data = []
    font = {'family' : 'normal',
            'size'   : 14}

    plt.rc('font', **font)
    plt.rc('text', usetex=True)
    for i in range(0,10):
        best_error_rates.append(i)
    
    for i in range(0,4):
        best_for_all_data.append([1,2,3,4,5,6,7,8,9])
    
    #inner first array = Failure rates for bit stream
    #im_array = [[[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7],[0,0,0,0,0,0,0,0,0]],[[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7],[]],[[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7],[0,0,0,0,0,0,0,0,0]],[[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7],[0,0,0,0,0,0,0,0,0]]]
    im_array = []
    for i in range(0,4):
        tmp_holder = []
        for j in range(0,8):
            row = []
            for k in range(0,8):
                row.append(0)
            tmp_holder.append(row)
        im_array.append(tmp_holder)
    for key in data.keys():

        if data[key] != 'NA' and 'before' not in key:
            var_array = key.split('_')
            #print(var_array)
            bit_seq_len = int(find_number_in_string(var_array[-1]))
            discard_len = int(var_array[0][0])
            tmp = swtich_satement(key).lower()
            failure_rate = float(data[key])
            if bit_seq_len < 10 and bit_seq_len > 1:
                # if 'S' in key or 'raw' in key:
                if 'raw' in tmp:
                    if im_array[0][bit_seq_len-2][discard_len] < failure_rate:
                        im_array[0][bit_seq_len-2][discard_len] = failure_rate

                elif 'car' in tmp:
                    if im_array[3][bit_seq_len-2][discard_len] < failure_rate:
                        im_array[3][bit_seq_len-2][discard_len] = failure_rate

                elif 'office' in tmp:
                    if im_array[1][bit_seq_len-2][discard_len] < failure_rate:
                        im_array[1][bit_seq_len-2][discard_len] = failure_rate
                    
                elif 'mobile' in tmp:
                    if im_array[2][bit_seq_len-2][discard_len] < failure_rate:
                        im_array[2][bit_seq_len-2][discard_len] = failure_rate
    
    fig = plt.figure()
    # ax = plt.subplot(111)
    # axs = plt.subplots(1,3)
    x_axis = best_error_rates
    count = 0
    separator = 0.3
    #print(im_array)

    # eles = np.arange(len(x_vals))
    # plt.xticks( eles+(separator/2), x_vals, rotation='horizontal')
    # for line in best_for_all_data:
    #     if count == 0:
    #         ax.plot(x_axis, line, label="Electricity")
    #     elif count == 2:
    #         ax.plot(x_axis, line, label="Office")
    #     elif count == 3:
    #         ax.plot(x_axis, line, label="Mobile")
    #     count+=1
    
    count = 0
    extent= [1, 7, 1, 9]
    x_labels = np.arange(1,9,2)
    ax = None
    for line in best_for_all_data:
        if count == 0:
            ax = fig.add_subplot(1, 5, 1)
            tmp = np.array(im_array[0])
            img = ax.imshow(tmp,  interpolation='nearest', vmin=0, vmax=1, cmap='jet')
            
            ax.set_title("Voltkey")
            plt.grid(True) 
        if count == 1:
            bx = fig.add_subplot(1, 5, 2)
            tmp = np.array(im_array[1])
            bx.set_title("Office Data")
            img = bx.imshow(tmp,  interpolation='nearest', vmin=0, vmax=1, cmap='jet', extent=extent)
            bx.set_xticks(x_labels)
            bx.set_aspect(1)
        
            plt.grid(True)
        if count == 2:
            cx = fig.add_subplot(1, 5, 3)
            tmp = np.array(im_array[2])
            img = cx.imshow(tmp,  interpolation='nearest', vmin=0, vmax=1, cmap='jet', extent=extent)
            cx.set_aspect(1)
            cx.set_xticks(x_labels)
            cx.set_title("Mobile Data")
            plt.grid(True)
        
        if count == 3:
            cx = fig.add_subplot(1, 5, 4)
            tmp = np.array(im_array[3])
            img3 = cx.imshow(tmp,  interpolation='nearest', vmin=0, vmax=1, cmap='jet', extent=extent)
            cx.set_aspect(1)
            cx.set_xticks(x_labels)
            cx.set_title("Car Data")
            plt.grid(True)

        count+=1
    ip = InsetPosition(cx, [1.05,0,0.05,1])   
    cax = fig.add_subplot(1, 5, 5)
    cax.set_axes_locator(ip)
    fig.colorbar(img3, cax=cax)
    # handles, labels = ax.get_legend_handles_labels()
    fig.suptitle("Discard Amount vs Bit Sequence Length")
    fig.text(0.5, 0.2, 'Bit Sequence Length', ha='center', va='center')
    fig.text(0.06, 0.6, 'Discard Amount', ha='center', va='center', rotation='vertical')
    plt.subplots_adjust(left=0.1, right=1.1, top=1.0, bottom=0.18   )

    plt.savefig("2D_block_figure.pdf", bbox_inches='tight')
            
    print(best_for_all_data)

def get_all_file_sizes():
    font = {'family' : 'normal',
            'size'   : 14}

    plt.rc('font', **font)
    plt.rc('text', usetex=True)
    path = '../Other/sts-2.1.2/sts-2.1.2/data'
    before_sizes = {}
    after_size = {}
    compared_sizes = {}
    for (dirpath, dirnames, filenames) in os.walk('../Other/sts-2.1.2/sts-2.1.2/data'):
        for file_name in filenames:
            if 'before' in file_name:
                entry = file_name.split('_')[0]
                count = 0
                with open(f"{path}/{file_name}") as f:
                    for line in f:
                        for bit in line:
                            count+=1
                before_sizes.update({entry: count})
    
    for (dirpath, dirnames, filenames) in os.walk('../Other/sts-2.1.2/sts-2.1.2/data'):
        for file_name in filenames:
            if 'after' in file_name:
                front = (file_name.split('_')[0])
                entry = front+file_name.split('_')[-1].replace('.txt', '')[-1]
                count = 0
                with open(f"{path}/{file_name}") as f:
                    for line in f:
                        for bit in line:
                            count+=1
                after_size.update({entry : count})

    percentage_lost = {}
    im_array = []
    extent= [0, 6, 0, 7]
    for i in range(0,4):
        tmp_holder = []
        for j in range(0,8):
            row = []
            for k in range(0,7):
                row.append(0)
            tmp_holder.append(row)
        im_array.append(tmp_holder)
    #print(im_array)
    for ele in after_size.keys():
        dataset = ele[1: (len(ele)-1)]
        x = int(ele[0])
        y = int(ele[-1])
        #print(ele)
        #print(y) 
        for data in before_sizes.keys():
            if dataset in data and y > 1 and y != 9:
                print(f"{x}\t{y}")
                percent = after_size[ele]/before_sizes[data]
                check = swtich_satement(ele).lower()
                if 'raw' in check:
                    #print(f"{ele}\t{percent}")
                    im_array[0][x][y-2] = percent
                elif 'office' in check:
                    im_array[1][x][y-2] = percent
                if 'mobile' in check:
                    im_array[2][x][y-2] = percent
                if 'car' in check:
                    im_array[3][x][y-2] = percent
                break
        count = 0

    fig = plt.figure()
    x_labels = np.arange(2,7,2)
    y_labels = np.arange(0,8,2)
    print(im_array)
    cx = None
    count = 0
    img3 = None
    for i in range(0,4):
        if count == 0:
            ax = fig.add_subplot(1, 5, 1)
            tmp = np.array(im_array[0])
            #print(im_array[0])
            img3 = ax.imshow(tmp,  interpolation='nearest', vmin=0, vmax=1, cmap='jet', extent=extent)
            ax.set_title("VoltKey")
            ax.set_xticks(x_labels)
            ax.set_yticks(y_labels)
            plt.grid(True)
            
        if count == 1:
            bx = fig.add_subplot(1, 5, 2)
            tmp = np.array(im_array[1])
            bx.set_title("Office Data")
            img = bx.imshow(tmp,  interpolation='nearest', vmin=0, vmax=1, cmap='jet', extent=extent)
            bx.set_xticks(x_labels)
            bx.set_aspect(1)
            bx.set_yticks([])
        
            plt.grid(True)
        if count == 2:
            cx = fig.add_subplot(1, 5, 3)
            tmp = np.array(im_array[2])
            img = cx.imshow(tmp,  interpolation='nearest', vmin=0, vmax=1, cmap='jet', extent=extent)
            cx.set_aspect(1)
            cx.set_xticks(x_labels)
            cx.set_yticks([])
            cx.set_title("Mobile Data")
            plt.grid(True)
        
        if count == 3:
            cx = fig.add_subplot(1, 5, 4)
            tmp = np.array(im_array[3])
            img3 = cx.imshow(tmp,  interpolation='nearest', vmin=0, vmax=1, cmap='jet', extent=extent)
            cx.set_aspect(1)
            cx.set_xticks(x_labels)
            cx.set_yticks([])
            cx.set_title("Car Data")
            plt.grid(True)

        count+=1
    ip = InsetPosition(cx, [1.05,0,0.05,1])   
    cax = fig.add_subplot(1, 5, 5)
    cax.set_axes_locator(ip)
    fig.colorbar(img3, cax=cax)
    # handles, labels = ax.get_legend_handles_labels()
    #fig.suptitle("Data Rentention")
    
    fig.text(0.5, 0.35, 'Bit Sequence Length', ha='center', va='center')
    fig.text(0.01, 0.6, 'Discard Amount', ha='center', va='center', rotation='vertical')

    # fig.text(0.35, 0.2, 'Bit Sequence Length', ha='center', va='center')
    # fig.text(0.02, 0.6, 'Discard Amount', ha='center', va='center', rotation='vertical')

    plt.subplots_adjust(left=0.1, right=1.1, top=1.0, bottom=0.18   )
    plt.savefig("data_retention_color_graph.pdf", bbox_inches='tight')

def quick_shit():
    y_axis_plot_1_Moon = []
    for i in range(2, 9):
        y_axis_plot_1_Moon.append(0)
    
    path = '../Other/sts-2.1.2/sts-2.1.2/data'
    total = 0
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file_name in filenames:
            if 'before' in file_name and 'raw' in file_name:
                with open(f"{path}/{file_name}") as f:
                    for line in f:
                        for bit in line:
                            total+=1
    remove = ['10','11', '12']
    check = True
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file_name in filenames:
            if '2raw' in file_name:
                check = True
                for iter in remove:
                    if iter in file_name:
                        check = False
                if check:
                    index = int(file_name.replace(".txt", '')[-1])
                    count = 0
                    if index < 9:
                        with open(f"{path}/{file_name}") as f:
                            for line in f:
                                for bit in line:
                                    count+=1
                        print(count/total)
                        print(index)
                        y_axis_plot_1_Moon[index-2] = count/total
    print(y_axis_plot_1_Moon)
   

    x_axis_plot_2_VN = [ 2,  3,  4,  5,  6,  7,  8]
    y_axis_plot_2_VN = [0.9074074074074074, 0.9074074074074074, 0.9074074074074074, 0.9074074074074074, 0.9074074074074074, 0.9074074074074074, 0.9074074074074074]

    x_axis_plot_2_Moon = [2, 3, 4, 5, 6, 7, 8]
    y_axis_plot_2_Moon = [0.7037037037037037, 0.9074074074074074, 0.9148936170212766, 0.9574468085106383, 0.9202127659574468, 0.9946808510638298, 0.9787234042553191 ]

    #FIGURE DATA REMAINING
    x_axis_plot_1_VN = [2, 3, 4, 5, 6, 7, 8]
    y_axis_plot_1_VN = [0.16998559824999773, 0.16998559824999773, 0.16998559824999773, 0.16998559824999773, 0.16998559824999773, 0.16998559824999773, 0.16998559824999773]

    x_axis_plot_1_Moon = [2, 3, 4, 5, 6, 7, 8]
    #y_axis_plot_1_Moon = [0.5000000169615955, 0.5000000169615955, 0.3333333446410636, 0.25000000848079773, 0.20000000678463817, 0.1666666723205318, 0.14285713801097272]


    #FIGURE 3 TIME GRAPH
    x_axis = [2,3,4,5,6,7,8,9,10,11]
    y_axis = [.340625, .396875, .40625, .43125, .4625, .48125, .53125, .54375, .56875, .6]


    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20,6), constrained_layout=True)

    ax1.plot(x_axis_plot_1_Moon, y_axis_plot_1_Moon, label="Moonshine")
    ax1.plot(x_axis_plot_1_VN, y_axis_plot_1_VN, label="Von Neumann")

    ax2.plot(x_axis_plot_2_Moon, y_axis_plot_2_Moon, label="Moonshine")
    ax2.plot(x_axis_plot_2_VN, y_axis_plot_2_VN, label="Von Neumann")

    ax3.plot(x_axis, y_axis)
 
    plt.tight_layout()
    plt.show()


def histogram():
    dataset = "officeSH"

    for (dirpath, dirnames, filenames) in os.walk(path):
         for file_name in filenames:
             if dataset in file_name and "before" in file_name:
                 


    

if __name__ == '__main__':
    data = parse_files()
    failure_data = examine_data(data)
    #create_bar_graph(failure_data)
    new_figure_6(failure_data)
    #print(failure_data)
    #get_all_file_sizes()
    #quick_shit()

#[[0.5000000169615955, 0.5000000169615955, 0.3333333446410637, 0.25000000848079773, 0.20000000678463814, 0.16666667232053178, 0.14285713801097277, 0.1250000042403988], [0.4966800560370406, 0.4966800560370406, 0.33333331071787276, 0.29798110539328193, 0.19999997286144733, 0.21286154361577592, 0.18626420147742961, 0.124999970317208], [0.4948680487947107, 0.4948680487947107, 0.3958271897021134, 0.329975830744174, 0.2827075279190405, 0.24743538132499165, 0.219944841570048, 0.19790965976091135], [0.4924345686949535, 0.4924345686949535, 0.4104196234261208, 0.3517481756701586, 0.3078817243524309, 0.2735897544364664, 0.2462886417795509, 0.22380302784154305], [0.48588206690881264, 0.48588206690881264, 0.4164037082254137, 0.3643189568320272, 0.3238012672279349, 0.29150856056811036, 0.26483048123540387, 0.24293211165519768], [0.4791674461933244, 0.4791674461933244, 0.419354890141612, 0.3728499608814724, 0.3355336028033311, 0.304779855622221, 0.279608135581767, 0.25795862653005885], [0.47382620586173063, 0.47382620586173063, 0.42147905858667367, 0.37909162446932676, 0.3442450782284048, 0.3158155106259477, 0.29141103139425095, 0.2706527184908767], [0.46974697607828175, 0.46974697607828175, 0.4224441394448042, 0.3838100689390478, 0.35209436183337073, 0.3247917565560552, 0.3017233761214456, 0.28174220959857366], [0.10228018459236488, 0.10228018459236488, 0.09294801654325469, 0.08333330223707502, 0.0769231082367916, 0.0730349338645343, 0.06666663500502179, 0.06250022262094035]]