import os,sys

def bits_log_parse():
    bits = []
    count = 0
    with open('../bits.log', 'r') as f:
        for line in f:
            if line[0] == '0' or line[0] == '1':
                bits.append(line[0])
                count+=1
    #print(len(bits))
    return bits

def bit_stream_parse(filepath):
    bits = []
    with open('../bits.log', 'r') as f:
        for line in f:
            for bit in line:
                if bit == '1' or bit == '0':
                    bits.append(bit)
    return bits

def create_file(bits):
    with open('./simulated_input.c', 'a') as f:
        f.write('char bits[] = {')
        for bit in range(0,len(bits)):
            if bit < len(bits)-2:
                holder = bits[bit].replace('\n','')
                if holder == '':
                    continue
                if holder == '0':
                    f.write(f"'{holder}',")
                else:
                    f.write(f"'{holder}',")
            elif bit < len(bits)-1:
                holder = bits[bit].replace('\n','')
                if holder == '':
                    continue
                if holder == '0':
                    f.write(f"'{holder}'")
                else:
                    f.write(f"'{holder}'")
                f.write('};\n')


if __name__ == "__main__":
    bits = bits_log_parse()
    create_file(bits)
        
