import unittest
from unittest.mock import patch, MagicMock
import time
import random


class CDN:
    def __init__(self, origin_server, cache_timeout=300):
        self.origin_server = origin_server
        self.cache = {}
        self.cache_timeout = cache_timeout

    def get_content(self, url):
        if url in self.cache and self.cache[url]['expires'] > time.time():
            print(f"Cache hit for {url}")
            return self.cache[url]['content']
        else:
            print(f"Cache miss for {url}")
            content = self.origin_server.fetch_content(url)
            self.cache[url] = {
                'content': content,
                'expires': time.time() + self.cache_timeout
            }
            return content


class OriginServer:
    def fetch_content(self, url):
        # Simulate network latency
        time.sleep(random.uniform(0.5, 2.0))
        return f"Content from {url}"


class TestCDN(unittest.TestCase):

    def setUp(self):
        self.origin_server = OriginServer()
        self.cdn = CDN(self.origin_server)

    @patch('time.sleep')
    def test_cache_hit(self, mock_sleep):
        url = "http://example.com/page1"
        content = self.cdn.get_content(url)
        self.assertEqual(content, f"Content from {url}")
        # Second call should be a cache hit
        content = self.cdn.get_content(url)
        self.assertEqual(content, f"Content from {url}")
        mock_sleep.assert_not_called()  # No sleep during cache hit

    @patch('time.sleep')
    def test_cache_miss_and_latency(self, mock_sleep):
        url = "http://example.com/page2"
        # First call should be a cache miss and simulate latency
        content = self.cdn.get_content(url)
        self.assertEqual(content, f"Content from {url}")
        mock_sleep.assert_called_once()  # Sleep should have been called during cache miss
        # Second call should be a cache hit
        content = self.cdn.get_content(url)
        self.assertEqual(content, f"Content from {url}")
        mock_sleep.assert_called_once()  # Sleep should not have been called again

    @patch('time.sleep')
    def test_cache_expiration(self, mock_sleep):
        url = "http://example.com/page3"
        content = self.cdn.get_content(url)
        self.assertEqual(content, f"Content from {url}")
        # Manually expire the cache entry
        self.cdn.cache[url]['expires'] = 0
        # Second call should be a cache miss and simulate latency
        content = self.cdn.get_content(url)
        self.assertEqual(content, f"Content from {url}")
        mock_sleep.assert_called_once()


if __name__ == '__main__':
    unittest.main()
