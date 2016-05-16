import socket
import sys
from lxml import etree
from collections import OrderedDict

# parse input sentence and return alpino output as an xml element tree
def alpino_parse(sent, host='zardoz.service.rug.nl', port=42424):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((host,port))
	sent = sent + "\n\n"
	sentbytes= sent.encode('utf-8')
	s.sendall(sentbytes)
	bytes_received= b''
	while True:
		byte = s.recv(8192)
		if not byte:
			break
		bytes_received += byte
	# print(bytes_received.decode(’utf-8’), file=sys.stderr)
	xml = etree.fromstring(bytes_received)
	return xml

def tree_yield(xml):
    leaves = xml.xpath('descendant-or-self::node[@word]')
    dic = OrderedDict()
    words = []
    for l in leaves:
        pos = l.attrib["pos"]
        word = l.attrib["word"]
        dic[pos] = word
    return dic



def main():
	xml = alpino_parse("Door wie is de geboorteplaats van Usain Bolt?")
	print(xml)
	result = (tree_yield(xml))
	print(result)
	print(result['pron'])


main()
