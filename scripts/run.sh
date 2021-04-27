#!/bin/bash

trap exit SIGINT

scripts/parse.sh
scripts/eval.sh
