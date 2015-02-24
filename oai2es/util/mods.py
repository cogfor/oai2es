from urlparse import urlparse
import re


def getUrl(url):
    """Select url from header"""
    # does not contain url
    if len(url) == 1:
        return ""
    else:
        return url[1]


def getID(url):
    """Get the ID"""
    # e.g. http://www.surfsharekit.nl:8080/fedora/get/smpid:12825/DS1/
    # get path
    #url = getUrl(url)
    print "URL = ", url
    #return urlparse(url).path.split('/')[2].split(':')[1]
    #return urlparse(url).path[-10:-5]
    return str(re.findall(r'[0-9]{5}', url)[0])
