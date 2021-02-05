import os
from subprocess import Popen, PIPE

def part1():
    data_types = ['acc', 'bar', 'gyr', 'hum', 'lux', 'mag', 'tmp']
    block_size = 2
    discard = 1
    
    for i in range(2,13):
        #os.system(f"python3 ./python_scripts/create_all_object_files.py {i} {block_size}")
        # for data_type in data_types: 
        #     os.system(f"./VoltCrypt.o {i} {i-1} {discard} ./Other/sts-2.1.2/sts-2.1.2/data/{data_type}_before{i}.txt ./Other/sts-2.1.2/sts-2.1.2/data/{data_type}_after{i}.txt")
        for discard in range(0,13):
            for (dirpath, dirnames, filenames) in os.walk("./Other/sts-2.1.2/sts-2.1.2/data"):
                for file_ in filenames:
                    if 'before' in file_:
                        new_file_name = file_.replace("before",f"after{i}")
                        new_file_name = f"{discard}{new_file_name}"
                        os.system(f"./VoltCrypt.o {i} {i-1} {discard} ./Other/sts-2.1.2/sts-2.1.2/data/{file_} ./Other/sts-2.1.2/sts-2.1.2/data/{new_file_name}")
                    
                break

def part2():
    path = 'Other/sts-2.1.2/sts-2.1.2/data'
    file_size_example = ''' ./data/acc_after.txt | wc -c'''

     
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file_ in filenames:
            #if "audio_bits_after" in file_ or "audio_bits_before" in file_ :
            path2 = f"{path}/{file_}"
            p1 = Popen(["cat", f"{path2}"], stdout=PIPE,cwd="/home/jweezy/Drive2/Drive2/Code/VoltCrypt")
            p2 = Popen(["wc", "-c"], stdin=p1.stdout, stdout=PIPE,cwd="/home/jweezy/Drive2/Drive2/Code/VoltCrypt" )
            p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
            output = int(p2.communicate()[0].decode('UTF-8'))
            bit_stream_len,bits = get_bit_stream_len(output)
            if bit_stream_len == 0 or bits == 0:
                continue
            print(f"{file_}:\t{output}")
            
            p1 = Popen(["echo", f"0\n./data/{file_}\n1\n0\n{bits}\n0\n" ], stdout=PIPE,cwd="/home/jweezy/Drive2/Drive2/Code/VoltCrypt/Other/sts-2.1.2/sts-2.1.2/")
            p2 = Popen(["./assess", f"{bit_stream_len}"], stdin=p1.stdout, stdout=PIPE,cwd="/home/jweezy/Drive2/Drive2/Code/VoltCrypt/Other/sts-2.1.2/sts-2.1.2/" )
            output = p2.communicate()[0]
            print(output)
            os.system(f"cp Other/sts-2.1.2/sts-2.1.2/experiments/AlgorithmTesting/finalAnalysisReport.txt nist_test_results/{file_}")
           # else:
           #     continue

def clear_out_old_tests():
    path = 'nist_test_results'
    path2 = 'Other/sts-2.1.2/sts-2.1.2/data'

    for (dirpath, dirnames, filenames) in os.walk(path):
        for file_ in filenames:
                if "after" in file_ and "before" not in file_:
                    #print(f"rm {path2}/{file_}")
                    os.system(f"rm {path}/{file_}")
    
    for (dirpath, dirnames, filenames) in os.walk(path2):
        for file_ in filenames:
                if "after" in file_ and "before" not in file_:
                    #print(f"rm {path2}/{file_}")
                    os.system(f"rm {path2}/{file_}")
    
def get_bit_stream_len(length):

    bit_stream_len = int(length/1000) *10
    if bit_stream_len > 1000:
        return (bit_stream_len,100)
    else:
        divisor = 90
        while bit_stream_len < 1000:
            bit_stream_len = int(length/divisor)
            divisor -= 10
            if divisor == 0:
                break
        if divisor == 0:
            return(0,0)
    return(bit_stream_len, divisor)


def main():
    data_types = ['acc', 'bar', 'gyr', 'hum', 'lux', 'mag', 'tmp']
    command_example = '''python3 -c 'print("0\n./data/acc_after.txt\n1\n0\n100\n0\n")' | ./assess 1080'''
    file_size_example = ''' ./data/acc_after.txt | wc -c'''
    # try:  
    #     os.system("rm ./Other/sts-2.1.2/sts-2.1.2/data/* &&  rm ./nist_test_results/*" )
    # except:
    #     print(e)
    #print("HERE")
    clear_out_old_tests()
    part1()
    part2()

    #single_test("../Ascii_files/key1.txt")


main()