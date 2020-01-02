import os
import random
import base64
import datetime


class NoEncryptionKeyPresent(Exception): pass


# the version
VERSION = "0.1"

# sexy banner
BANNER = """
  _____      _____    _____      ______ 
 |_   _|   / ____|   |_   _|    |  ____|
   | |     | (___      | |      | |__   
   | |      \\___ \\     | |      |  __|  
  _| |_     ____) |   _| |_     | |____ 
 |_____|nfo|_____/lut|_____|mage|______|ditor
version({})\n""".format(VERSION)

# the default watermark to use
DEFAULT_WATERMARK = "ISIE {}".format(datetime.datetime.today())

# the home path where the database sits
ISIE_HOME = "{}/.isie".format(os.path.expanduser("~"))

# the database file path
ISIE_DATABASE_FILE_PATH = "{}/isie.sqlite".format(ISIE_HOME)


def show_cache(cached_data):
    """
    output your burn book
    """
    if cached_data is not None:
        if len(cached_data) == 0:
            print("No image data cached into the database")
            exit(1)
        else:
            print("{}\n{}ID#:{}|\t{}Watermark:{}\t|\t{}Sent To:{}\t|\tTimestamp:\n{}".format(
                "-" * 106, " " * 2, " " * 2, " " * 7, " " * 7, " " * 4, " " * 4, "-" * 106
            ))
            output_template = "{0:7} | {1:37} | {2:29} | {3:60}"
            for item in cached_data:
                id_num, _, timestamp, watermark, sent_to, _ = item
                print(output_template.format(
                    id_num, watermark, sent_to, timestamp
                ))


def resave_image(id_num, filename, cache):
    """
    save the base64 data of the image back into an image
    """
    for item in cache:
        if item[0] == id_num:
            if not filename.endswith(item[-1]):
                filename = filename + "." + item[-1]
            base64_data = item[1]
            with open(filename, 'a+') as data:
                data.write(base64.b64decode(base64_data))
    return filename


def random_filename_string(length=13):
    import string

    f = []
    acceptable = string.ascii_letters
    for _ in range(length):
        f.append(random.choice(acceptable))
    return "".join(f)
