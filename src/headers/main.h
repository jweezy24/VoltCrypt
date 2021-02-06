#include <stdio.h>

#include <string.h>
#include <stdlib.h>
//#include "simulated_input.h"
#include <math.h>

typedef struct dict{
    char* string;
    int iter;
}dict;

typedef struct bin_number{
    char* seq;
}bin_number;

typedef struct between{
    char* source;
    char* dest;
}between;

typedef struct cmd_args{
    char* filepath;
    char* outfile;
    int bl;
    int sl;
    int discard;
}cmd;

int main();

void vn_swap();

int create_dictionary_entry(char* bnum, dict* all_numbers, int iter, int iterate);

char* clear_pointer(char* string, int size);

void free_dictionary(dict* all_numbers, int iter);

bin_number* create_bin_number (char* str);

void int_to_binary(char* output_2, int num, int size);

dict* remap_dictionary_entry(char* src, char* dest, dict* remapper, int iter, int val);

char* get_key_from_string(dict* all_numbers, char* key);

int fromBinary(char *s);

void clear_str(char* str,int size);

void make_inital_bit_sequence(int total_bin_nums, bin_number* list_of_binary_seqs, dict* all_numbers, int bl);

void find_highest_half(int total_after_mapping, int total_before_mapping,  dict* all_numbers);

void replace_values(int total_before_mapping, int total_bin_nums, bin_number* list_of_binary_seqs, dict* all_numbers);

void remapping_algorithm(int total_after_mapping, int total_before_mapping, int total_bin_nums, bin_number* list_of_binary_seqs, dict* all_numbers, int bl, int sl,char* path);

int str_to_int(char* number);

long pow_jack(int a, int b);

void figure_what_to_write(int value, char* path);

cmd* parse_commandline(int argc, char** argv);
char* create_bits_arr(char* filepath);

long bin_to_int(char* bin);
void apply_discard(char* bits, int len, int bin_len, int discard);
void print_stream(char* bits, int len);

void form_histogram(char* bits, int len, int bin_len, int* histo_before, int* ordering_list, int histo_len);
void drop_highest_half(int* histo_before, int len1, int len2);
void new_mapping(int* histo_before, int len1, int* ordering_list_before, int* ordering_list_after, int* judges_list);
char* int_to_bin(int bin, int size);
void write_to_file(char* bin, char* path);
void translate_new_mappings(int* ordering_list, int len, int sl, char* bits, int len2, char* path);