#!/bin/bash

out_dir="output"

for ref_file in ../pa193_dataset/dataset/*.json; do
    out_file="$out_dir/$(basename $ref_file)"
    echo evaluating "$out_file"...
    python3 ../pa193_dataset/output_compare.py "$out_file" "$ref_file"
done
