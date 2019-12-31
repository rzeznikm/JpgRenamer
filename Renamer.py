import os
from PIL import Image
from datetime import datetime

DIR = "path to Dir"

def getCreationDate(path):
    try:
        return Image.open(path)._getexif()[36867]
    except Exception as e:
        print(str(e))
        return datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y%m%d_%H%M%S")

def renameJpgInDir(dir):
    for file in os.listdir(dir):
        if file.lower().endswith(".jpg"):
            creation = getCreationDate(os.path.join(dir, file))
            new_name = "IMG_" + creation.replace(":", "").replace(" ", "_") + ".jpg"
            print(file + "->" + new_name)
            try:
                os.rename(os.path.join(dir, file), os.path.join(dir, new_name))
            except OSError as e:
                print(str(e))
                new_name = "IMG_" + creation.replace(":", "").replace(" ", "_") + "_.jpg"
                os.rename(os.path.join(dir, file), os.path.join(dir, new_name))
                continue

if __name__ == "__main__":
    renameJpgInDir(DIR)