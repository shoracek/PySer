#!/bin/bash

trap exit SIGINT

out_dir="output"

mkdir -p "$out_dir"

python3 src/pyser.py --output_folder="$out_dir" pa193_dataset/dataset/*.txt

