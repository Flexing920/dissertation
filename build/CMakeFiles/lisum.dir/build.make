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

# Utility rule file for lisum.

# Include the progress variables for this target.
include CMakeFiles/lisum.dir/progress.make

CMakeFiles/lisum:
	cd /home/tl/sumo && /usr/bin/cmake -E env JAVA_HOME=/usr /usr/bin/mvn --batch-mode -f tools/contributed/lisum/pom.xml clean install
	cd /home/tl/sumo && /usr/bin/cmake -E copy tools/contributed/lisum/lisum-core/target/lisum-core-1.0.2.jar bin/lisum-core.jar
	cd /home/tl/sumo && /usr/bin/cmake -E copy tools/contributed/lisum/lisum-gui/target/lisum-gui-1.1.jar bin/lisum-gui.jar

lisum: CMakeFiles/lisum
lisum: CMakeFiles/lisum.dir/build.make

.PHONY : lisum

# Rule to build all files generated by this target.
CMakeFiles/lisum.dir/build: lisum

.PHONY : CMakeFiles/lisum.dir/build

CMakeFiles/lisum.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/lisum.dir/cmake_clean.cmake
.PHONY : CMakeFiles/lisum.dir/clean

CMakeFiles/lisum.dir/depend:
	cd /home/tl/sumo/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/tl/sumo /home/tl/sumo /home/tl/sumo/build /home/tl/sumo/build /home/tl/sumo/build/CMakeFiles/lisum.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/lisum.dir/depend

