'''
Encapsulates all tasks that can be run against the 'webhooks' endpoint
See also: https://developer.wunderlist.com/documentation/endpoints/webhooks
'''
def _check_url_length(url, api):
    ''' Checks the given url against the given API specifications to ensure it's short enough '''
    if len(url) > api.MAX_WEBHOOK_URL_LENGTH:
        raise ValueError("Url cannot be longer than {} characters".format(api.MAX_WEBHOOK_URL_LENGTH))

def get_list(client, list_id):
    ''' Get all webhooks for a list '''
    endpoint = '/'.join([client.api.Endpoints.WEBHOOKS, str(list_id)])
    response = client.authenticated_request(endpoint)
    return response.status_code, response.json()


def create_webhook(client, list_id, url, processor_type, configuration=""):
    ''' Creates a new webhook '''
    _check_title_length(url, client.api)
    data = {
            'list_id' : list_id,
            'url': url,
            'processor_type': processor_type,
            'configuration': configuration
            }
    response = client.authenticated_request(client.api.Endpoints.WEBHOOKS, method='POST', data=data)
    return response.status_code, response.json()

def delete_webhook(client, webhook_id, revision):
	'''Delete a webhook permanently'''
    params = {
            'revision' : int(revision),
            }
    endpoint = '/'.join([client.api.Endpoints.WEBHOOKS, str(webhook_id)])
    response = client.authenticated_request(endpoint, 'DELETE', params=params)
    return response.status_code