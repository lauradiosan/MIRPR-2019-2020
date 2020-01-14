import os, shutil

rootdir = '.'

for subdir, dirs, files in os.walk(rootdir):
    try:
        subdir.index("inference")
        shutil.rmtree(subdir)
    except Exception:
        pass