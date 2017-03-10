'''
Encapsulates all tasks that can be run against the 'avatar' endpoint
'''
import os

def get_avatar(client, user_id, size=None, fallback=None, save_path=".", avatar_name="avatar.png"):
	'''Show the avatar of a user'''
	data = {
		"user_id": user_id,
		"size": size,
		"fallback": fallback
	}
	data = {k:v for k, v in data.items() if v is not None}
	response = client.authenticated_request(client.api.Endpoints.AVATAR, data=data)
	# save it to save_path
	image_path = os.path.join(save_path, avatar_name)
	with open(image_path, "wb") as f:
		for chunk in response.iter_content(chunk_siz=1024):
			f.write(chunk)
	print "avatar has been saved to", image_path
	return image_path
	