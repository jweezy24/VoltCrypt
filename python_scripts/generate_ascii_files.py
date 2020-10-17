import sys,os

def main():
    for i in range(2,13):
        print(f"Bit Sequence length {i}")
        #os.system("rm /home/jweezy/Desktop/sts-2.1.2/sts-2.1.2/data/C_gen_file.txt")
        #os.system("touch /home/jweezy/Desktop/sts-2.1.2/sts-2.1.2/data/C_gen_file.txt")
        os.system(f"rm ./Ascii_files/{i}.txt")
        os.system(f"touch ./Ascii_files/{i}.txt")
        print(os.system(f"./alg.o {i} ./Ascii_files/{i}.txt"))
        #os.system(f"cp ~/Desktop/sts-2.1.2/sts-2.1.2/data/C_gen_file.txt ./Ascii_files/{i}.txt")

main()