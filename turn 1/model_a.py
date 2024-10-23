import time
import unittest
from unittest.mock import Mock, patch

class CDN:
	def __init__(self, cache_timeout=300):
		self.cache = {}
		self.cache_timeout = cache_timeout

	def get_content(self, url):
		current_time = time.time()

		if url in self.cache and current_time - self.cache[url]['time'] < self.cache_timeout:
			print(f"Cache Hit for {url}")
			return self.cache[url]['content']

		print(f"Cache Miss for {url}")
		content = self.fetch_content_from_network(url)
		self.cache[url] = {'content': content, 'time': current_time}
		return content

	def fetch_content_from_network(self, url):
		time.sleep(2)  # Simulate network latency
		return f"Dummy content for {url}"


class TestCDN(unittest.TestCase):

	def setUp(self):
		self.cdn = CDN()

	@patch('time.sleep')
	def test_cache_miss_and_latency(self, mock_sleep):
		url = "http://example.com/test.txt"

		# First request: Simulate cache miss and network latency
		content = self.cdn.get_content(url)
		self.assertEqual(content, f"Dummy content for {url}")
		mock_sleep.assert_called_once_with(2)  # Check for network latency simulation

		# Second request: Simulate cache hit
		content = self.cdn.get_content(url)
		self.assertEqual(content, f"Dummy content for {url}")
		mock_sleep.assert_not_called()  # No latency for cache hit

if __name__ == '__main__':
	unittest.main()
