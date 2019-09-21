import os
import re
import getify
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

my_novel = {}
my_novel['title'] = ''
my_novel['first_chapter_url'] = ''
my_novel['author'] = ''
my_novel['cover_url'] = ''
my_novel['genre'] = ''
my_novel['series'] = ''
my_novel['published'] = ''

#
# Examples
#

# my_novel = {}
# my_novel['title'] = 'Octopussy & the Living Daylights'
# my_novel['first_chapter_url'] = 'https://novel12.com/octopussy-the-living-daylights/page-1-991170.htm'
# my_novel['author'] = 'Ian Fleming'
# my_novel['cover_url'] = 'https://novel12.com/uploads/truyen/Octopussy-the-Living-Daylights.jpg'
# my_novel['genre'] = 'Thriller, Adventure '
# my_novel['series'] = 'James Bond #14'
# my_novel['published'] = 'June 23rd 1966'

mistborne_novel1 = {}
mistborne_novel1['title'] = 'Mistborn'
mistborne_novel1['first_chapter_url'] = 'https://novel12.com/mistborn-the-final-empire/page-1-1016911.htm'
mistborne_novel1['author'] = 'Brandon Sanderson'
mistborne_novel1['cover_url'] = 'https://novel12.com/uploads/truyen/Mistborn-The-Final-Empire.jpg'
mistborne_novel1['genre'] = 'Fantasy'
mistborne_novel1['series'] = 'Mistborn #1: The Final Empire'
mistborne_novel1['published'] = 'July 17th 2006'

mistborne_novel2 = {}
mistborne_novel2['title'] = 'Mistborn'
mistborne_novel2['first_chapter_url'] = 'https://novel12.com/the-well-of-ascension/page-1-1017025.htm'
mistborne_novel2['author'] = 'Brandon Sanderson'
mistborne_novel2['cover_url'] = 'https://novel12.com/uploads/truyen/The-Well-of-Ascension.jpg'
mistborne_novel2['genre'] = 'Fantasy'
mistborne_novel2['series'] = 'Mistborn #2: The Well of Ascension'
mistborne_novel2['published'] = 'August 21st 2007'

mistborne_novel3 = {}
mistborne_novel3['title'] = 'Mistborn'
mistborne_novel3['first_chapter_url'] = 'https://novel12.com/the-hero-of-ages/page-1-1017152.htm'
mistborne_novel3['author'] = 'Brandon Sanderson'
mistborne_novel3['cover_url'] = 'https://novel12.com/uploads/truyen/The-Hero-of-Ages.jpg'
mistborne_novel3['genre'] = 'Fantasy'
mistborne_novel3['series'] = 'Mistborn #3: The Hero of Ages'
mistborne_novel3['published'] = '2008'

mistborne_novel4 = {}
mistborne_novel4['title'] = 'Mistborn'
mistborne_novel4['first_chapter_url'] = 'https://novel12.com/the-alloy-of-law/page-1-1017269.htm'
mistborne_novel4['author'] = 'Brandon Sanderson'
mistborne_novel4['cover_url'] = 'https://novel12.com/243881/the-alloy-of-law.htm'
mistborne_novel4['genre'] = 'Fantasy'
mistborne_novel4['series'] = 'Mistborn #4: The Alloy of Law'
mistborne_novel4['published'] = 'January 1st 2011'

# used to find the next button
# to navigate between chapters up to the last chapter
next_button_text = 'Next >'
storage_dir = ''

def export(data_novel):
    getify.cover_generator(data_novel['cover_url'], data_novel['series'], data_novel['title'], data_novel['author'])

    chapter = 1

    download_url = data_novel['first_chapter_url']
    file_list = []
    end = False
    while (True):
        filename = storage_dir + os.sep + "tmp" + os.sep + str(chapter) + ".xhtml"
        filenameOut = storage_dir + os.sep + "tmp"+os.sep+'ch-{:0>3}'.format(chapter)
        try:
            getify.download(download_url, filename)
        except HTTPError as e:
            # Return code error (e.g. 404, 501, ...)
            print('URL: {}, HTTPError: {} - {}'.format(download_url, e.code, e.reason))
        except URLError as e:
            # Not an HTTP-specific error (e.g. connection refused)
            print('URL: {}, URLError: {}'.format(download_url, e.reason))
        else:
            raw = open(filename, "r", encoding="utf8")
            soup = BeautifulSoup(raw, 'lxml')
            button_next = soup.find_all('a', string=re.compile('Next >'), href=True)
            if (not button_next):
                end = True
            else:
                download_url = button_next[0]['href']
            getify.clean(filename, filenameOut, "Chapter #{:100}".format(chapter))
            file_list.append(filenameOut + ".xhtml")
        if (not end):
            chapter += 1
        else:
            break
    getify.generate(file_list, data_novel['title'], data_novel['author'], 'ch-', data_novel['series'], None, None)

def mistborne():
    '''downloads the 4 Mistborne novels'''
    mistborne = [mistborne_novel1, mistborne_novel2, mistborne_novel3, mistborne_novel4]
    for novel in mistborne:
        print("Exporting {0}".format(novel['series']))
        export(novel)
        print("Exporting {0} DONE!".format(novel['series']))
    print("All done!")

if __name__ == '__main__':
    # mistborne()
    export(my_novel)

