import requests


def get_user_gender(user, response, *args, **kwargs):
    access_token = response['access_token']
    user_id = response['user_id']
    gender = {'0': '', '1': 'Female', '2': 'Male'}
    vk_response = requests.get(
        f'https://api.vk.com/method/users.get?access_token={access_token}&user_id={user_id}&fields=about,sex&v=5.131'
    )

    user.profile.about = vk_response.json()['response'][0]['about']
    user.profile.gender = gender[str(vk_response.json()['response'][0]['sex'])]
    user.profile.save()
    return {}

