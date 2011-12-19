#!/bin/bash

export PATH=$CXXTEST/bin:$PATH

# @main:
cxxtestgen --runner=YesNoRunner -o runner.cpp MyTestSuite2.h
# @:main

# @compile:
g++ -o runner -I$CXXTEST runner.cpp
# @:compile

./runner

echo $?