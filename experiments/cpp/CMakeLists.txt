cmake_minimum_required(VERSION 3.20)
project(value_logic_kernel LANGUAGES CXX)

include(CTest)

add_library(value_logic_kernel SHARED value_logic_kernel.cpp)
target_compile_features(value_logic_kernel PRIVATE cxx_std_17)
target_compile_definitions(value_logic_kernel PRIVATE VL_KERNEL_BUILD=1)

if(MSVC)
  target_compile_options(value_logic_kernel PRIVATE /W4 /permissive- /EHsc)
else()
  target_compile_options(value_logic_kernel PRIVATE -Wall -Wextra -Wpedantic)
endif()

if(BUILD_TESTING)
  add_executable(value_logic_kernel_self_test value_logic_kernel_self_test.cpp)
  target_compile_features(value_logic_kernel_self_test PRIVATE cxx_std_17)
  target_link_libraries(value_logic_kernel_self_test PRIVATE value_logic_kernel)
  add_test(NAME value_logic_kernel_self_test COMMAND value_logic_kernel_self_test)
endif()
