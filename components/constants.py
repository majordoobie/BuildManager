LIBRARY_TEMPLATE = """\
# Name of the lib you are creating for linking later
TARGET={component_name}.a  # Name of the library

INCLUDE=../../include

CC=cc
CFLAGS+=-Wall -Wextra -Wpedantic -Waggregate-return -Wwrite-strings -Wvla -Wfloat-equal -I$(INCLUDE)

# Set the target directory, all obj's will go to bin so that each section can link if they need to
BIN=../../bin

# greps through the CWD for any files ending in .c
# Then match those files with files in $(BIN) with the extension of .o not .c
# This is how we'll create the rules; i.e. $(BIN)/prog.o: prog.c
# You can check them out with:
# $(info $$SRCS is [${{SRCS}}])
# $(info $$OBJS is [${{OBJS}}])

SRCS=$(wildcard *.c)
OBJS=$(patsubst %.c, $(BIN)/%.o, $(SRCS))

# Target rule for call target
all: $(TARGET)

# This allows for a section to be missing like "check" only belongs in /test by
# setting it in .PHONY we don't need to edit the main Makefile
.PHONY: debug clean check profile

# Compiles with -pg
profile: CFLAGS+= -pg
profile: $(TARGET)

# Compiles with -g
debug: CFLAGS+= -g
debug: $(TARGET)

# Links all the OBJ files. Since there is no OBJ it will look for a rule
# for an obj. For example if obj is ../../bin/arg_parser.o it will match on
# $(BIN)/%.o and match it with a file with the same name in the CWD with the
# extension of .c
$(TARGET): $(OBJS)
    $(info $(OBJS))
    ar rcs $(BIN)/$(TARGET) $(OBJS)
    ranlib $(BIN)/$(TARGET)

# This is where it matches the OBJ to the source file
$(BIN)/%.o: %.c
    $(CC) $(CFLAGS) -c $< -o $@

# This is called when `make clean` is called from the master
clean:
    rm -rf $(OBJS)
    rm -rf $(BIN)/$(TARGET)
"""

LIBRARY_C_FILE_TEMPLATE = """\
#include <{component_name}.h>

int {component_name}(void)
{{
    return 0;
}}
"""

LIBRARY_H_FILE_TEMPLATE = """\
#ifndef {header_var}
#define {header_var}

#endif //{header_var}
"""

ROOT_MAKEFILE = """\
# This is the only part you edit. Add the path to the Makefile to call
# The order does matter!
DIRS={project_dirs}

BUILD_DIRS=$(DIRS:%=build-%)
DEBUG_DIRS=$(DIRS:%=debug-%)
CLEAN_DIRS=$(DIRS:%=clean-%)
CHECK_DIRS=$(DIRS:%=check-%)
PROFILE_DIRS=$(DIRS:%=profile-%)

all: SETUP $(BUILD_DIRS)

SETUP:
    @mkdir -p bin

$(BUILD_DIRS):
    $(MAKE) -C $(@:build-%=%)

clean: $(CLEAN_DIRS)
$(CLEAN_DIRS):
    $(MAKE) -C $(@:clean-%=%) clean

debug: $(DEBUG_DIRS)
$(DEBUG_DIRS):
    $(MAKE) -C $(@:debug-%=%) debug

profile: $(PROFILE_DIRS)
$(PROFILE_DIRS):
    $(MAKE) -C $(@:profile-%=%) profile

check: $(CHECK_DIRS)
$(CHECK_DIRS):
    $(MAKE) -C $(@:check-%=%) check
"""


ROOT_CMAKE = """\
cmake_minimum_required(VERSION {cmake_version})
project({project_name} C)

set(CMAKE_C_STANDARD {c_standard})

{cmake_projects}
"""


