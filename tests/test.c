#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int str_to_int(char* str);
int pow_2(int base, int power);

int main(){
    char* test = "11010111";
    int res = str_to_int(test);
    printf("%d", res);
}

int str_to_int(char* str){
    int ret_int = 0;
    int length = strlen(str);

    for(int i=0; i<length; i++){
        if(str[i] == '1'){
            ret_int += pow_2(2,length-(i+1));
            printf("%d\n", pow_2(2,length-(i+1)));
        }
    }

    return ret_int;
}

int pow_2(int base, int power){
    int ret_int = 1;

    for(int i =0; i<power; i++){
        ret_int = ret_int*base;
    }

    return ret_int;

}