import os
import subprocess
import multiprocessing
from colorama import Fore, Style
import sys
import shutil
from settings import *

def status(msg: str):
    print(Style.BRIGHT + Fore.CYAN + msg + Fore.RESET + Style.RESET_ALL)


if len(sys.argv) >= 2 and sys.argv[1] == 'clean':
    shutil.rmtree(getBuildPath())

if not os.path.exists(getBuildPath()):
    os.mkdir(getBuildPath())
    os.chdir(getBuildPath())
    subprocess.run("cmake .. -G \"Unix Makefiles\"", shell=True)
    os.chdir('..')

os.chdir(getBuildPath())

verbose = ''
if len(sys.argv) >= 2 and sys.argv[1] == 'verbose':
    verbose = 'VERBOSE=1'
result = subprocess.run(f'make -j {multiprocessing.cpu_count()} {verbose}', shell=True)
if result.returncode != 0:
    exit()

def fromelf():
    status("Generating code.bin")
    subprocess.run("\"" + os.environ.get('ARMCC_PATH') + f"/bin/fromelf.exe\" --bincombined --bincombined_padding=1,0x00 {getElfName()} --output {getCodeBinaryName()}", shell=True)

if os.path.exists(getCodeBinaryName()):
    if os.path.getmtime(getCodeBinaryName()) < os.path.getmtime(getElfName()):
        fromelf()
else:
    fromelf()
    
def trimCodeBinary():
    TRUNCATED_SIZE = 0x45B000

    with open(getCodeBinaryName(), 'a') as codeBinary:
        codeBinary.truncate(TRUNCATED_SIZE)

# A hack here: We'll trim code.bin to its known "correct" size to erase the unwanted extra sections that were placed
trimCodeBinary()

os.chdir('..')