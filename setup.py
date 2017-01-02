#
# from cx_Freeze import setup, Executable
#
# setup(name='deneme prg', version='0.01',description='simple gui',executables=[Executable("fap.py")])




import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "includes": ["PyQt5"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "my gui",
        version = "0.1",
        description = "My GUI application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("fap.py", base=base)])