import unittest
import wunderpy2

import tests_config
from endpoint_test_case import EndpointTestCase

class TestRootEndpoint(EndpointTestCase):
	def test_get_root(self):
		'''Fetch the Root for the current User'''
		code, root = self.client.get_root()
		self.assertEqual(code, 200)
		print root

if __name__ == "__main__":
    unittest.main()