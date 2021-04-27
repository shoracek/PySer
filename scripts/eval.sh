#!/bin/bash

trap exit SIGINT

out_dir="output"

python3 pa193_dataset/output_compare.py "$out_dir" pa193_dataset/dataset/ -v
