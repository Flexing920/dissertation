# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/tl/sumo

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/tl/sumo/build

# Utility rule file for generate-version-h.

# Include the progress variables for this target.
include src/CMakeFiles/generate-version-h.dir/progress.make

src/CMakeFiles/generate-version-h: src/version.h


src/version.h: ../.git
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/tl/sumo/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Generating version.h"
	cd /home/tl/sumo/build/src && /home/tl/anaconda3/bin/python /home/tl/sumo/src/../tools/build/version.py /home/tl/sumo/build/src

generate-version-h: src/CMakeFiles/generate-version-h
generate-version-h: src/version.h
generate-version-h: src/CMakeFiles/generate-version-h.dir/build.make

.PHONY : generate-version-h

# Rule to build all files generated by this target.
src/CMakeFiles/generate-version-h.dir/build: generate-version-h

.PHONY : src/CMakeFiles/generate-version-h.dir/build

src/CMakeFiles/generate-version-h.dir/clean:
	cd /home/tl/sumo/build/src && $(CMAKE_COMMAND) -P CMakeFiles/generate-version-h.dir/cmake_clean.cmake
.PHONY : src/CMakeFiles/generate-version-h.dir/clean

src/CMakeFiles/generate-version-h.dir/depend:
	cd /home/tl/sumo/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/tl/sumo /home/tl/sumo/src /home/tl/sumo/build /home/tl/sumo/build/src /home/tl/sumo/build/src/CMakeFiles/generate-version-h.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/CMakeFiles/generate-version-h.dir/depend

