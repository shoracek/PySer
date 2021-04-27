# PySer

A regular expression based parser for security certificates.

## Examples of Usage

### Parse a single file

The resulting file are then located in the current working directory.

    ./src/pyser.py pa193_dataset/dataset/1102a_pdf.txt

### Parse the whole dataset

Can also specify the output folder to not clutter the current working directory.

    ./src/pyser.py pa193_dataset/dataset/*.txt -o output

### Parse a single file with pretty-printing of title and revisions

    ./src/pyser.py pa193_dataset/dataset/1102a_pdf.txt -o output -p title,revisions
    
### Parse a single file with pretty-printing of title and revisions (short form)
    
    ./src/pyser.py pa193_dataset/dataset/1102a_pdf.txt -o output -p tit,rev

See `./src/pyser.py --help` for a complete overview.

## Bash Scripts

The scripts are meant to be run in the root directory of the project.

- `parse.sh` - create a folder named `output` and store the results of whole dataset parsing there.
- `eval.sh` - evaluate each output against the ground truth of the dataset using `pa193_dataset/output_compare.py`.
- `run.sh` - run both stages above in given order.
