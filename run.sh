#!/bin/bash
crf_learn -f 4 -p 40 -c 3 template data/train.data model > train.rst  #output:model train.rst
crf_test -m model data/test.data > test.rst  #output:test.rst

