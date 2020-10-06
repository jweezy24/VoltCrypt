#include "main.h"

int main(){

    vn_swap();

}

void vn_swap(){

    int count = 0;
    int count_nums = 0;
    int value = 0;
    int all_nums_pos = 0;
    char* path = "./Ascii_files/vn.txt";
    int length = 29478362;

    // This loop creates 2 things.
    // The first thing is a sequence of binary numbers in order of the created array.
    // The second thing this loop does is create a dictionary mapping all the original values

    for(int i=0; i<length; i++){
        if (count < 2 && count%2 == 0){
            value += (int)bits[i];
            count+=1;
        }else if(count < 2 && count%2 == 1){
            value -= (int)bits[i];
            count+=1;
        }else{

            //0 = '0' - '0' or '1' - '1'
            //1 = '1' - '0'
            //-1 = '0' - '1'
            if ( value == 1){
                write_to_file("1",path);
            }
            else if ( value == -1){
                write_to_file("0",path);
            }
           value = 0;
           count = 0;

    }

    }

}


int write_to_file(char* str, char* path){
    FILE *fpw;
    //work path
    //fpw = fopen("/opt/sts-2.1.2/sts-2.1.2/data/C_gen_file.txt", "a");
    
    //home
    fpw = fopen(path, "a");
    
    /*Error handling for output file*/
    if (fpw== NULL)
    {
        puts("Issue in opening the Output file");
    }

    fputs(str, fpw);
    fclose(fpw);
    return 0;

}