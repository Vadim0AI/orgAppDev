import subprocess
from path_global import path_scr1, path_py_interpreter

process = subprocess.Popen([path_py_interpreter, path_scr1],
                                   creationflags=subprocess.CREATE_NO_WINDOW)