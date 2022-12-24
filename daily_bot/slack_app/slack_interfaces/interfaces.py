from decouple import config
from slack import WebClient

SLACK_TOKEN = config("SLACK_OAUTH_TOKEN", cast=str)


def get_client():
    return WebClient(token=SLACK_TOKEN)


def get_bot_id():
    return get_client().auth_test()['user_id']


def get_user_profile(user_id):
    response = get_client().users_profile_get(user=user_id)
    if response['ok']:
        response['profile']['user_id'] = user_id
        return response['profile']
    else:
        return False


def get_all_user_info():
    response = get_client().api_call("users.list")
    if response['ok']:
        return response['members']
    else:
        return False


def get_active_users():
    response = get_all_user_info()
    result = list()
    if response:
        for item in response:
            if item['is_bot'] is False and item['deleted'] is False:
                result.append(item)
    return result
