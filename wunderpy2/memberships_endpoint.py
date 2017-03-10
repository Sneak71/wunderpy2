'''
Encapsulates all tasks that can be run against the 'memberships' endpoint
A Membership is the join model between Users and Lists.

See also: https://developer.wunderlist.com/documentation/endpoints/membership
'''

def get_memberships(client):
    ''' Get Memberships for a List or the current User '''
    response = client.authenticated_request(client.api.Endpoints.MEMBERSHIPS)
    return response.status_code, response.json()

def add_member(client, list_id, user_id=None, email=None, muted=False):
    ''' 
    Add a Member to a List
    '''
    assert (user_id is None) != (email is None)
    data = {
            'list_id' : list_id,
            'muted': muted
    }
    if user_id:
    	data["user_id"] = user_id
    elif email:
    	data["email"] = email

    response = client.authenticated_request(client.api.Endpoints.MEMBERSHIPS, method='POST', data=data)
    return response.status_code, response.json()

def mark_member_accepted(client, member_id, revision, state="accepted", muted=False):
	'''
	Mark a Member as accepted
	'''
	data = {
		"revision": revision,
		"state": state,
		"muted": muted
	}
	endpoint = '/'.join([client.api.Endpoints.MEMBERSHIPS, str(member_id)])
    response = client.authenticated_request(endpoint, 'PATCH', data=data)
    return response.status_code, response.json()

def remove_member(client, member_id, revision):
	'''Remove a Member from a List'''
    params = {
            'revision' : int(revision),
            }
    endpoint = '/'.join([client.api.Endpoints.MEMBERSHIPS, str(member_id)])
    response = client.authenticated_request(endpoint, 'DELETE', params=params)
    return response.status_code

# seems no difference with the method above
def reject_invite(client, member_id, revision):
	'''Reject an invite to a List'''
    params = {
            'revision' : int(revision),
            }
    endpoint = '/'.join([client.api.Endpoints.MEMBERSHIPS, str(member_id)])
    response = client.authenticated_request(endpoint, 'DELETE', params=params)
    return response.status_code