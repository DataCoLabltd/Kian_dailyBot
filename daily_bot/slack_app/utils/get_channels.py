from ..slack_interfaces.interfaces import get_client
from ..models import Channel, WorkSpaceUser
from .utils import map_user_profile_items
from ..slack_interfaces.interfaces import get_user_profile


def get_info():
    res = get_client().conversations_list(types='private_channel')
    channels = res['channels']
    res = get_client().conversations_list(types='public_channel')
    channels = res['channels'] + channels
    for channel in channels:
        body = {
            "ChannelId": channel['id'],
            "Name": channel['name'],
            "Creator": channel['creator'],
            "ChannelDescription": channel['topic']['value'],
        }
        Channel.objects.get_or_create(**body)
        channel_info = get_client().conversations_members(channel=channel['id'])
        for member in channel_info['members']:
            data = get_user_profile(member)
            user_info = map_user_profile_items(data)
            if user_info:
                WorkSpaceUser.objects.get_or_create(**user_info)
                channel_object = Channel.objects.get(ChannelId=channel['id'])
                channel_object.ChannelUsers.add(user_info['UserId'])
