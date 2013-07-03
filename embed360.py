#!/usr/bin/env python
# -*- coding: utf8 -*-
# This script looks for panorama pictures in your g+ album
# and embeds them into a website.
#
# Example usage:
# $ ./embed360.py 114253306058596674445 5882828446552988657
#
# Link: https://developers.google.com/photo-sphere/web/
#
# License: Apache 2.0
# Author: Harald Schilly <harald@schil.ly>

import json
from urllib2 import urlopen

INTRO = '''\
<!DOCTYPE html>
<html>
<head>
<title>Panorama Pix</title>
</head>
<body>
'''

OUTRO = '''\
<script type="text/javascript" src="https://apis.google.com/js/plusone.js"></script>
<script>gapi.panoembed.go();</script>
</body>
</html>
'''


def pixlink(url, href):
    y = urlopen(href + '&full-exif=true').read()
    data = json.loads(y)['feed']
    # print json.dumps(data, indent=True)
    exif = data["exif$tags"]
    # print json.dumps(exif, indent=True)

    fullheight = exif["exif$FullPanoHeightPixels"]["$t"]
    fullwidth = exif["exif$FullPanoWidthPixels"]["$t"]
    croppedheight = exif["exif$CroppedAreaImageHeightPixels"]["$t"]
    croppedwidth = exif["exif$CroppedAreaImageWidthPixels"]["$t"]
    offsetleft = exif["exif$CroppedAreaLeftPixels"]["$t"]
    offsettop = exif["exif$CroppedAreaTopPixels"]["$t"]

    print "<g:panoembed imageurl='%s'" % url
    print "  fullsize ='%s,%s'" % (fullwidth, fullheight)
    print "  croppedsize='%s,%s'" % (croppedwidth, croppedheight)
    print "  offset='%s,%s' />" % (offsetleft, offsettop)


def get_feed(uid, albumid):
    href = "https://picasaweb.google.com/data/feed/api/user/{0}/albumid/{1}?alt=json&v=4".format(
        uid, albumid)
    x = urlopen(href).read()
    data = json.loads(x)['feed']
    entries = data['entry']
    print INTRO
    for entry in entries:
        streamIds = [_['$t'] for _ in entry['gphoto$streamId']]
        links = entry['link']
        url = entry['content']['src']
        # print json.dumps(entry, indent=True)
        if 'photosphere' in streamIds:
            for link in links:
                if link['rel'] == 'http://schemas.google.com/g/2005#feed':
                    # print link['href']
                    pixlink(url, link['href'])
    print OUTRO

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 3:
        userid = sys.argv[1]
        albumid = sys.argv[2]
    else:
        userid = input("Your User ID, the first long number in the URL: ")
        albumid = input(
            "The Album ID, another long number, probably the second one in the URL: ")
    get_feed(userid, albumid)
