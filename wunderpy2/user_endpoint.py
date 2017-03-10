'''
Encapsulates all tasks that can be run against the 'user' endpoint
'''

def get_user(client):
	'''Fetch the currently logged in user'''
	response = client.authenticated_request(client.api.Endpoints.USER)
	return response.json()
	