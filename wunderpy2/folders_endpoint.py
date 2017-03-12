'''
Encapsulates all tasks that can be run against the 'folders' endpoint
See also: https://developer.wunderlist.com/documentation/endpoints/folder
'''

def _check_title_length(title, api):
    ''' Checks the given title against the given API specifications to ensure it's short enough '''
    if len(title) > api.MAX_FOLDER_TITLE_LENGTH:
        raise ValueError("Title cannot be longer than {} characters".format(api.MAX_FOLDER_TITLE_LENGTH))

def _assure_type_list(var, var_name):
	'''assure the given var is a list'''
	if not isinstance(var, list):
		raise ValueError("{} should be a list, but a {}".format(var_name, type(var)))

def get_folders(client):
    ''' Get all Folders created by the the current User '''
    response = client.authenticated_request(client.api.Endpoints.FOLDERS)
    return response.status_code, response.json()

def get_list(client, folder_id):
    ''' Gets the specific folder '''
    endpoint = '/'.join([client.api.Endpoints.FOLDERS, str(folder_id)])
    response = client.authenticated_request(endpoint)
    return response.status_code, response.json()

def create_folder(client, title, list_ids):
    ''' Creates a new folder with the given title '''
    _check_title_length(title, client.api)
    _assure_type_list(list_ids, "list_ids")
    data = {
            'title' : title,
            'list_ids': list_ids,
            }
    response = client.authenticated_request(client.api.Endpoints.FOLDERS, method='POST', data=data)
    return response.status_code, response.json()

def update_folder(client, folder_id, revision, title=None, list_ids=None):
    '''
    Update a Folder by overwriting properties
    '''
    data = {
    	'revision' : revision,
    }
    if title is not None:
        _check_title_length(title, client.api)
        data['title'] = title
    if list_ids is not None:
    	_assure_type_list(list_ids, "list_ids")
    	data['list_ids'] = list_ids
    
    endpoint = '/'.join([client.api.Endpoints.FOLDERS, str(folder_id)])
    response = client.authenticated_request(endpoint, 'PATCH', data=data)
    return response.status_code, response.json()

def delete_folder(client, folder_id, revision):
	'''Delete a Folder permanently'''
    params = {
            'revision' : int(revision),
            }
    endpoint = '/'.join([client.api.Endpoints.FOLDERS, str(folder_id)])
    response = client.authenticated_request(endpoint, 'DELETE', params=params)
    return response.status_code
