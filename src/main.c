#include "main.h"

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

    int* list_ints_before = malloc(sizeof(int) * total_before_mapping);
    int* list_ints_after = malloc(sizeof(int) * total_after_mapping);
    int* judges_list = malloc(sizeof(int) * total_before_mapping);
    int* ordering_list_before =malloc(sizeof(int) * total_before_mapping);
    int* ordering_list_after =malloc(sizeof(int) * total_after_mapping);

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
        judges_list[j] = -1;
    }

    for(j = 0; j < total_before_mapping; j++){
        ordering_list_before[j] = -2;
    }

    for(j = 0; j < total_after_mapping; j++){
        ordering_list_after[j] = 0;
    }

    //Testing bin_to_int function
    //printf("%d\n", bin_to_int("01110111"));

    //Testing apply discard
    apply_discard(bits, total_bin_nums, bl, discard);
    
    //print_stream(bits, total_bin_nums);

    form_histogram(bits, total_bin_nums, bl, list_ints_before, ordering_list_before, total_before_mapping);

    //histogram test
    // printf("TOTAL BEFORE MAPPING = %d\n", list_ints_before);
    // for(int i =0; i < total_before_mapping; i++ ){
    //     printf("%d\t", list_ints_before[i]);
    // }
    // printf("\n");
    //ordering list check
    // for(int i =0; i < total_before_mapping; i++ ){
    //     printf("%d\t", ordering_list_before[i]);
    // }

    // printf("\n");
    drop_highest_half(list_ints_before, total_before_mapping, total_after_mapping);
    
    // for(int i =0; i < total_before_mapping; i++ ){
    //     printf("%d\t", list_ints_before[i]);
    // }

    // printf("\n");
    new_mapping(list_ints_before, total_before_mapping, ordering_list_before, ordering_list_after, judges_list);


    // for(int i =0; i < total_after_mapping; i++ ){
    //     printf("%d\t", ordering_list_after[i]);
    // }
    // printf("\n");

    translate_new_mappings(judges_list, total_after_mapping, sl, bits, total_bin_nums, outfile);
}

long pow_jack(int a, int b){
    long tmp_num = 1;
    if (b == 0){
        return 1;
    }
    for(int i = 0; i < b; i++){
        
        tmp_num = tmp_num*a;
        //printf("tmp_num = %d\n", tmp_num);
    }
    return tmp_num;
}

void apply_discard(char* bits, int len, int bin_len, int discard){
    int count = 0;
    if (discard == 0){
        return;
    }
    int just_discarded = 0;
    for (int i =0; i < len;){
        if(i%bin_len == 0 && i > 0 && just_discarded == 0){
            for(int j = 0; j < discard; j++){
                bits[i+j] = -1;
            }
            i+=discard;
            just_discarded = 1;
            continue;
        }
        just_discarded = 0;
        i+=1;

    }
}


void print_stream(char* bits, int len){
    for(int i =0; i < len; i++){
        printf("%c", bits[i]);
    }
    printf("\n");
}


void form_histogram(char* bits, int len, int bin_len, int* histo_before, int* ordering_list, int histo_len){
    char* bin_num = malloc(bin_len+1);
    int count = 0;
    int index = 0;
    for(int i = 0; i < len; i++){
        if(count%bin_len == 0 && i > 0){
            bin_num[count] = 0;
            int num = bin_to_int(bin_num);
            if(histo_before[num] == 0){
                ordering_list[index] = num;
                index+=1;
            }

            histo_before[num] += 1;

            if(bits[i]!= -1){
                count = 1;
                bin_num[0] = bits[i];
            }else{
                count = 0;
            }

        }else{
            if(bits[i] != -1){
                bin_num[count] = bits[i];
                count+=1;
            }
        }
    }
    free(bin_num);
}

void drop_highest_half(int* histo_before, int len1, int len2){
    int max = 0;
    int index = 0;
    for(int i =0; i < len2; i++){
        max = 0;
        for(int j =0; j < len1; j++){
            if(histo_before[j] > max){
                max = histo_before[j];
                index = j;
            }
        }
        histo_before[index] = -1;
        index = 0;
    }

}

void new_mapping(int* histo_before, int len1, int* ordering_list_before, int* ordering_list_after, int* judges_list){
    int index = 0;
    int location = 0;

    for(int i = 0; i < len1; i++){
        index = ordering_list_before[i];

        if(histo_before[index] != -1){
            ordering_list_after[location] = index;
            judges_list[index] = (location+i)%((int)(len1/2));
            location+=1;
        }
    }

}

void translate_new_mappings(int* judges_list, int len, int sl, char* bits, int len2, char* path){
    char* bin_num = malloc(sl+1);
    int count = 0;
    for(int i = 0; i < len2; i++){
        if(count%(sl+1) == 0 && i > 0){
            bin_num[count] = 0;
            int num = bin_to_int(bin_num);
            
            
            int ind = judges_list[num];
            if(ind != -1){
                char* new_num = int_to_bin(ind,sl);
                write_to_file(new_num, path);
                free(new_num);
            }
                
            

            if(bits[i]!= -1){
                count = 1;
                bin_num[0] = bits[i];
            }else{
                count = 0;
            }

        }else{
            if(bits[i] != -1){
                bin_num[count] = bits[i];
                count+=1;
            }
        }
    }
    free(bin_num);

}


long bin_to_int(char* bin){
    long ret = 0;
    int len = strlen(bin);
    for(int i = 0; i < len; i++){
        if(bin[i] == '1'){
            ret += pow_jack(2,(len-1)-i);
        }
    }

    return ret;
}

char* int_to_bin(int bin, int size){
    char* ret = malloc(size+1);

    int count = 0;
    for(int i = size-1; i >= 0; i--){
        if(bin >= pow_jack(2,i)){
            ret[count] = '1';
            bin -= pow_jack(2,i);
        }else{
            ret[count] = '0';
        }
        count+=1;
    }
    ret[size] = 0;

    return ret;

}

int str_to_int(char* number){
    int count = 0;
    int ret = 0;

    printf("NUMBER = %s\n", number);

    while(number[count] != 0){
        count+=1;    
    }

    int* holder = malloc((count+1) * sizeof(int));

    for(int i =0; i < count; i++){
        holder[i] = number[i]- '0';
    }


    for (int i =0; i < count; i++){
        ret += pow_jack(10, (count)-(i+1)) * holder[i];
       
    }
    

    return ret;

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

    ret->bl = (int) (str_to_int(argv[1]));
    ret->sl = (int) (str_to_int(argv[2]));
    ret->discard = (int) (str_to_int(argv[3]));

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

void write_to_file(char* bin, char* path){

    FILE* fp = fopen(path, "a");
    fputs(bin, fp);
    fclose(fp);

}