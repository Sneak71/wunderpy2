import unittest
import wunderpy2

import tests_config
from endpoint_test_case import EndpointTestCase

class TestUserEndpoint(EndpointTestCase):
	def test_get_user(self):
		'''Test getting a specific user'''
		print self.client.get_user()

if __name__ == "__main__":
    unittest.main()