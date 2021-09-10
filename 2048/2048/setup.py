

import sys
from cx_Freeze import setup,Executable

import os

os.environ['TCL_LIBRARY'] = r"C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\tcl\tk8.6"

include_files = [
    r"C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\DLLs\tcl86t.dll",
    r"C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\DLLs\tk86t.dll",
]


build_exe_options = {
    "packages":[],
    "include_files":include_files
}

base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(name = "2048",
    version = "0.1",
    description = "2048",
    options = {"build_exe":build_exe_options},
    executables = {Executable("_2048.py",base=base)}
    )