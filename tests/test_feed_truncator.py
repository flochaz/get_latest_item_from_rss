from unittest import TestCase
from get_latest_item_from_rss import feed_truncator
from xml.dom import minidom

class TestFeedTruncator(TestCase):

    france_inter_feed = 'http://radiofrance-podcast.net/podcast09/rss_14518.xml'

    def test_get_feed_from_url(self):
        expected_str = feed_truncator.get_feed_from_url(self.france_inter_feed)
        self.assertLess(len(expected_str.split('\n')),2000)

    def test_get_truncated_feed(self):
        original_feed = feed_truncator.get_feed_from_url(self.france_inter_feed)
        original_feed_dom = minidom.parseString(original_feed)
        truncated_feed = feed_truncator.get_truncated_feed(original_feed)
        print "### NEW ###"
        print truncated_feed
        print '###########'
        truncated_feed_dom = minidom.parseString(truncated_feed)

        self.assertGreater(len(original_feed_dom.getElementsByTagName("item")), 10)
        self.assertEqual(1, len(truncated_feed_dom.getElementsByTagName("item")))
        self.assertEqual(original_feed_dom.getElementsByTagName("guid")[0].firstChild.nodeValue.replace(
                        'http:', 'https:'), truncated_feed_dom.getElementsByTagName("enclosure")[0].getAttribute("url"))
