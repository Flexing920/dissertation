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

# Include any dependencies generated for this target.
include src/tools/CMakeFiles/emissionsMap.dir/depend.make

# Include the progress variables for this target.
include src/tools/CMakeFiles/emissionsMap.dir/progress.make

# Include the compile flags for this target's objects.
include src/tools/CMakeFiles/emissionsMap.dir/flags.make

src/tools/CMakeFiles/emissionsMap.dir/emissionsMap_main.cpp.o: src/tools/CMakeFiles/emissionsMap.dir/flags.make
src/tools/CMakeFiles/emissionsMap.dir/emissionsMap_main.cpp.o: ../src/tools/emissionsMap_main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/tl/sumo/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object src/tools/CMakeFiles/emissionsMap.dir/emissionsMap_main.cpp.o"
	cd /home/tl/sumo/build/src/tools && /bin/g++-9  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/emissionsMap.dir/emissionsMap_main.cpp.o -c /home/tl/sumo/src/tools/emissionsMap_main.cpp

src/tools/CMakeFiles/emissionsMap.dir/emissionsMap_main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/emissionsMap.dir/emissionsMap_main.cpp.i"
	cd /home/tl/sumo/build/src/tools && /bin/g++-9 $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/tl/sumo/src/tools/emissionsMap_main.cpp > CMakeFiles/emissionsMap.dir/emissionsMap_main.cpp.i

src/tools/CMakeFiles/emissionsMap.dir/emissionsMap_main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/emissionsMap.dir/emissionsMap_main.cpp.s"
	cd /home/tl/sumo/build/src/tools && /bin/g++-9 $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/tl/sumo/src/tools/emissionsMap_main.cpp -o CMakeFiles/emissionsMap.dir/emissionsMap_main.cpp.s

# Object files for target emissionsMap
emissionsMap_OBJECTS = \
"CMakeFiles/emissionsMap.dir/emissionsMap_main.cpp.o"

# External object files for target emissionsMap
emissionsMap_EXTERNAL_OBJECTS =

../bin/emissionsMapD: src/tools/CMakeFiles/emissionsMap.dir/emissionsMap_main.cpp.o
../bin/emissionsMapD: src/tools/CMakeFiles/emissionsMap.dir/build.make
../bin/emissionsMapD: src/utils/emissions/libutils_emissions.a
../bin/emissionsMapD: src/foreign/PHEMlight/cpp/libforeign_phemlight.a
../bin/emissionsMapD: src/utils/distribution/libutils_distribution.a
../bin/emissionsMapD: src/utils/shapes/libutils_shapes.a
../bin/emissionsMapD: src/utils/options/libutils_options.a
../bin/emissionsMapD: src/utils/xml/libutils_xml.a
../bin/emissionsMapD: src/utils/geom/libutils_geom.a
../bin/emissionsMapD: src/utils/common/libutils_common.a
../bin/emissionsMapD: src/utils/importio/libutils_importio.a
../bin/emissionsMapD: src/utils/iodevices/libutils_iodevices.a
../bin/emissionsMapD: src/utils/traction_wire/libutils_traction_wire.a
../bin/emissionsMapD: src/foreign/tcpip/libforeign_tcpip.a
../bin/emissionsMapD: /usr/lib/x86_64-linux-gnu/libxerces-c.so
../bin/emissionsMapD: /usr/lib/x86_64-linux-gnu/libz.so
../bin/emissionsMapD: /usr/lib/x86_64-linux-gnu/libproj.so
../bin/emissionsMapD: src/tools/CMakeFiles/emissionsMap.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/tl/sumo/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../../bin/emissionsMapD"
	cd /home/tl/sumo/build/src/tools && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/emissionsMap.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/tools/CMakeFiles/emissionsMap.dir/build: ../bin/emissionsMapD

.PHONY : src/tools/CMakeFiles/emissionsMap.dir/build

src/tools/CMakeFiles/emissionsMap.dir/clean:
	cd /home/tl/sumo/build/src/tools && $(CMAKE_COMMAND) -P CMakeFiles/emissionsMap.dir/cmake_clean.cmake
.PHONY : src/tools/CMakeFiles/emissionsMap.dir/clean

src/tools/CMakeFiles/emissionsMap.dir/depend:
	cd /home/tl/sumo/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/tl/sumo /home/tl/sumo/src/tools /home/tl/sumo/build /home/tl/sumo/build/src/tools /home/tl/sumo/build/src/tools/CMakeFiles/emissionsMap.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/tools/CMakeFiles/emissionsMap.dir/depend

