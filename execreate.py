'''
EXE CREATION UTILITY

Date: 10/27/22

Description:
A tool for converting python files to executables automatically.

Requirements:
  * argparse
  * py2exe (pip install it)

TODO:

'''

import argparse
import base64
import os
import hashlib
import shutil
import json
import traceback

ROOT_DIR = ""
PYTHON_SCRIPTS_DIR = ""
BIN_DIR = ""
MD5_PASSWORD_HASH = ""

def generate_setup_py(filename : str) -> str:
  '''SUMMARY
  
  DESCRIPTION
  
  Args:
    file_root (str): The name of the file in root form.
      (i.e jus tthe name without an extension or proceeding path - e. execreate)
  
  Returns:
    str: A string containing the generated python script.
  '''
  py_script = (
    "from distutils.core import setup\n"
    "import py2exe\n"
    "setup(console=['%s'])" %(filename)
  )
  
  return py_script


def generate_executable_bat_wrapper(file_root : str, executable_path : str):
  '''
  '''
  
  global ROOT_DIR
  
  # Creates the target executable full path string
  print(executable_path)
  executable_path = os.path.normpath(executable_path) + "\\%s.exe" %(file_root)
  
  bat_script = (
    r"@echo off" + "\n"
    r"setlocal enabledelayedexpansion" + "\n"
    r'set target="REPLACE_ME"' + "\n"
    r"set argString=" + "\n"
    r"for %%x in (%*) do set argString=!argString! %%x" + "\n"
    r"%target% %argString%" + "\n"
  ).replace('REPLACE_ME', executable_path)
  
  bat_name = "%s.bat" %(file_root)
  with open(bat_name, 'w') as fd:
    fd.write(bat_script)
    
  # move bat script to root directory
  src = os.path.normpath(bat_name)
  dst = "%s/%s" %(ROOT_DIR, bat_name)
  shutil.move(src, dst)
  
def run_p2e_and_relocate(setup_script : str, file_root : str) -> str:
  '''
  '''
  
  global PYTHON_SCRIPTS_DIR
  global BIN_DIR
  
  with open('setup.py', 'w') as fd:
    fd.write(setup_script)
  
  # generate dist directory with executable
  # TODO: supress output
  os.system('python setup.py py2exe')
  
  # rename dist directory
  bin_dist_name = "%s_dist" %(file_root)
  os.rename('dist', bin_dist_name)
  print("Renaming dist directory ==> %s" %(bin_dist_name))
  
  # move directory to bin
  src = "%s/%s" %(".", bin_dist_name)
  dst = "%s/%s" %(BIN_DIR, bin_dist_name)
  shutil.move(src, dst)
  
  return os.path.realpath(dst)

def run(args : argparse.Namespace):
  
  script = generate_setup_py(args.filename)
  
  file_root = os.path.splitext(os.path.split(args.filename)[1])[0]
  
  executable_path = run_p2e_and_relocate(script, file_root)
  
  generate_executable_bat_wrapper(file_wroot, executable_path)
    
# TODO: add validate user


def init_config(args : argparse.Namespace) -> bool:
  '''
  '''
  
  global ROOT_DIR
  global PYTHON_SCRIPTS_DIR
  global BIN_DIR
  global MD5_PASSWORD_HASH
  
  try:
    
    config = json.load(args.config)
    
    architecture = config['architecture']
    ROOT_DIR = architecture['rootDir']
    PYTHON_SCRIPTS_DIR = architecture['pythonScriptsDir']
    BIN_DIR = architecture['binDir']
    
    MD5_PASSWORD_HASH = config['md5PasswordHash']
  except Exception as e:
    
    print("Failed to parse configuration file")
    traceback.print_exc()
    return False
  
  return True

def main():
  
  parser = argparse.ArgumentParser()
  parser.add_argument("-c", "--config", type=argparse.FileType('r'), default="./execonfig.json", help="JSON configuration file")
  parser.add_argument("filename", type=str, help="Python file to convert to .exe")
  
  args = parser.parse_args()
  
  try:
    # TODO: implement validate_user
    if(init_config(args) '''and validate_user()'''):
      run(args)
    
  except KeyboardInterrupt:
    pass
  except AssertionError as e:
    print(e)
  except Exception as e:
    print("Unknown exception...")
    print(e)
  
  
if __name__ == "__main__":
  main()
  
  
  
  
  
