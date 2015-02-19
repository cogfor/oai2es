from lxml import etree
from lxml.etree import SubElement
from oai2es import common


class MetadataRegistry(object):
    """A registry that contains readers and writers of metadata.

    a reader is a function that takes a chunk of (parsed) XML and
    returns a metadata object.

    a writer is a function that takes a takes a metadata object and
    produces a chunk of XML in the right format for this metadata.
    """
    def __init__(self):
        self._readers = {}
        self._writers = {}
        
    def registerReader(self, metadata_prefix, reader):
        self._readers[metadata_prefix] = reader

    def registerWriter(self, metadata_prefix, writer):
        self._writers[metadata_prefix] = writer

    def hasReader(self, metadata_prefix):
        return metadata_prefix in self._readers
    
    def hasWriter(self, metadata_prefix):
        return metadata_prefix in self._writers
    
    def readMetadata(self, metadata_prefix, element):
        """Turn XML into metadata object.

        element - element to read in

        returns - metadata object
        """
        return self._readers[metadata_prefix](element)

    def writeMetadata(self, metadata_prefix, element, metadata):
        """Write metadata as XML.
        
        element - ElementTree element to write under
        metadata - metadata object to write
        """
        self._writers[metadata_prefix](element, metadata)

global_metadata_registry = MetadataRegistry()


class Error(Exception):
    pass


class MetadataReader(object):
    """A default implementation of a reader based on fields.
    """
    def __init__(self, fields, namespaces=None):
        self._fields = fields
        self._namespaces = namespaces or {}

    def __call__(self, element):
        map = {}
        # create XPathEvaluator for this element
        xpath_evaluator = etree.XPathEvaluator(element, 
                                               namespaces=self._namespaces)
        
        e = xpath_evaluator.evaluate
        # now extra field info according to xpath expr
        for field_name, (field_type, expr) in self._fields.items():
            if field_type == 'bytes':
                value = str(e(expr))
            elif field_type == 'bytesList':
                value = [str(item) for item in e(expr)]
            elif field_type == 'text':
                # make sure we get back unicode strings instead
                # of lxml.etree._ElementUnicodeResult objects.
                value = unicode(e(expr))
            elif field_type == 'textList':
                # make sure we get back unicode strings instead
                # of lxml.etree._ElementUnicodeResult objects.
                value = [unicode(v) for v in e(expr)]
            else:
                raise Error, "Unknown field type: %s" % field_type
            map[field_name] = value
        return common.Metadata(element, map)

oai_dc_reader = MetadataReader(
    fields={
        'title':       ('textList', 'oai_dc:dc/dc:title/text()'),
        'creator':     ('textList', 'oai_dc:dc/dc:creator/text()'),
        'subject':     ('textList', 'oai_dc:dc/dc:subject/text()'),
        'description': ('textList', 'oai_dc:dc/dc:description/text()'),
        'publisher':   ('textList', 'oai_dc:dc/dc:publisher/text()'),
        'contributor': ('textList', 'oai_dc:dc/dc:contributor/text()'),
        'date':        ('textList', 'oai_dc:dc/dc:date/text()'),
        'type':        ('textList', 'oai_dc:dc/dc:type/text()'),
        'format':      ('textList', 'oai_dc:dc/dc:format/text()'),
        'identifier':  ('textList', 'oai_dc:dc/dc:identifier/text()'),
        'source':      ('textList', 'oai_dc:dc/dc:source/text()'),
        'language':    ('textList', 'oai_dc:dc/dc:language/text()'),
        'relation':    ('textList', 'oai_dc:dc/dc:relation/text()'),
        'coverage':    ('textList', 'oai_dc:dc/dc:coverage/text()'),
        'rights':      ('textList', 'oai_dc:dc/dc:rights/text()'),
    },
    namespaces={
        'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
        'dc': 'http://purl.org/dc/elements/1.1/',
    }
)

custom_namespaces = {
    'oai-pmh': 'http://www.openarchives.org/OAI/2.0/',
    'didl': 'urn:mpeg:mpeg21:2002:02-DIDL-NS',
    'dii': 'urn:mpeg:mpeg21:2002:01-DII-NS',
    'dip': 'urn:mpeg:mpeg21:2005:01-DIP-NS',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'oai_dc': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'dcterms': 'http://purl.org/dc/terms/',
    'mods': 'http://www.loc.gov/mods/v3',
    'marc': 'http://www.loc.gov/MARC21/slim',
    'dai': 'info:eu-repo/dai http://www.surfgroepen.nl/sites/oai/metadata/Shared%20Documents/dai-extension.xsd',
    'xlink': 'http://www.w3.org/1999/xlink',
#    'hbo': 'http://wiki.surf.nl/download/attachments/11600294/hboMODSextension.xsd'
}

#didl:DIDL/didl:Item/didl:Item/didl:Component/didl:Resource/mods:mods/mods:titleInfo/mods:title/text()
mods_reader = MetadataReader(
    fields={
        'id':           ('textList', 'didl:DIDL/didl:Item/didl:Descriptor/didl:Statement/dii:Identifier/text()'),
        'url':           ('textList', 'didl:DIDL/didl:Item/didl:Item/didl:Descriptor/didl:Statement/dii:Identifier/text()'),
        'title':        ('textList', 'didl:DIDL/didl:Item/didl:Item/didl:Component/didl:Resource/mods:mods/mods:titleInfo/mods:title/text()'),
        'genre':        ('textList', 'didl:DIDL/didl:Item/didl:Item/didl:Component/didl:Resource/mods:mods/mods:genre/text()'),
        'name':         ('textList', 'didl:DIDL/didl:Item/didl:Item/didl:Component/didl:Resource/mods:mods/mods:name[@type="personal"]/*[@type="family" or @type="given"]/text()'),
        'affiliation':  ('textList', 'didl:DIDL/didl:Item/didl:Item/didl:Component/didl:Resource/mods:mods/mods:name/mods:affiliation/text()'),
        'abstract':     ('textList', 'didl:DIDL/didl:Item/didl:Item/didl:Component/didl:Resource/mods:mods/mods:abstract/text()'),
        'language':     ('textList', 'didl:DIDL/didl:Item/didl:Item/didl:Component/didl:Resource/mods:mods/mods:language/mods:languageTerm/text()'),
        'topics':       ('textList', 'didl:DIDL/didl:Item/didl:Item/didl:Component/didl:Resource/mods:mods/mods:subject/mods:topic/text()'),
 #       'corporate':    ('textList', 'didl:DIDL/didl:Item/didl:Item/didl:Component/didl:Resource/mods:mods/mods:extension/hbo:hbo/hbo:name[@type="corporate"/*/text()')
    },
    # namespaces={
    #     'mods': 'http://www.loc.gov/mods/v3',
    #     'didl': 'urn:mpeg:mpeg21:2002:02-DIDL-NS',
    # }
    namespaces=custom_namespaces
)

