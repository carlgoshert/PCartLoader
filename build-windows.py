import sys, subprocess, argparse, os, make_version, shutil

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch", action="store_true", help="Launch EXE after building.")
    args = parser.parse_args()
    
    version = make_version.main()
    
    proc = subprocess.Popen(["pyinstaller", ".\\PCartLoader.spec", "-y"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        print(line, end="", flush=True)
    proc.wait()
    if proc.returncode != 0:
      sys.exit(proc.returncode)
    
    shutil.make_archive(f"./dist/PCartLoader_Windows_x86_64_v{version}", "zip", "./dist/PCartLoader/")

    if args.launch:
      proc = subprocess.Popen(["./dist/PCartLoader/PCartLoader.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
      for line in proc.stdout:
          print(line, end="", flush=True)
      sys.exit(proc.returncode)

if __name__ == "__main__":
    main()
