modules = ['selenium', 'aiogram', 'requests', 'json', 'uuid']

import subprocess
import sys

def installmodules():
    def install(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    for i in modules:
        try:
            install(i)
        except Exception as e:
            print(e)

#installmodules()