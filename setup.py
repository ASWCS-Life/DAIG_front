from cx_Freeze import setup, Executable
import sys

base = None 
# if sys.platform == "win32": 
#     base = "Win32GUI"


                                
buildOptions ={"packages" :["ui"],
                "includes":[],
                }

exe = [Executable("daig_exec.py",base=base)]  

setup(
    name= 'DAIG',
    version = '0.1',
    author = "Life",
    description = "DAIG",
    options = {
        'build_exe':buildOptions,
        'bdist_msi': {
                    'target_name':'DAIG_installer.msi'
                    }
    },
    executables = exe
    
)
