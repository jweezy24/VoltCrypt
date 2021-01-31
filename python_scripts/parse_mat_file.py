from scipy.io import loadmat
import os

#x = loadmat('./together.mat')
x = loadmat('../Ascii_files/NIST.mat')

print(x)

ave1 = 0
ave2 = 0
count = 0
stream1 = ''
stream2 = ''
tmp1 = []
tmp2 = []
for row in x['NIST']:
    for bit in row:
        with open("../Ascii_files/Aero_key.txt",'a') as f:
            f.write(str(bit))