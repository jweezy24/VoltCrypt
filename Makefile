RM := rm -rf


#OPENOCDDIR := /opt/openocd/
#OCDCONFIG=microchip_same54_xplained_pro.cfg
ODIR= bin
SDIR= src
CFLAGS=-I src/headers 
CFLAGS+= -lm
# CFLAGS += -DDEBUG=2
# CFLAGS+=-O0 -fno-stack-protector -mthumb -march=armv7e-m -mtune=cortex-m4 -mfloat-abi=hard -mfpu=fpv4-sp-d16 -fvar-tracking -g3
# # CFLAGS+=-I./src/samd51/CMSIS/Include
# CFLAGS+=-I./src/samd51/include/instance
# CFLAGS+=-I./src/samd51/include/pio
# CFLAGS+=-I./src/samd51/include
# CFLAGS+=-I./src/samd51/include/component

# CFLAGS+= -D__ATSAMD51G18A__
# CFLAGS+= -D pvPortMalloc=malloc
# CFLAGS+= -D vPortMalloc=malloc
# CFLAGS+= -D pvPortFree=free
# CFLAGS+= -D vPortFree=free
# CFLAGS += -D STACK_SIZE=1024
# CFLAGS += -D printf=rprintf

CC=gcc
LD=ld
SIZE=size


OBJS += \
		main.o\
		


	

OBJ = $(patsubst %,$(ODIR)/%,$(OBJS))

$(ODIR)/%.o: $(SDIR)/%.c
		$(CC) $(CFLAGS) -c -g -o $@ $^
$(ODIR)/%.o: $(SDIR)/%.s
	nasm -f elf32 -g -o $@ $^

all: bin

bin: $(OBJ)
	$(CC) $(CFLAGS) $(ODIR)/*  -o VoltCrypt.o

clean:
	rm  VoltCrypt ./bin/main.o

clean_all:
	rm -rf VoltCrypt bin/*

run:
	#python3 ./python_scripts/NIST_test_script.py
	python3 ./python_scripts/create_nist_graphs.py