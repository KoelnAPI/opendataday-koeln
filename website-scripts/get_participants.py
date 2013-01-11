# encoding: utf-8

"""
Liest die Twitter-Links aus der Teilnehmerliste im Wiki und schreibt
sie in einen lokalen Cache
"""

import urllib
import simplejson as json
from urlparse import urlparse
import sys

OUTPUT_PATH = '/var/www/opendataday.koeln.de/opendataday-koeln/website/participants.inc.html'


def get_twitter_users():
    sections_url = 'http://wiki.opendataday.org/wiki/api.php?action=parse&text={{:Cologne2013}}__TOC__&prop=sections&format=json'
    section_url_mask = 'http://wiki.opendataday.org/wiki/api.php?action=parse&page=Cologne2013&section=%d&format=json'
    sections_json = urllib.urlopen(sections_url).read()
    sections = json.loads(sections_json)
    counter = 0
    for section in sections['parse']['sections']:
        counter += 1
        if 'participants' in section['line'].lower():
            #print counter, section
            break
    section_json = urllib.urlopen(section_url_mask % counter).read()
    section = json.loads(section_json)
    links = []
    for link in section[u'parse'][u'externallinks']:
        if '//twitter.com/' in link:
            parsed = urlparse(link)
            links.append(parsed.path[1:])  # ommit leading slash
    return links


def get_twitter_user_info(username):
    url = 'https://api.twitter.com/1/users/show.json?screen_name=' + urllib.quote(username.encode('utf-8'))
    response = urllib.urlopen(url).read()
    return json.loads(response)


if __name__ == '__main__':
    twitter_users = get_twitter_users()
    if len(twitter_users) == 0:
        sys.exit(1)
    f = open(OUTPUT_PATH, 'w')
    template = '<a href="%s" target="_blank" title="%s"><img src="%s" class="img-polaroid" width="48" height="48" alt="%s" /></a>'
    for user in twitter_users:
        info = get_twitter_user_info(user)
        f.write(template % (
            'https://twitter.com/' + info['screen_name'].encode('utf-8'),
            info['name'].encode('utf-8') + ' (' + info['screen_name'].encode('utf-8') + ')',
            info['profile_image_url'].encode('utf-8'),
            'Profilbild von ' + info['name'].encode('utf-8')
        ))
        f.write("\n")
