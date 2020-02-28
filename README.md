# Annotation of Adverse Drug Reactions in Patients’Weblogs
[[Japanese]](./README_ja.md)

We only distribute metadata of annotations as json files. 
Please follow the steps below to reconstruct the annotations with full contents. 
Basically, you only need to run `run.sh` after setting appropriate arguments.

1. Download the medatada json file.
2. Create an empty folder and put the medatada json file.
3. Edit arguments of `run.sh`.
    - Set the folder name created in step-2 to `--folder_path`.
    - Set the json file name to `--infile_name`.
    - Set an output file name to `--out_file`. (* extension must be `.json`.)
4. Run `sh run.sh`.
    - It downloads all the weblog articles over the internet through `http` using` request` of python module.
    - It creates `./folder_path/html/` and `./folder_path/article/` (You may delete these later if not needed).
    - There is a one second interval between `request`.
    Depending on the internet connection, this step may take time. Please be patient.
5. The json file with full text content will be reconstructed and saved.
    - The location was specified by `--folder_path`.
    - The output file name was specified by `--out_file`.


You may try and test this script using a sample file.
Please simply run ` sh run.sh` to generate `./trial/annotation.json` file from`./trial/trial.json` file.
