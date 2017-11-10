cmake_minimum_required(VERSION 3.8)
project(pi_fys)

set(CMAKE_CXX_STANDARD 17)

set(SOURCE_FILES src/main.cpp)

add_executable(pi_fys ${SOURCE_FILES} src/main.cpp)