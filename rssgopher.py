#!/usr/bin/env python
# -*- coding: utf-8 -*-
import feedparser, html2text, os, sys, re

feed = feedparser.parse("http://planet.entropia.de/rss.rdf")
filepath = "/var/gopher/planet/"
i = 0

def title2filename(title, i):
  if isinstance(title,unicode): title = title.encode("iso-8859-15", "replace")
  title = re.compile("\/").sub("-", title) 
  title = re.compile("ä").sub("ae", title) 
  title = re.compile("ü").sub("ue", title) 
  title = re.compile("ö").sub("oe", title) 
  title = re.compile("Ä").sub("Ae", title) 
  title = re.compile("Ü").sub("Ue", title) 
  title = re.compile("Ö").sub("Oe", title) 
  title = re.compile("ß").sub("ss", title) 
  
  filename = "%sfeed-%02d-%s.txt" % (filepath, i, title)  
  
  return filename

def wrap(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line)-line.rfind('\n')-1
                         + len(word.split('\n',1)[0]
                              ) >= width)],
                   word),
                  text.split(' ')
                 )

for entry in feed['entries']:
    i = i + 1
    text = entry['description']
    text = html2text.html2text(text)

    filename = title2filename(entry['title'], i)
    
    if isinstance(text,unicode): text = text.encode("iso-8859-15","replace")
    text = wrap(text,80)

    try:
        f = open(filename, "w")
        f.write(text)
        f.close()
    except:
        os.unlink(filename)
        sys.stderr.write("Could not write file %s \n" % (filename))
        
