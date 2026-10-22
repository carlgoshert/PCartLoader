import argparse, os, sys, subprocess, tomllib, make_version

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch", action="store_true", help="Launch AppImage after building.")
    args = parser.parse_args()
    
    make_version.main()

    proc = subprocess.Popen(["pyproject-appimage"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        print(line, end="", flush=True)
    proc.wait()
    if proc.returncode != 0:
      sys.exit(proc.returncode)

    distpath = "./dist"
    appimage = "PCartLoader.AppImage"
    zsync = "PCartLoader.AppImage.zsync"
    os.makedirs(distpath, exist_ok=True)
    if os.path.exists(appimage):
      os.rename(appimage, os.path.join(distpath, appimage))
    if os.path.exists(zsync):
      os.rename(zsync, os.path.join(distpath, zsync))

    if args.launch:
      proc = subprocess.Popen([os.path.join(distpath, appimage)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
      for line in proc.stdout:
          print(line, end="", flush=True)
      sys.exit(proc.returncode)

if __name__ == "__main__":
    main()
