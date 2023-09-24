import subprocess
import sys
import os
from pathlib import Path

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def read_deps_file(deps_filename):
    with open(deps_filename, 'r') as deps_file:
        deps = deps_file.read().strip()
        if not deps:
            return None
        else:
            return deps
        
def build_asm_deps(build_cmd, deps, out_filename):
    try:
        # print("running: " + build_cmd + " " + deps + " -o " + out_filename, flush=True)
        subprocess.run(build_cmd + " " + deps + " -o " + out_filename)
        # print("finished running: " + build_cmd + " " + deps + " -o " + out_filename, flush=True)
    except subprocess.CalledProcessError as e:
        print(f"Error building asm deps: Command '{build_cmd + deps + f'-o' + out_filename}' returned a non-zero exit code ({e.returncode}).")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python build_asm_deps.py <build_command> <deps_filename> <out_filename>")
        sys.exit(1)

    deps = read_deps_file(sys.argv[2])
    if deps is not None:
        build_asm_deps(str(sys.argv[1]), str(deps), str(sys.argv[3]))
    else:
        build_asm_deps(str(sys.argv[1]), get_script_path() + "/empty_asm.s", str(sys.argv[3]))
