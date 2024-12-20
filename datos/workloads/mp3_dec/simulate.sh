#! /bin/bash

cd "$(dirname $0)"
GEM5PATH=~/mySimTools/gem5/build/ARM
SCRIPTDIR=../../scripts/CortexA76_scripts_gem5

MOREOPTIONS="--l1d_size=512kB --num_fu_write=16 --l2_assoc=16"

$GEM5PATH/gem5.fast $SCRIPTDIR/CortexA76.py --cmd=mp3_dec --options="-w mp3dec_outfile.wav mp3dec_testfile.mp3 " $MOREOPTIONS
