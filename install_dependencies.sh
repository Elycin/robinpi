#!/usr/bin/env bash
git clone https://github.com/aamazie/Robinhood.git
git clone https://github.com/rm-hull/luma.led_matrix.git

cd Robinhood;
pip3 install .

cd ..


cd luma.led_matrix;
pip3 install .