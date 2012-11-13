#!/usr/bin/env python
from thetvdb import TVShow

print "Testing thetvdb.py"
print "------------------\n"
print "Loading Community..."
tv = TVShow('94571')
print ""
print "Printing first episode filename..."
print tv.get_filename(1,1)
print ""
print "Printing filename for fourth episode of season 2 with one flag..."
print tv.get_filename(2,4,['HDTV'])
print ""
print "Printing filename for seventh episode of season 3 with two flag..."
print tv.get_filename(3,7,['HDTV','x264'])
print ""
print "Searching Voyager..."
print tv.search("voyager")
print ""
print "Requesting filename with padded zeros before seasong and episode..."
print tv.get_samba_filename("01","02")
print ""
