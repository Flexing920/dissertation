# CMake generated Testfile for 
# Source directory: /home/tl/sumo/src/traci_testclient
# Build directory: /home/tl/sumo/build/src/traci_testclient
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(libsumotest "/home/tl/sumo/bin/testlibsumo")
set_tests_properties(libsumotest PROPERTIES  _BACKTRACE_TRIPLES "/home/tl/sumo/src/traci_testclient/CMakeLists.txt;18;add_test;/home/tl/sumo/src/traci_testclient/CMakeLists.txt;0;")
add_test(libsumostatictest "/home/tl/sumo/bin/testlibsumostatic")
set_tests_properties(libsumostatictest PROPERTIES  _BACKTRACE_TRIPLES "/home/tl/sumo/src/traci_testclient/CMakeLists.txt;23;add_test;/home/tl/sumo/src/traci_testclient/CMakeLists.txt;0;")
