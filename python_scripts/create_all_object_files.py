import os

data_types = ['acc', 'bar', 'gry', 'hum', 'lux', ]


'''
    This function parses a file from the ZIA dataset folder and converts it into a list of numbers in a string format.

    Input:
    filepath = str();       This is the path to a txt file which holds all of the data we want to parse.

    Output:
    data = [];              data holds the numeric raw values gathered from the file given

'''
def parse_car_data(filepath):
    data = []
    with open(filepath,"r") as f:
        for line in f:
            raws = line.split(' ')
            try:
                data.append(float(raws[1]))
            except Exception as e:
                print(e)
    return data

'''
    This function parses the raw bit stream from bits.log

    Input:
    filepath = str();       This is the path to a txt file which holds all of the data we want to parse.

    Output:
    data = [];              data holds the numeric raw values gathered from the file given

'''
def parse_raw_bit_stream(filepath, binary_len):
    data = []
    count = 0
    total_bits = 1000000
    with open(filepath,"r") as f:
        binary = ''
        bit = ''
        for line in f:
            
            if count%binary_len == 0 and count > 0:
                binary = bit
                data.append(binary)
                bit = ''

            if '0' in line:
                bit += '0'
            elif '1' in line:
                bit+='1'
            count+=1

            if count > total_bits:
                break


    return data
    
''' 
    This function will take the parsed data set and convert it to a bit stream
    
    Input:
    data = [];              Data will be the parsed stream of data from the file, we assume that the type in the list is a string
    ele_size = int();       This is the element length, in other words, this is the length of the original bit stream
    block_s = int();       This is the element length, in other words, this is the length of the original bit stream  

    Output:
    streams = []        This list will be a list of bit streams where each element is a binary number.
'''   
def data_to_bit_stream(data,ele_size,block_size):
    #initalization of locals
    average = 0
    highest_block_mean = []
    streams = []
    ele = ''
    bin_num = ''
    count = 0
    count_raws = 0
    count_block = 0 
    local_delta = -1000

    #This is the average over the entire stream of numbers
    for item in data:
        num = float(item)
        average+=num
    average = average/len(data)
    
    #grabs the highest difference from the mean
    for item in data:
        delta = abs(average - float(item))
        if count_block%block_size == 0 and count_block >0:
            highest_block_mean.append(local_delta)
            local_delta = -1000
        elif delta > local_delta:
            local_delta = delta
        
        count_block+=1
    #This function makes the bit stream
    for i in highest_block_mean:
        num = float(i)
        if num >= average:
            ele = '1'
        else:
            ele = '0'
        
        if count%ele_size == 0 and count > 0:
            streams.append(bin_num)
            bin_num = ''
            bin_num += ele    
        else:
            bin_num += ele
        
        count += 1

    return streams

def create_file(bits, data_type):
    with open(f'../src/simulated_input_{data_type}.c', 'w+') as f:
        f.write('char' + f' {data_type}[] =' + ' { ')
        for binary in range(0,len(bits)):
            for bit in range(0, len(bits[binary])):
                if binary < len(bits) -1 or bit < len(bits[binary]) - 1:
                    f.write(f"'{bits[binary][bit]}', ")
                else:
                    f.write(f"'{bits[binary][bit]}' " + "};\n" )
                

''' 
    This function will write a stream of data as binary to a txt file to be used by the nist tests

    Input:
    nums = [];          A list of strings that are binary numbers
    filepath = str();   A string that is the file path for the file to be created.

'''
def create_nist_test_file(nums, filepath):
    with open(filepath, 'w+') as f:
        for num in nums:
            if num != -1:
                f.write(num)




def main():
    bit_stream_size = 9
    block_size = 2
    data_type = "acc"
    data = parse_car_data(f"/home/jweezy/Drive2/Drive2/Code/AEP_Prototype/ZIADatasets/CarDataset/Sensor-01/sensors/{data_type}Data")
    streams = data_to_bit_stream(data, bit_stream_size, block_size)
    create_nist_test_file(streams, f"../../sts-2.1.2/sts-2.1.2/data/{data_type}_before.txt")
    create_file(streams, data_type)

main()