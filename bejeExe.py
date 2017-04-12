import sys
from cx_Freeze import setup, Executable

include_files = ['autorun.inf']
base = "Win32GUI"

setup(name="puzzle",
      version="0.1",
      description="Funny",
      options = {'build_exe' : {'include_files' : include_files}},
      executables = [Executable("client.py", base = base)]
      )

