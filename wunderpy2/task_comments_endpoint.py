'''
Encapsulates all tasks that can be run against the 'task_comments' endpoint
'''

def get_comments(client, task_id=None, list_id=None):
	'''Get the Comments for a Task or a List'''
	data = {}
	if task_id is not None:
		data["task_id"] = task_id
	if list_id is not None:
		data["list_id"] = list_id

	response = client.authenticated_request(client.api.Endpoints.TASK_COMMENTS, data=data)
	return response.json()

def get_comment(client, comment_id):
	'''Get a specific Comment'''
	endpoint = '/'.join([client.api.Endpoints.TASK_COMMENTS, str(comment_id)])
    response = client.authenticated_request(endpoint)
    return response.json()

def create_comment(client, task_id, text):
	'''
	Create a Comment

	See https://developer.wunderlist.com/documentation/endpoints/task_comment for detailed parameter information
	'''
	data = {
		"task_id": task_id,
		"text": text
	}
	response = client.authenticated_request(client.api.Endpoints.TASK_COMMENTS, method="POST", data=data)
	return response.json()