#include <main.h>

//#define DEBUG 



int main(int argc, char *argv[]){
    int j;
    
    cmd* vals = parse_commandline(argc, argv);

    int count = vals->bl;
    int bl = vals->bl;
    int sl = vals->sl;
    int discard = vals->discard;
    int total_before_mapping = pow_jack(2,bl);
    int total_after_mapping = pow_jack(2,sl);

    int list_ints_before[256] = {};
    int list_ints_after[128] = {};
    int judges_list[256] = {};
    int ordering_list_before[256] ={};
    int ordering_list_after[128] = {};

    char *path = vals->filepath;
    char *outfile = vals->outfile; 

    char* bits = create_bits_arr(path);
    int total_bin_nums = strlen(bits);


    for(j = 0; j < total_before_mapping; j++){
        list_ints_before[j] = 0;
    }

    for(j = 0; j < total_after_mapping; j++){
        list_ints_after[j] = 0;
    }

    for(j = 0; j < total_before_mapping; j++){
        judges_list[j] = 0;
    }

    for(j = 0; j < total_before_mapping; j++){
        ordering_list_before[j] = -2;
    }

    for(j = 0; j < total_after_mapping; j++){
        ordering_list_after[j] = 0;
    }


    int number = 0;
    int current_number = 0;
    int nxt = 0;

    for(j = 0; j < total_bin_nums; j++){
        if(count > 0){
	        if (bits[j] == '1'){
                number = pow_jack(2, count-1);
                current_number += number;
            }
        count-=1;
        }else{
            count = bl;
            list_ints_before[current_number] += 1;
            if(ordering_list_before[current_number] == -2){
                ordering_list_before[current_number] = nxt;
                nxt+=1;
            }
            current_number = 0;
            number = 0;
            for(int i = 1; i < discard; i++){
                j++;
            }
        }
    }


    int current_check = 0;
    int  greater_than = 0;

    for(int i = 0; i < total_before_mapping; i++){
        for(int j = 0; j < total_before_mapping; j++){
            if(list_ints_before[i] > list_ints_before[j]){
                greater_than += 1; 
            }
        }
        judges_list[i] = greater_than;
        greater_than = 0;   
    }

    current_check = 0;
    greater_than = 0;
    int dropped = 255;
    int cont = 1;
    int tmp_check = 1;
    //Extracting the highest half of numbers
    //
    for(int i = 0; i < total_after_mapping; i++){
        for(int j = 0; j < total_before_mapping; j++){
            if(current_check < judges_list[j] && judges_list[j] != -1){
                current_check = judges_list[j];
                cont = j;
            }
        }

        
        list_ints_before[cont] = -1;
        judges_list[cont] = -1;
        ordering_list_before[cont] = -1;
        current_check = 0;
        tmp_check = 1;
    }

    int iter = 0;
    current_check = 512;
    int val = 0;
    int order_iter=0;
    int check = 0;
    tmp_check = 1000000;

    for(int j = 0; j < total_after_mapping; j++){
        for (int k = 0; k < total_before_mapping; k++){
            if(ordering_list_before[k] < tmp_check && ordering_list_before[k] != -1){
                val = k;
                tmp_check = ordering_list_before[k];
            }
        }
        ordering_list_before[val] = -1;
        ordering_list_after[order_iter] = val;
        order_iter+=1;
        tmp_check = 1000000;
    }

    for(int i = 0; i < total_after_mapping; i++){
        for(int k = 0; k < total_after_mapping; k++){
            if(ordering_list_after[k] == i){
                list_ints_after[i] = k;
            }
        }
    }


    int remapped_number = 0;
    int pos_holder = 0;
    int mapped =0;  
    count = bl;
    current_number = 0;
    int converter = total_after_mapping;
    number = 0;

    for(int i = 0; i < total_bin_nums;i++){
        if(count > 0){
            if (bits[i] == '1'){
                number = pow_jack(2, count-1);
                current_number += number;
            }
            count-=1;
        }else{
            pos_holder = (i) - bl;

            if(list_ints_before[current_number] == -1){
                mapped = -1;
            }

            if(list_ints_before[current_number] != -1){
                mapped = 0;
            }

            for(int k = 0; k < total_after_mapping && mapped == 0; k++){
                if(current_number == ordering_list_after[k]){
                    remapped_number = k;
                    mapped = 1;
                }
            }

            if(mapped == 0 || mapped == -1){
                for(int j = 0; j < bl; j++) {
                    bits[pos_holder+j] = 'f';
                }
            }else{
                //converts integer into 8 bit binary sequence within the given list.
                for(int j = bl-2; j >=0; j--) {
                    bits[(pos_holder)+j] = (remapped_number & 1) + '0';
                    remapped_number >>= 1;
                }
            }
            bits[i-1] = 'f';
            for(int j = 1; j < discard; j++){
                bits[i] = 'f';
                i++;
            }
            current_number = 0;
            remapped_number = 0;
            pos_holder = 0;
            count = bl;
            mapped = 0;

        }
    }

    write_to_file(bits, outfile, total_bin_nums);


}



int str_int(char* str){
    char c = 0;
    int tmp_num = 0;
    int num = 0;
    int size = strlen(str);

    for (int i =0; i < size; i++){
        c = str[i];
        tmp_num = c -'0';
        num += tmp_num*pow_jack(10, size-(i+1));   
    }
    return num;
}

int pow_jack(int a, int b){
    int tmp_num = 1;
    if (b == 0){
        return 1;
    }
    for(int i = 0; i < b; i++){
        tmp_num = tmp_num*a;
    }
    return tmp_num;
}

int write_to_file(char* str, char* path, int total_bin_nums){
    FILE *fpw;
    //work path
    //fpw = fopen("/opt/sts-2.1.2/sts-2.1.2/data/C_gen_file.txt", "a");
    
    //laptop
    fpw = fopen(path, "a");
    
    /*Error handling for output file*/
    if (fpw== NULL)
    {
        puts("Issue in opening the Output file");
        exit(0);
    }

    for(int i = 0; i < total_bin_nums; i++){
        if(str[i] != 'f'){
            fputc(str[i], fpw);
        }
    }
    fclose(fpw);
    return 0;

}

cmd* parse_commandline(int argc, char** argv){

    cmd* ret = malloc(sizeof(cmd));

    if( argc > 6 ) {
        printf("Too many arguments supplied.\n");
        exit(0);
    }
    else if (argc < 6){
        printf("Five arguments expected.\n");
        exit(0);
    }

    ret->bl = (int) (argv[1][0] - '0');
    ret->sl = (int) (argv[2][0] - '0');
    ret->discard = (int) (argv[3][0] - '0');

    ret->filepath = malloc(strlen(argv[4])+1);

    for(int i = 0; i < strlen(argv[4]); i++){
        ret->filepath[i] = argv[4][i];
    }
    
    ret->outfile = malloc(strlen(argv[5])+1);

    for(int i = 0; i < strlen(argv[5]); i++){
        ret->outfile[i] = argv[5][i];
    }


    printf("filepath = %s\n", ret->filepath);
    printf("outfile = %s\n", ret->outfile);
    return ret;

}

char* create_bits_arr(char* filepath){
    FILE* fpw = fopen(filepath, "r");
    char* bits = malloc(256);
    int count = 0;
    int iter = 1;
    char c = 0;
    while((c = fgetc(fpw)) != EOF){
        if(count%256 ==0 && count > 0){
            iter+=1;
            bits = realloc(bits, 256*iter);
            if(bits == NULL){
                printf("Bad pointer\n");
                exit(0);
            }
        }
        bits[count] = c;
        count+=1;
    }
    return bits;

}