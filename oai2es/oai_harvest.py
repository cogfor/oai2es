# coding: utf-8
from datetime import date
from oai2es.metadata import oai_dc_reader, mods_reader, MetadataRegistry
from oaipmh.client import Client
from pdfthumb import getThumb
from urlparse import urlparse
from oai2es.util.mods import *

import elasticsearch

URL = 'http://hhs.surfsharekit.nl:8080/oai/hhs/'

registry = MetadataRegistry()
registry.registerReader('mods', mods_reader)
client = Client(URL, registry)

# Round-robin between two nodes:
es = elasticsearch.Elasticsearch(["http://search1.cogfor.com:9200", "http://search2.cogfor.com:9200"])


def _getNames(names):
    """Concat family and given name"""
    si = iter(names)
    return [c+", "+next(si, '') for c in si]


def _getDate(datestamp):
    """Return year, month, day"""
    date = datestamp.split[" "][0].split["-"]
    year = date[0]
    month = date[1]
    day = date[2]
    return year, month, day


def esIndex(record, datestamp):
    """Put record in ElasticSearch"""
    es.index(
        index="hhs",
        doc_type="oai",
        id=record['id'],
        body={
            "title": record['title'],
            "url": getUrl(record['url']),
            "genre": record['genre'],
            "name": _getNames(record['name']),
            "language": record['language'],
            "topics": record['topics'],
            "abstract": record['abstract'],
            "date": datestamp,
        }
    )

for record in client.listRecords(metadataPrefix='mods'):
    #print record
    if record[1] is not None:
        datestamp = record[0].datestamp()
        record = record[1].getMap()

        print datestamp, record
        #print {record['title']}, {record['url'][1]}, record['genre'], ', '.join(record['name']), record['language'], ', '.join(record['topics']), record['abstract']

        doc_url = getUrl(record['url'])
        if doc_url is not None:
            getThumb(doc_url)
        #esIndex(record, datestamp)
        #raw_input("Press Enter to continue...")
