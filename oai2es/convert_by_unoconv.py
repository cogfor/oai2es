from urllib2 import urlopen
from wand.image import Image
import os.path
from os import remove
from oai2es.util.mods import *
import magic


# login
#http://baasbox-cog4.rhcloud.com/login -d "username=admin" -d "password=xvbBk01b8S" -d "appcode=1234567890"

# add asset
# curl 'http://baasbox --form file=@16286.pdf --form name=16286.pdf --form meta='{"name": 16286, "type": "original"}' -H X-BB-SESSION:7fbaae32-992a-49f1-a212-fe9f9b780ee4

# retrieve asset
# curl 'http://baasbox-cog4.rhcloud.com/asset/16286.pdf' -H X-BAASBOX-APPCODE:1234567890


class Asset(object):
    def __init__(self, url):
        self.url = url
        self.id = ""
        self.mage = magic.Magic(flags=magic.MAGIC_MIME_ENCODING)
        self.mime = ""


def getOriginalFile(url):
    """ Download asset from url and store with correct extension"""
    # does url exist?
    if url is None or url is "":
        return




def getThumb(url):
    # checks
    # does url exist?
    if url is None or url is "":
        return

    print "Download from ", url
    PDF_DIR = 'pdfs/'
    THUMB_DIR = 'thumbs/'

    id = getID(url)

    #BASE_URL = 'http://www.surfsharekit.nl:8080/fedora/get/smpid:'
    id = getID(url)
    print "ID ", id
    #URL = BASE_URL + id + '/DS1/'

    PDF_FILE = PDF_DIR + id + '.pdf'
    THUMB_FILE = THUMB_DIR + id + '.jpg'

    print "Download from ", url

    if not os.path.exists(PDF_FILE):
        # Download pdf from repository
        response = urlopen(url)
        try:
            with open(PDF_FILE, "w") as pdffile:
                pdfdata = response.read()
                if 'pdf' not in magic.from_buffer(pdfdata, mime=True):
                    print "This is not PDF"
                    response.close()
                    pdffile.close()
                    remove(PDF_FILE)
                    return
                pdffile.write(pdfdata)
        finally:
            response.close()


    # Converting first page into JPG
    try:
        print PDF_FILE
        with Image(filename=PDF_FILE+'[0]') as img:
            img.transform(resize='640x480>')
            img.save(filename=THUMB_FILE)
    except Exception:
        pass




