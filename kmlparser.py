#!/usr/bin/env python
# encoding: utf-8
"""
kmlparser.py

Created by John Wesonga on 2011-11-03.

"""

import sys
import os
import csv
import getpass
from optparse import OptionParser

from BeautifulSoup import BeautifulSoup
import gdata.docs.service
import gdata.docs.data



class KmlParser(object):
	def __init__(self,kmlfile,csvfile):
		self.kmlfile = kmlfile
		self.csvfile = csvfile
		self.outputData = []
		
	def parse_file(self):
		try:
			handler = open(self.kmlfile).read()
			soup = BeautifulSoup(handler)
			for message in soup.findAll('placemark'):
				imageData = {}
				msg_attrs = dict(message.attrs)
				coordinates= message.find('coordinates')
				imageData['geometry'] = '<LineString>' + str(coordinates) + '</LineString>'
				namex = message.findAll('name')
				for name in namex:
					text = name.find(text=True)
					print text
					imageData['name'] = text
				self.outputData.append(imageData)
			print self.outputData
		except IOError as (errno, strerror):
			print "I/O error({0}): {1}".format(errno, strerror)
		
		
	
	def write_csv(self):
		output_file= os.getcwd() + '/' + self.csvfile
		try:
			out=open(output_file,'w')
			print 'Writing output to file ' + str(output_file)
			try:
				fieldnames=sorted(self.outputData[0].keys())
				fieldnames.reverse()
				writer = csv.DictWriter(out,dialect='excel', fieldnames=fieldnames, extrasaction='ignore', quoting=csv.QUOTE_NONNUMERIC)
				headers=dict((n, n) for n in fieldnames)
				writer.writerow(headers)
				for row in self.outputData:
					writer.writerow(row)
			finally:
				out.close()
		except IOError as (errno, strerror):
			print "I/O error({0}): {1}".format(errno, strerror)
		return output_file
		
		
	def upload(self,output_file):
		print 'This will upload your CSV file to the google account you specify.\n'
		
		email=raw_input('Please enter your gmail email address: ')
		password=getpass.getpass('Please enter your gmail password: ')
		client = gdata.docs.service.DocsService()
		client.ClientLogin(email, password, 'kmltocsv')
		uploaded_filename=self.csvfile[0:-4]
		ms = gdata.data.MediaSource(file_path=output_file,
		                            content_type=gdata.docs.service.SUPPORTED_FILETYPES['TXT'])
		entry = client.Upload(ms, uploaded_filename)
		print 'FIle uploaded ' % ()
	

	

def main():
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="kmlfile",
	                  help="KML file to be parsed", metavar="FILE")
	parser.add_option("-d", "--output", dest="csvfile",
					   help="CSV output file", metavar="FILE")				
	(options, args) = parser.parse_args()
	if not options.kmlfile:
		print "please type python kmlparser.py --file=[kmlfilename] --output=[csvfilename]"
	elif not options.csvfile:
		print "please type python kmlparser.py --file=[kmlfilename] --output=[csvfilename]"
	else:
		kmlparser=KmlParser(kmlfile=options.kmlfile, csvfile=options.csvfile)
		kmlparser.parse_file()
		upload_file=kmlparser.write_csv()
		kmlparser.upload(upload_file)
		
	
if __name__ == '__main__':
	main()

