'''
Encapsulates all tasks that can be run against the 'files' endpoint
'''

def get_files(client, task_id=None, list_id=None):
	'''Get Files for a Task or List'''
	data = {}
	if task_id is not None:
		data["task_id"] = task_id
	if list_id is not None:
		data["list_id"] = list_id

	response = client.authenticated_request(client.api.Endpoints.FILES, data=data)
	return response.json()

def get_file(client, file_id):
	'''Get a specific File'''
	endpoint = '/'.join([client.api.Endpoints.FILES, str(file_id)])
    response = client.authenticated_request(endpoint)
    return response.json()

def create_file(client, upload_id, task_id, local_created_at=None):
	'''
	create a file

	See https://developer.wunderlist.com/documentation/endpoints/file for detailed parameter information
	'''
	data = {
		"upload_id": upload_id,
		"task_id": task_id
	}
	if local_created_at is not None:
		data["local_created_at"] = local_created_at
	response = client.authenticated_request(client.api.Endpoints.FILES, method="POST", data=data)
	return response.json()

def destroy_file(client, file_id, revision):
	'''Destroy a File'''
	params = {
            'revision' : int(revision),
            }
	endpoint = '/'.join([client.api.Endpoints.FILES, str(file_id)])
    client.authenticated_request(endpoint, 'DELETE', params=params)