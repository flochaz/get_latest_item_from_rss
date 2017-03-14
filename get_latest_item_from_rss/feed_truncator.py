print('Loading function')

# https://05o2r94unj.execute-api.us-east-1.amazonaws.com/dev/truncated-feed.xml?feed_url=http://radiofrance-podcast.net/podcast09/rss_14518.xml
# geopolitique : http://radiofrance-podcast.net/podcast09/rss_10009.xml
# Histoire du monde : http://radiofrance-podcast.net/podcast09/rss_14518.xml
# 7pm journal : http://radiofrance-podcast.net/podcast09/rss_11736.xml
# Une de la science : http://radiofrance-podcast.net/podcast09/rss_16589.xml

import urllib2
from xml.dom import minidom


def lambda_handler(event, context):
    if 'feed_url' in event:
        original_feed = get_feed_from_url(event['feed_url'])
        {'response': get_truncated_feed(original_feed)}
        return {'response': get_truncated_feed(original_feed)}
    else:
        original_feed = get_feed_from_url('http://radiofrance-podcast.net/podcast09/rss_16589.xml')
        {'response': get_truncated_feed(original_feed)}
        return {'response': get_truncated_feed(original_feed)}
        print('No feed_url found')
        raise Exception


def get_feed_from_url(url):
    feed = urllib2.urlopen(url).read()
    return feed


def get_truncated_feed(feed):
    truncated_feed = ""
    count = 0
    for line in feed.split('\n'):
        count += 1
        if "</item>" not in line:
            if "<enclosure" in line:
                truncated_feed += "<enclosure url=\"{mp3_url}\" length=\"3928192\" type=\"audio/mpeg\"/>".format(
                    mp3_url=minidom.parseString(feed).getElementsByTagName("guid")[0].firstChild.nodeValue.replace(
                        'http:', 'https:'))
                truncated_feed += "\n"
            else:
                truncated_feed += line.replace('http:', 'https:')
                truncated_feed += "\n"
        else:
            truncated_feed += "</item></channel></rss>"
            break
    return truncated_feed