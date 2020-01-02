import base64

from lib.settings import (
    NoEncryptionKeyPresent,
    DEFAULT_WATERMARK
)
from lib.sql import insert

from PIL import (
    Image,
    ImageDraw,
    ImageFont
)


class ImageMagick(object):

    colors = {
        "black": (0, 0, 0),
        "yellow": (152, 116, 18),
        "green": (0, 0, 100),
        "blue": (0, 100, 0),
        "red": (100, 0, 0),
        "white": (100, 100, 100)
    }

    def __init__(self, path, cursor, **kwargs):
        self.path = path
        self.cursor = cursor
        self.watermark = kwargs.get("watermark", DEFAULT_WATERMARK)
        self.do_encrypt = kwargs.get("do_encrypt", False)
        self.font_size = kwargs.get("font_size", 12)
        self.sent_to = kwargs.get("sent_to", "N/A")
        self.no_save = kwargs.get("no_save", False)
        self.custom_watermark = kwargs.get("custom_watermark_color", None)
        self.watermark_color = kwargs.get("watermark_color", "black")
        if self.do_encrypt:
            self.encryption_key = kwargs.get("encryption_key", None)
            if self.encryption_key is None:
                raise NoEncryptionKeyPresent()

    def __get_filename(self, watermarked=False, exifed=False):
        """
        rename the original file so that we have the output file with `ISIE_` prepended to it
        """
        original_filename = self.path.split("/")[-1]
        if watermarked:
            return "ISIE_watermarked_{}".format(original_filename)
        elif exifed:
            return "ISIE_no_exif_{}".format(original_filename)
        else:
            return "ISIE_{}".format(original_filename)

    def __magick(self):
        """
        image magic using PIL
        """
        return Image.open(self.path)

    def __get_meta(self):
        """
        extract the metadata from the image along with get the margin length
        """
        data = self.__magick()
        return {"attrib": data.size, "margin": 5}

    def __get_filetype(self):
        """
        get the file type so that we can save it again from the database
        """
        filename = self.__get_filename()
        return filename.split(".")[-1]

    def save_image_in_db(self):
        """
        save the image in a cipher for "future use"
        """
        with open(self.path) as data:
            base64_image_data = base64.b64encode(data.read())
            try:
                insert(self.cursor, base64_image_data, self.watermark, self.__get_filetype(), sent_to=self.sent_to)
                return True
            except Exception:
                return False

    def wipe_exif(self):
        image = self.__magick()
        save_file = self.__get_filename(exifed=True)
        data = list(image.getdata())
        no_exif = Image.new(image.mode, image.size)
        no_exif.putdata(data)
        no_exif.save(save_file)
        if not self.no_save:
            self.save_image_in_db()
        return save_file

    def make_watermark(self):
        """
        add a watermark to the image along with wipe all exif data out of the image
        """
        data = self.__magick()
        save_filename = self.__get_filename(watermarked=True)
        meta_data = self.__get_meta()
        draw = ImageDraw.Draw(data)
        font = ImageFont.truetype("arial.ttf", self.font_size)
        width, height = draw.textsize(self.watermark, font)
        coord_x = meta_data["attrib"][0] - width - meta_data["margin"]
        coord_y = meta_data["attrib"][1] - height - meta_data["margin"]
        if self.custom_watermark is None:
            fill_color = self.colors[self.watermark_color]
        else:
            fill_color = tuple(self.custom_watermark)
        draw.text((coord_x, coord_y), self.watermark, fill=fill_color, font=font)
        data.save(save_filename)
        if not self.no_save:
            self.save_image_in_db()
        return save_filename

    def encrypt_image(self):
        """
        encrypt the image for sharing
        """
        pass
