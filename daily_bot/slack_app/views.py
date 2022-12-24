import json
from decouple import config
import slack
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WorkSpaceUser, Menu
from .utils.utils import map_user_profile_items
from .slack_interfaces.interfaces import get_user_profile, get_bot_id
from .utils.slack_attachments import generate_attachment, create_user_register_form
from .process_block_actions.main import main
from .process_interactive_message.main import process as interactive_main
from .utils import get_channels
from .model_interactions.methds import get_users_not_reported

SLACK_TOKEN = config("SLACK_OAUTH_TOKEN", cast=str)
SLACK_SIGNING_SECRET = config("SLACK_SIGNING_SECRET", cast=str)
SLACK_VERIFICATION_TOKEN = config("SLACK_VERIFICATION_TOKEN", cast=str)
SLACK_COMPANY_NAME = config("SLACK_COMPANY_NAME", cast=str)
Client = slack.WebClient(SLACK_TOKEN)
BOT_ID = get_bot_id()


class Interaction(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        payload = json.loads(slack_message.get('payload'))
        print(payload, flush=True)
        if payload['type'] == 'block_actions':
            main(payload)
        elif payload['type'] == 'interactive_message':
            interactive_main(payload)
        return Response(status=status.HTTP_200_OK)


class Events(APIView):
    def post(self, request, *args, **kwargs):

        slack_message = request.data

        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # verification challenge
        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message,
                            status=status.HTTP_200_OK)
        # greet bot
        if 'event' in slack_message:  # 4
            event_message = slack_message.get('event')  #
            # ignore bot's own message
            if event_message.get('subtype') == 'bot_message':  # 5
                return Response(status=status.HTTP_200_OK)  #
            # process user's message
            user = event_message.get('user')
            text = event_message.get('text')
            if user != BOT_ID and user is not None:
                text = event_message.get('text')  #
                channel = event_message.get('channel')  #
                if not WorkSpaceUser.objects.filter(UserId=user).exists():
                    body = map_user_profile_items(get_user_profile(user))
                    WorkSpaceUser.objects.create(**body)
                    response_msg = f":wave:,Hello <@%s>, welcome to {SLACK_COMPANY_NAME} company, I hope we will have a good " \
                                   f"cooperation! " % user
                    Client.chat_postMessage(channel=channel, text=response_msg)
                    Client.chat_postMessage(channel=channel, user=user, blocks=create_user_register_form())
                    return Response(status=status.HTTP_200_OK)
                elif text.lower() == 'report':
                    menu_obj = Menu.objects.filter(UserId=user)
                    for menu in menu_obj:
                        attachment = generate_attachment(menu.MenuTitle)
                        if attachment:
                            Client.chat_postMessage(channel=channel,
                                                    attachments=json.dumps(attachment), as_user=True)
                            return Response(status=status.HTTP_200_OK)
                    message = 'No reports have been specified for you, Talk to the team leader please'
                    Client.chat_postMessage(channel=channel, text=message)
                elif text.lower() == 'profile':
                    Client.chat_postMessage(channel=channel, user=user, blocks=create_user_register_form())
                else:
                    message = "I do not understand what you said :thinking: \n" \
                              "Say one of the following: \n" \
                              "`profile` : edit profile \n" \
                              "`report` : create a report "
                    Client.chat_postMessage(channel=channel, text=message)
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)


class FetchChannels(APIView):
    def get(self, request, format=None):
        get_channels.get_info()
        return Response(status=status.HTTP_200_OK)


class Test(APIView):
    def get(self, request, format=None):
        menu_obj = Menu.objects.filter(UserId='U012L1M3RUP')
        print(menu_obj, flush=True)
        return Response(status=status.HTTP_200_OK)
