'''
Encapsulates all tasks that can be run against the 'root' endpoint
'''

def get_root(client):
	'''Fetch the Root for the current User'''
	response = client.authenticated_request(client.api.Endpoints.ROOT)
	return response.status_code, response.json()