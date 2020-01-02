from lib.sql import initialize
from lib.cmd import Parser
from img.editor import ImageMagick
from lib.settings import BANNER


def main():
    opt = Parser().optparse()
    cursor = initialize()
    Parser().check_args(opt, cursor)

    print(BANNER)

    if opt.workingFile is None:
        print("You must pass a filename to work with")
        exit(1)
    else:
        try:
            open(opt.workingFile)
        except IOError:
            print("the file failed to open, does it exist?")
            exit(1)
        magic = ImageMagick(
            opt.workingFile, cursor, watermark=opt.watermarkString,
            font_size=opt.fontSize, no_save=opt.noSaveDatabase, sent_to=opt.recvName,
            watermark_color=opt.watermarkColor, custom_watermark_color=opt.customWaterMarkColor
        )
        if opt.doExifWipe:
            print("only wiping exif data from file '{}'".format(opt.workingFile))
            new_filename = magic.wipe_exif()
            print("exif data wiped and new file saved as '{}'".format(new_filename))
            exit(1)
        else:
            print("adding watermark and wiping exif data from image '{}'".format(opt.workingFile))
            new_filename = magic.make_watermark()
            print("watermark added and exif data wiped from file, file saved as '{}'".format(new_filename))
            exit(1)

