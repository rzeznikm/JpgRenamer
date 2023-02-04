import os
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

DIR = r""
ROOT_DIR = r"D:\Foto\2022"
PREFIX = "IMG_"
POSTFIX = ".jpg"


def getExif(path):
    exifdata = Image.open(path)._getexif()
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        print(f"{tag_id} {tag:25}: {data}")


def getCreationDate(path):
    try:
        return Image.open(path)._getexif()[36867]
    except Exception as e:
        print(str(e))
        return datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y%m%d_%H%M%S")

def getModel(path):
    return Image.open(path)._getexif()[272]

def createNameFromExif(path):
    exifinfo = Image.open(path)._getexif()
    try:
        creationDate = exifinfo[36867]
    except Exception as e:
        print(str(e))
        creationDate = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y%m%d_%H%M%S")
    model = exifinfo[271]
    return creationDate.replace(":", "").replace(" ", "_") + "_" + model.replace(" ", "")


def renameJpgInDir(dir):
    for file in os.listdir(dir):
        if file.lower().endswith(".jpg"):
            try:
                baseName = createNameFromExif(os.path.join(dir, file))
            except Exception as e:
                print(str(e))
                continue
            new_name = PREFIX + baseName + POSTFIX
            counter = 1;
            while (os.path.isfile(os.path.join(dir, new_name))) :
                new_name = PREFIX + baseName + "_" + str(counter) + POSTFIX
                counter = counter + 1
            try:
                os.rename(os.path.join(dir, file), os.path.join(dir, new_name))
            except Exception as e:
                print(e)
                continue

def renameJpgRecusive(root_path):
    for directory, subdirectories, files in os.walk(root_path):
        print("Working in:")
        print(directory)
        renameJpgInDir(directory)


if __name__ == "__main__":
    #renameJpgInDir(DIR)
    renameJpgRecusive(ROOT_DIR)
    print("Finished")

