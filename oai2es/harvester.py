import urllib
import urllib2

import datetime
import codecs


# function for return dom response after parsing oai-pmh URL
from xml.dom.minidom import parseString
import parser


def oaipmh_response(URL):
    file = urllib2.urlopen(URL)
    data = file.read()
    file.close()

    dom = parseString(data)
    return dom


# function for getting value of resumptionToken after parsing oai-pmh URL
def oaipmh_resumptionToken(URL):
    file = urllib2.urlopen(URL)
    data = file.read()
    file.close()

    dom = parseString(data)
    print "START: " + str(datetime.datetime.now())
    return dom.getElementsByTagName('resumptionToken')[0].firstChild.nodeValue


# function for writing to output files
def write_xml_file(inputData, outputFile):
    with codecs.open(outputFile, "w", "utf-8-sig") as oaipmhResponse:

    # Ensure text is UTF-8
    #content = unicode(inputData.strip(codecs.BOM_UTF8), 'utf-8')
    #parser.parse(StringIO.StringIO(content))
    #content = inputData.encode('ascii', 'ignore')
        oaipmhResponse.write(inputData)
        oaipmhResponse.close()
        print "END: " + str(datetime.datetime.now())


# main code
baseURL = 'http://hhs.surfsharekit.nl:8080/oai/hhs/'
getRecordsURL = str(baseURL + '?verb=ListRecords&metadataPrefix=mods')

# initial parse phase
resumptionToken = oaipmh_resumptionToken(getRecordsURL)  # get initial resumptionToken
print "Resumption Token: " + resumptionToken
outputFile = 'page-0.xml'  # define initial file to use for writing response
write_xml_file(oaipmh_response(getRecordsURL).toxml(), outputFile)

# loop parse phase
pageCounter = 1
while resumptionToken != "":
    print "URL ENCODED TOKEN: " + resumptionToken
    resumptionToken = urllib.urlencode({'resumptionToken': resumptionToken})  # create resumptionToken URL parameter
    print "Resumption Token: " + resumptionToken
    getRecordsURLLoop = str(baseURL + '?verb=ListRecords&' + resumptionToken)
    oaipmhXML = oaipmh_response(getRecordsURLLoop).toxml()
    outputFile = 'page-' + str(pageCounter)  # create file name to use for writing response
    write_xml_file(oaipmhXML, outputFile)  # write response to output file

    resumptionToken = oaipmh_resumptionToken(getRecordsURLLoop)
    pageCounter += 1  # increment page counter


