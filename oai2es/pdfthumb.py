from urllib2 import urlopen
from wand.image import Image
import os.path
from oai2es.util.mods import *
import magic
import glob
import logging
import subprocess
import shutil

logger = logging.getLogger('thumbnailer')


def write(id, type, stream):
    """
    Writes a data stream to a file
    """
    filename = id + "." + type
    logger.info("[INFO] Saving file %s " % filename)
    with open(filename, 'w') as outfile:
        outfile.write(stream)
    return filename


def make_pdf_thumb(inputfile, outputfile=None, size="640x480>"):
    """
    Makes a thumbnail from a pdf file
    """
    # Converting first page into JPG
    if outputfile is None:
        outputfile = "thumb_" + inputfile
    try:
        # get first page
        with Image(filename=inputfile+'[0]') as img:
            img.transform(resize=size)
            img.save(filename=outputfile)
    except Exception:
        logger.error("[ERROR] Some unknown error creating a pdf thumb occurred")


def convert_to_pdf(inputfile, outputfile=None):
    """
    Convert an office file to pdf
    """
    if outputfile is None:
        outputfile = inputfile + ".pdf"
    p = subprocess.Popen(['unoconv', '--stdout', inputfile], stdout=subprocess.PIPE)
    with open(outputfile, 'w') as output:
        shutil.copyfileobj(p.stdout, output)


def getThumb(url, id=None):
    ORG_DIR = 'pdfs/'
    THUMB_DIR = 'thumbs/'

    # checks
    # does url exist?
    if url is None or url is "":
        return

    if id is None:
        id = getID(url)

    logger.info("[INFO] Download doc with id: %s from %s" % id, url)

    # identify type of file from streaming buffer

    # TODO: don't download if file already available
    mage = magic.Magic(flags=magic.MAGIC_MIME_ENCODING)

    ORG_FILE = ORG_DIR + id
    THUMB_FILE = THUMB_DIR + id
    org_filespec = ORG_FILE + ".*"
    #thumb_filespec = THUMB_FILE + ".*"

    # doc starting with id already downloaded?
    if not os.path.exists(glob.glob(org_filespec)):
        # Download document from repository
        response = urlopen(url)
        docdata = response.read()
        doctype = mage.id_buffer(docdata, mime=True)
        if 'pdf' in doctype:
            filename = write(id, type="pdf", stream=docdata)
            make_pdf_thumb(inputfile=filename, outputfile=id + "_thumb.jpg")

        elif 'doc' in doctype:
            write(id, type="doc", stream=docdata)

        elif 'docx' in doctype:
            write(id, type="docx", stream=docdata)

        elif 'ppt' in doctype:
            write(id, type="ppt", stream=docdata)

        else:
            print "This is an unknown filetype"
            logger.error("[WARN] Found unknown filetype for id: %s" % id)

        response.close()
        docdata.close()