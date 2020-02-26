# prism_annotation

This is a repository that include the script for restoring the text and annotations from released json file.
Annotation data and text data can be reproduced by executing `run.sh` with appropriate arguments.

The usage is as follows.

1. Get released json file.
2. Create an arbitrary folder and put the json data obtained in 1. into that folder.
3. Change arguments of `run.sh`.
    - Enter the folder name created in 2. into `--folder_path`.
    - Enter the json file name obtained in 1. into `--infile_name`.
    - Enter the name of the file you want to output into `--out_file`. (* extension must be `.json`.)
4. Execute `sh run.sh`.
    - When executed, it communicates with `http` using` request` of python module.
    Please execute with an internet.
    - `./folder_path/html/` and `./folder_path/article/` are generated. Delete them if not needed.
    - There is a one second interval between `request`.
    Depending on the amount of data, it can be expected to take a lot of time.
5. The json file with the text and annotations restored is generated.
    - The location where the file is created is specified by `--folder_path`.
    - The output file name is specified by `--out_file`.


Please execute using the trial data attached for the test.
After `clone` this repository, execute` sh run.sh` to generate `./trial/annotation.json` file from`./trial/trial.json` file.
