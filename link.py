# -*- coding: utf-8 -*-
import os
import sys

linksFileName = 'links.db'

delimiter = '===>'
currFile = ''

# weather .py be compiled to binary
if getattr(sys, 'frozen', False):
    currFile = sys.executable
else:
    currFile = __file__

currDir, _ = os.path.split(currFile)
linksFile = os.path.join(currDir, linksFileName)

all_links = { }


def read_links():
    if os.path.isfile(linksFile):
        with open(linksFile, 'r') as plinks:
            while True:
                # read lines
                line = plinks.readline()
                if not line:
                    break
                # get link and orignal directory, then delete blank characters
                # and store them to all_links(dict)
                if line.find(delimiter) < 0:
                    continue
                link, orignal = line.split(delimiter)
                link, orignal = link.strip(), orignal.strip()
                all_links.update({link: orignal})


def add_link(link, orignal):
    all_links.update({link: orignal})


def revise_link(link, orignal):
    all_links.update({link: orignal})


def delete_link(link):
    all_links.pop(link)


def clear_links():
    all_links.clear()


def save_change():
    with open(linksFile, 'w') as plinks:
        links = all_links.keys()
        for link in links:
            item = link + ' ===> ' + all_links[link] + '\n'
            plinks.write(item)


if __name__ == '__main__':
    read_links()
    save_change()

# with open(linksFileName, 'w') as p:
#     p.write('赛垦利, 啊;slkd ===> 龙卡 另\n')
#     p.write("sdll las另\n")
#     p.write("sdf赛lfLsdlf ===> a;lsfasd /asdfasdf/afsdf\n")
    