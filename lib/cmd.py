import sys
import argparse

import lib.sql
import lib.settings


class Parser(argparse.ArgumentParser):

    def __init__(self):
        super(Parser, self).__init__()

    @staticmethod
    def optparse():
        parser = argparse.ArgumentParser(usage="isie -[f|p] FILE [-e|w] WATERMARK [--no-save] [-r|s]")

        mandatory = parser.add_argument_group("mandatory arguments")
        mandatory.add_argument(
            "-f", "-p", "--file", "--path", metavar="FILENAME", dest="workingFile", default=None,
            help="Pass a file path to work with (*default=None)"
        )
        mandatory.add_argument(
            "-e", "--exif", action="store_true", dest="doExifWipe", default=False,
            help="Wipe the exif data from a file and save it (*default=False)"
                 "NOTE: adding a watermark will also wipe the exif data from the image"
        )
        mandatory.add_argument(
            "-w", "--watermark", metavar="WATERMARK-STRING", default=None, dest="watermarkString",
            help="Pass a string to use as the watermark (*default={})".format(lib.settings.DEFAULT_WATERMARK)
        )

        database = parser.add_argument_group("database arguments")
        database.add_argument(
            "-c", "--cache", dest="viewCache", action="store_true", default=False,
            help="View the data currently cached inside the database"
        )
        database.add_argument(
            "--no-save", dest="noSaveDatabase", action="store_true", default=False,
            help="Do not store the edited file into the database (*default=False)"
        )
        database.add_argument(
            "-d", "--dump-b64", type=int, metavar="DATABASE-ID-#", default=None, dest="dumpBase64",
            help="Used in conjunction with `-n/--name` pass an ID# found from using"
                 "`-c/-cache` to resave the file (*default=None)"
        )
        database.add_argument(
            "-n", "--name", metavar="FILENAME", default=None, dest="saveFileName",
            help="Used in conjunction with `-d/--dump-b64` pass a filename for the created file (*default=random)"
        )

        misc = parser.add_argument_group("misc arguments")
        misc.add_argument(
            "-r", "--recipient-name", dest="recvName", metavar="RECIPIENTS-NAME", default="N/A",
            help="Pass this to add a name of the person receiving the picture into the database (*default=N/A)"
        )
        misc.add_argument(
            "-s", "--font-size", type=int, dest="fontSize", default=12, metavar="FONT-SIZE (PIXELS)",
            help="Pass this to control the font size of the watermark (*default=12)"
        )
        misc.add_argument(
            "--watermark-color", default="black", choices=('black', 'yellow', 'green', 'blue', 'red', 'white'),
            dest="watermarkColor", help="Choose a preset watermark color (*default=black)"
        )
        misc.add_argument(
            "--custom-watermark", default=None, nargs=3, type=int, dest="customWaterMarkColor",
            help="Pass the RGB 3 color spectrum of a watermark color (*default=None)",
            metavar=("R", "G", "B")
        )
        if len(sys.argv[1:]) == 0:
            parser.print_help()
            exit(1)
        else:
            return parser.parse_args()

    @staticmethod
    def check_args(opts, cursor):
        if opts.viewCache:
            lib.settings.show_cache(lib.sql.fetch(cursor))
            exit(1)
        if opts.watermarkString is None:
            opts.watermarkString = lib.settings.DEFAULT_WATERMARK
        if opts.saveFileName is not None and opts.dumpBase64 is None:
            print(
                "You must pass the ID number you find from using the `-c/--cache` flag as an "
                "argument to the `-d/--dump-b64` flag"
            )
            exit(1)
        if opts.saveFileName is None and opts.dumpBase64 is not None:
            opts.saveFileName = lib.settings.random_filename_string()
            print("random filename generated: {}".format(opts.saveFileName))
            lib.settings.resave_image(opts.dumpBase64, opts.saveFileName, lib.sql.fetch(cursor))
            print("file saved successfully")
            exit(1)
