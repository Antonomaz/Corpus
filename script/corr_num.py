from lxml import etree
import glob
import argparse
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("file", help="file to process")
args = arg_parser.parse_args()

ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

def num(xml):
    pb = xml.xpath('//tei:pb', namespaces=ns)
    n = 1
    for x in pb:
        x.attrib["n"] = str(n)
        n+=1
    return xml.write(args.file, pretty_print=True, encoding="utf-8", method="xml", xml_declaration=True)


if __name__ == "__main__":
    parser = etree.XMLParser(remove_blank_text=True)
    doc = etree.parse(args.file, parser)
    num(doc)