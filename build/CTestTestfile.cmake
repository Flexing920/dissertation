# CMake generated Testfile for 
# Source directory: /home/tl/sumo
# Build directory: /home/tl/sumo/build
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(exampletest "/home/tl/anaconda3/bin/python" "/home/tl/sumo/docs/examples/runAll.py")
set_tests_properties(exampletest PROPERTIES  _BACKTRACE_TRIPLES "/home/tl/sumo/CMakeLists.txt;653;add_test;/home/tl/sumo/CMakeLists.txt;0;")
subdirs("src")
subdirs("unittest")
