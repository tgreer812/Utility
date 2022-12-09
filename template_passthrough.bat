rem This template can be used to allow python files to be called from the command line without specifying 'python' first. I'm lazy
rem To use: rename this file to have the same name as the python script and then place this bat file in a directory on the PATH
rem Note: Make sure the python files lives in the directory specified by myscripts_dir
@echo off

rem Get the base name of the batch script without the file extension
set script_name=%~n0

rem Get the value of the MYSCRIPTS environment variable
set myscripts_dir=%MYSCRIPTS%

rem Call the Python script with the same name as the batch script and pass all arguments to it
python %myscripts_dir%\%script_name%.py %*
