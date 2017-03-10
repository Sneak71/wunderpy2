'''
Encapsulates all tasks that can be run against the 'reminders' endpoint
'''

def get_reminders(client, task_id=None, list_id=None):
	'''Get Reminders for a Task or List'''
	data = {}
	if task_id is not None:
		data["task_id"] = task_id
	if list_id is not None:
		data["list_id"] = list_id

	response = client.authenticated_request(client.api.Endpoints.REMINDERS, data=data)
	return response.json()


def create_reminders(client, task_id, date, created_by_device_udid=None):
	'''
	Create a Reminder

	See https://developer.wunderlist.com/documentation/endpoints/reminder for detailed parameter information
	'''
	data = {
		"task_id": task_id,
		"date": date
	}
	if created_by_device_udid is not None:
		data["created_by_device_udid"] = created_by_device_udid
	response = client.authenticated_request(client.api.Endpoints.REMINDERS, method="POST", data=data)
	return response.json()


def update_reminder(client, reminder_id, date, revision):
	'''
	Update a Reminder
	'''
	data = {
            'id' : reminder_id,
            'date' : date,
            'revision' : revision,
            }
    endpoint = '/'.join([client.api.Endpoints.REMINDERS, str(reminder_id)])
    response = client.authenticated_request(endpoint, 'PATCH', data=data)
    return response.json()

def delete_reminder(client, reminder_id, revision):
    params = {
            'revision' : int(revision),
            }
    endpoint = '/'.join([client.api.Endpoints.REMINDERS, str(reminder_id)])
    client.authenticated_request(endpoint, 'DELETE', params=params)