import urllib.request
import shutil
import os
import os.path
import zipfile
import time
import sys
import traceback
from subprocess import call
import base64
from html import escape

from bs4 import BeautifulSoup
import uuid


def find_between(file):
	f = open(file, "r", encoding = "utf8")
	soup = BeautifulSoup(f, 'html.parser')
	return soup.title


def download(link, file_name):
	"""Downloads web page from Wuxiaworld and saves it into the folder where the programm is located"""
	url = urllib.request.Request(
		link,
		data=None,
		headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
			}
		)

	with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
		shutil.copyfileobj(response, out_file)
	"""Extract Text from Wuxiaworld html file and saves it into a seperate xhtml file"""


def clean(file_name_in, file_name_out, chapter_title):
	has_spoiler = None
	raw = open(file_name_in, "r", encoding="utf8")
	# raw = open('test.html', "r", encoding="utf8")
	soup = BeautifulSoup(raw, 'lxml').find(class_="content-center").p
	# chapter_title = soup.find(class_="content-center").p
	contents = soup.contents
	# chapter_title = contents[0].replace('\n\t','') + ' - ' + contents[4].replace('\n\t','')
	# chapter_title = soup.find(class_="caption clearfix")
	# chapter_title = chapter_title.find("h4")
	# chapter_title = chapter_title.text
	# soups = soup.find_all(class_="fr-view")
	# for block in soups:
	# 	if not block.has_attr('id'):
	# 		soup = block
	# 		break
	for a in soup.find_all("a"):
		a.decompose()
	raw.close()
	file = open(file_name_out + ".xhtml", "w", encoding="utf8")
	file.write('<html xmlns="http://www.w3.org/1999/xhtml">')
	file.write("\n<head>")
	file.write('\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')
	file.write("\n<title>" + chapter_title + "</title>")
	file.write("\n"+'<link href="common.css" rel="stylesheet" type="text/css"/>')
	file.write("\n</head>")
	file.write("\n<body>")
	file.write("\n<h1>" + chapter_title + "</h1>")
	file.write(str(soup).replace('<p></p>', '').replace('<p><br></p>', '').replace('<hr>', ''))
	file.write("\n</body>")
	file.write("\n</html>")
	os.remove(file_name_in)


def update_progress(progress):
	"""Displays and updates the download progress bar"""
	# This function is not used anymore but may be added later on.
	# Still fully functional though
	bar_length = 25  # Modify this to change the length of the progress bar
	status = ""
	if isinstance(progress, int):
		progress = float(progress)
	if not isinstance(progress, float):
		progress = 0
		status = "error: progress var must be float\r\n"
	if progress < 0:
		progress = 0
		status = "Halt...\r\n"
	if progress >= 1:
		progress = 1
		status = "Done...\r\n"
	block = int(round(bar_length*progress))
	text = "\rDownload Progress: [{0}] {1}% {2}".format( "#"*block + "-"*(bar_length-block), progress*100, status)
	sys.stdout.write(text)
	sys.stdout.flush()


def cover_generator(src, novel, book_name, author):
	""" This will download a cover, calculating the average complementary color
	and will wirte the chapter range on the upper half of the cover centered
	in the before mentioned color.
	Todo: Improve CCR to ignore bright parts of cover's that makes text sometimes hard to read.
	"""
	current_dir = os.path.dirname(os.path.realpath(__file__))
	storage_dir = current_dir
	if os.name == 'nt':
		storage_dir = os.path.expanduser("~") + os.sep + "wuxiaworld_export_ebook"
	if os.path.isdir(storage_dir + os.sep + "tmp") is False:
		os.makedirs(storage_dir + os.sep + "tmp")

	# urllib.request.urlretrieve(src, storage_dir + os.sep + "tmp" + os.sep + "origin_cover")
	urllib.request.urlretrieve(src, storage_dir + os.sep + "tmp" + os.sep + "cover.png")

	# file1 = open(storage_dir + os.sep + "tmp" + os.sep + "origin_cover", "rb")
	file1 = open(storage_dir + os.sep + "tmp" + os.sep + "cover.png", "rb")
	file2 = open(current_dir + os.sep + "ressources" + os.sep + "jacket.xhtml", "rb")
	file3 = open(storage_dir + os.sep + "tmp" + os.sep + "jacket.xhtml", "wb")
	cov = file1.read()
	jacket = file2.read()
	file2.close()

	covi = base64.b64encode(cov).decode('utf-8')
	ext = ""
	if covi.startswith('iVBOR') is True:
		ext = "data:image/png;base64,"
	elif covi.startswith('/9j/4AAQSkZJRgAB') is True:
		ext = "data:image/jpeg;base64,"
	jacket = jacket.decode('utf-8')
	jacket = jacket.replace('{novel}', novel)
	jacket = jacket.replace('{title}', book_name)
	jacket = jacket.replace('{author}', author)
	jacket = jacket.replace('{COVER}', ext+covi)
	file3.write(jacket.encode('utf-8'))
	file3.close()

	# try:
	# 	call([
	# 			sys.executable,
	# 			current_dir + os.sep + "cover_generator" + os.sep + "exec.py",
	# 			"-o",
	# 			storage_dir + os.sep + "tmp" + os.sep + "cover.png",
	# 			storage_dir + os.sep + "tmp" + os.sep + "jacket.xhtml"
	# 		])
	# except RuntimeError as e:
	# 	traceback.print_exc()

	# os.remove(storage_dir + os.sep + "tmp" + os.sep + "origin_cover.jpg")
	# os.remove(storage_dir + os.sep + "tmp" + os.sep + "jacket.xhtml")


def generate_name(novelname, author, chaptername, book, chapter_s, chapter_e):
	file_name = ''
	if book is None:
		file_name = novelname + " - {}-{}".format(chapter_s, chapter_e)
	else:
		if chapter_s is None:
			file_name = novelname + " - {}".format(book)
		else:
			file_name = novelname + " - {} - {}-{}".format(book, chapter_s, chapter_e)
	return author + ' - ' + file_name


def generate(html_files, novelname, author, chaptername, book, chapter_s, chapter_e):
	""" Saves downloaded xhtml files into the epub format while also
	generating the for the epub format nesessary container, table of contents,
	mimetype and content files
	ToDo: Generaliseing this part of the code and make it standalone accessible.
	SideNote: Will take a lot of time.
	"""
	current_dir = os.path.dirname(os.path.realpath(__file__))
	storage_dir = current_dir
	if os.name == 'nt':
		storage_dir = os.path.expanduser("~") + os.sep + "wuxiaworld_export_ebook"
	if os.path.isdir(storage_dir + os.sep + 'export') is False:
		os.mkdir(storage_dir + os.sep + 'export')
	file_name = ''
	if book is None:
		file_name = novelname + " - {}-{}".format(chapter_s, chapter_e)
	else:
		if chapter_s is None:
			file_name = novelname + " - {}".format(book)
		else:
			file_name = novelname + " - {} - {}-{}".format(book, chapter_s, chapter_e)
	file_name = file_name.replace(':', ',')
	epub = zipfile.ZipFile(storage_dir + os.sep + "export/" + author + ' - ' + file_name + ".epub", "w")
	# The first file must be named "mimetype"
	epub.writestr("mimetype", "application/epub+zip")

	"""
	The filenames of the HTML are listed in html_files
	We need an index file, that lists all other HTML files
	This index file itself is referenced in the META_INF/container.xml file
	"""
	epub.writestr("META-INF/container.xml", '<container version="1.0" \
		xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\
		<rootfiles>\
			<rootfile full-path="OEBPS/Content.opf" media-type="application/oebps-package+xml"/>\
		</rootfiles>\
	</container>')

	# The index file is another XML file, living per convention
	# in OEBPS/Content.xml
	uniqueid = uuid.uuid1().hex
	file1 = open("./ressources/loading_fonts.txt", "r")
	font = file1.read()
	file1.close()
	index_tpl = '''<package version="3.1"
	xmlns="http://www.idpf.org/2007/opf" unique-identifier="''' + uniqueid + '''">
			<metadata>
				%(metadata)s
			</metadata>
			<manifest>
				%(manifest)s
				<item href="cover.png" id="cover" media-type="image/png" properties="cover-image"/>
				<item href="common.css" id="commoncss" media-type="text/css"/>
				<item href="Regular.ttf" id="id1" media-type="application/font-sfnt"/>
				<item href="Bold.ttf" id="id1" media-type="application/font-sfnt"/>
				<item href="Bold-Italic.ttf" id="id1" media-type="application/font-sfnt"/>
				<item href="Italic.ttf" id="id1" media-type="application/font-sfnt"/>
			</manifest>
			<spine>
				<itemref idref="toc"/>
				%(spine)s
			</spine>
		</package>'''

	manifest = ""
	spine = ""
	metadata = '''<dc:title xmlns:dc="http://purl.org/dc/elements/1.1/">%(novelname)s</dc:title>
		<dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:ns0="http://www.idpf.org/2007/opf" ns0:role="aut"
			ns0:file-as="Unbekannt">%(author)s</dc:creator>
		<dc:language xmlns:dc="http://purl.org/dc/elements/1.1/">en</dc:language>
		<dc:identifier xmlns:dc="http://purl.org/dc/elements/1.1/">%(uuid)s"</dc:identifier>''' % {
		"novelname": escape(file_name), "author": escape(author), "uuid": uniqueid}
	toc_manifest = '<item href="toc.xhtml" id="toc" properties="nav" media-type="application/xhtml+xml"/>'

	# Write each HTML file to the ebook, collect information for the index
	for i, html in enumerate(html_files):
		basename = os.path.basename(html)
		manifest += '<item id="file_%s" href="%s" media-type="application/xhtml+xml"/>' % (i+1, basename)
		spine += '<itemref idref="file_%s" />' % (i+1)
		epub.write(html, "OEBPS/"+basename)

	# Finally, write the index
	epub.writestr("OEBPS/Content.opf", index_tpl % {
		"metadata": metadata,
		"manifest": manifest + toc_manifest,
		"spine": spine,
		})

	epub.writestr("OEBPS/toc.xhtml", generate_toc(html_files, novelname))

	epub.write(storage_dir + os.sep + "tmp/cover.png", "OEBPS/cover.png")
	try: os.remove(storage_dir + os.sep + "tmp/cover.png")
	except: {}

	file2 = open("./ressources/common.css", "r")
	file3 = open(storage_dir + os.sep + "tmp/common.css", "w")
	ccss = file2.read()
	file2.close()
	ccss = ccss.replace('<FONT>', font)
	file3.write(ccss)
	file3.close()

	epub.write(storage_dir + os.sep + "tmp/common.css", "OEBPS/common.css")
	try: os.remove(storage_dir + os.sep + "tmp/common.css")
	except: {}
	epub.write("./ressources/fonts/"+font+"/Regular.ttf", "OEBPS/Regular.ttf")
	epub.write("./ressources/fonts/"+font+"/Bold.ttf", "OEBPS/Bold.ttf")
	epub.write("./ressources/fonts/"+font+"/Bold-Italic.ttf", "OEBPS/Bold-Italic.ttf")
	epub.write("./ressources/fonts/"+font+"/Italic.ttf", "OEBPS/Italic.ttf")

	epub.close()

	# removes all the temporary files
	for x in html_files:
		try: os.remove(x)
		except: {}


def generate_toc(html_files, novelname):
	# Generates a Table of Contents + lost strings
	toc_start = '''<?xml version='1.0' encoding='utf-8'?>
		<!DOCTYPE html>
		<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
		<head>
			<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
			<title>%(novelname)s</title>
			<link href="common.css" rel="stylesheet" type="text/css"/>
		</head>
		<body>
			<section class="frontmatter sectionCover">
				<img src="cover.png" alt="cover"/>
			</section>
			<section class="frontmatter TableOfContents">
				<header>
					<h1>Contents</h1>
				</header>
				<nav id="toc" role="doc-toc" epub:type="toc">
					<ol>
					%(toc_mid)s
			%(toc_end)s'''
	toc_mid = ""
	toc_end = '''</ol></nav></section></body></html>'''

	for i, y in enumerate(html_files):
		ident = 0
		chapter = find_between(html_files[i])
		chapter = str(chapter).replace('title>', 'span>')
		toc_mid += '''<li class="toc-Chapter-rw" id="num_%s">
			<a href="%s">%s</a>
			</li>''' % (i, os.path.basename(html_files[i]), chapter)

	return toc_start % {"novelname": escape(novelname), "toc_mid": toc_mid, "toc_end": toc_end}
