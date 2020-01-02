# ISIE

ISIE (InfoSlut Image Editor) is an image editing tool designed specifically for [The BADASS Army](https://twitter.com/theBADASS_army). The goal of this program is to create an efficient and simple way to remove exif data and add watermarks to images. 

# Features

 - Exif data wiping (just exif)
 - Watermark adding and exif data wiping
 - Database integration support, saves the image as base64 encoded along with a timestamp the image was created, image type, and the recipients name
 - Ability to resave the image from the base64 encoded image into a file
 - Ability to add custom watermark strings
 - Ability to add a custom watermark string color
 - Ability to view all the database cache
 - Support bmp, jpg, jpeg, and png images

# Usage:

Using it is actually extremely simple, for simplicity sake I have added a list of possible arguments;

```
usage: isie -[f|p] FILE [-e|w] WATERMARK [--no-save] [-r|s]

optional arguments:
  -h, --help            show this help message and exit

mandatory arguments:
  -f FILENAME, -p FILENAME, --file FILENAME, --path FILENAME
                        Pass a file path to work with (*default=None)
  -e, --exif            Wipe the exif data from a file and save it
                        (*default=False)NOTE: adding a watermark will also
                        wipe the exif data from the image
  -w WATERMARK-STRING, --watermark WATERMARK-STRING
                        Pass a string to use as the watermark (*default=ISIE
                        2020-01-02 17:03:48.761540)

database arguments:
  -c, --cache           View the data currently cached inside the database
  --no-save             Do not store the edited file into the database
                        (*default=False)
  -d DATABASE-ID-#, --dump-b64 DATABASE-ID-#
                        Used in conjunction with `-n/--name` pass an ID# found
                        from using`-c/-cache` to resave the file
                        (*default=None)
  -n FILENAME, --name FILENAME
                        Used in conjunction with `-d/--dump-b64` pass a
                        filename for the created file (*default=random)

misc arguments:
  -r RECIPIENTS-NAME, --recipient-name RECIPIENTS-NAME
                        Pass this to add a name of the person receiving the
                        picture into the database (*default=N/A)
  -s FONT-SIZE (PIXELS), --font-size FONT-SIZE (PIXELS)
                        Pass this to control the font size of the watermark
                        (*default=12)
  --watermark-color {black,yellow,green,blue,red,white}
                        Choose a preset watermark color (*default=black)
  --custom-watermark R G B
                        Pass the RGB 3 color spectrum of a watermark color
                        (*default=None)
```

To edit just the exif data of an image the following will do just that:
```
isie -p png-vs-jpeg.jpg -s 12 -e

  _____      _____    _____      ______ 
 |_   _|   / ____|   |_   _|    |  ____|
   | |     | (___      | |      | |__   
   | |      \___ \     | |      |  __|  
  _| |_     ____) |   _| |_     | |____ 
 |_____|nfo|_____/lut|_____|mage|______|ditor
version(0.1)

only wiping exif data from file 'png-vs-jpeg.jpg'
exif data wiped and new file saved as 'ISIE_no_exif_png-vs-jpeg.jpg'
```

To wipe the exif data and add a watermark to the image the following does that:
```
isie -p png-vs-jpeg.jpg 

  _____      _____    _____      ______ 
 |_   _|   / ____|   |_   _|    |  ____|
   | |     | (___      | |      | |__   
   | |      \___ \     | |      |  __|  
  _| |_     ____) |   _| |_     | |____ 
 |_____|nfo|_____/lut|_____|mage|______|ditor
version(0.1)

adding watermark and wiping exif data from image 'png-vs-jpeg.jpg'
watermark added and exif data wiped from file, file saved as 'ISIE_watermarked_png-vs-jpeg.jpg'
```

To control the watermark string you can pass the `-w` flag (the `-s` flag controls the font size):
```
python isie -p png-vs-jpeg.jpg -w "this is a watermark string" -s 25

  _____      _____    _____      ______ 
 |_   _|   / ____|   |_   _|    |  ____|
   | |     | (___      | |      | |__   
   | |      \___ \     | |      |  __|  
  _| |_     ____) |   _| |_     | |____ 
 |_____|nfo|_____/lut|_____|mage|______|ditor
version(0.1)

adding watermark and wiping exif data from image 'png-vs-jpeg.jpg'
watermark added and exif data wiped from file, file saved as 'ISIE_watermarked_png-vs-jpeg.jpg'
```
![ISIE_watermarked_png-vs-jpeg](https://user-images.githubusercontent.com/14183473/71698798-6e6f2e80-2d82-11ea-8b3d-43761dda12e8.jpg)

You can also control the size and the color of the watermark:
```
isie -p png-vs-jpeg.jpg -w "this is another watermark string" -s 25 --watermark-color yellow

  _____      _____    _____      ______ 
 |_   _|   / ____|   |_   _|    |  ____|
   | |     | (___      | |      | |__   
   | |      \___ \     | |      |  __|  
  _| |_     ____) |   _| |_     | |____ 
 |_____|nfo|_____/lut|_____|mage|______|ditor
version(0.1)

adding watermark and wiping exif data from image 'png-vs-jpeg.jpg'
watermark added and exif data wiped from file, file saved as 'ISIE_watermarked_png-vs-jpeg.jpg'
```
![ISIE_watermarked_png-vs-jpeg](https://user-images.githubusercontent.com/14183473/71698844-ac6c5280-2d82-11ea-9046-c63a659d3ea8.jpg)

# Installation

To install the program simply have git and python 2.7-3.x installed on your system and run:

``` 
git clone https://github.com/Ekultek/ISIE.git
cd ISIE
[sudo] python setup.py install
isie --help
```
 
# TODO:

 - Support encryption and uploading
 - More preset colors
 - More image types supported
 - More fonts
