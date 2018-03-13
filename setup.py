import os
import sys
from cx_Freeze import setup,Executable

os.environ["TCL_LIBRARY"] = "c:/Program Files/Python36/tcl/tcl8.6"
os.environ["TK_LIBRARY"] = "c:/Program Files/Python36/tcl/tk8.6"

includefiles = ["resources/avgs", "resources/sr", "resources/owlogo.ico", "resources/owHeader.png", "resources/currentSr.png", "resources/avgsrloss.png", "resources/avgsrgainnew.png", "C:\Program Files\Python36\DLLs\\tcl86t.dll", "C:\Program Files\Python36\DLLs\\tk86t.dll"]
includes = []
packages = []

base = None
if (sys.platform == "win32"):
    base = "Win32GUI"
    
setup(
    name = "Overwatch SR Counter",
    version = "0.1",
    description = "A utility for counting SR gains & loses, and an average or those.",
    author = "Tiyst#2803",
    author_email = "sijie.wuu@gmail.com",
    options = {'build_exe': {'includes':includes,'packages':packages,'include_files':includefiles}}, 
    executables = [Executable("owSrCounter.py", base=base, icon="owlogo.ico")]
)