import cx_Freeze

import sys
import PyQt5


base=None

if sys.platform=='Win32':
    base='Win32Gui'


executables=[cx_Freeze.Executable("cam_0.py",base=base)]

cx_Freeze.setup(
    name='tk gui',
    options={"build_exe":{"packages":["tkinter"]}},
    version="0.01",
    executables=executables
)