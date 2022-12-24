from ..models import WorkSpaceUser
from ..utils.slack_attachments import generate_attachment, create_user_report, create_user_report_today, \
    create_user_report_yesterday, create_user_report_header, create_user_report_blocker
from ..model_interactions.methds import add_report
import datetime
import slack
from decouple import config
import json

SLACK_TOKEN = config("SLACK_OAUTH_TOKEN", cast=str)

Client = slack.WebClient(SLACK_TOKEN)


def main(data):
    user_id = data['user']['id']
    channel_id = data['channel']['id']
    ts_id = data['container']['message_ts']
    values = data['state']['values']
    temp = []
    for key, value in values.items():
        temp.append(value)
    if data['actions'][0]['action_id'] == 'actionId-register-submit':
        selected_options = temp[0]['multi_static_select_role']['selected_options']
        home_address = temp[1]['plain_text_input_home_address']['value']
        report_time = temp[2]['timepicker-action-report-time']['selected_time']
        roles = []
        for item in selected_options:
            roles.append(int(item['value']))
        report_time = datetime.datetime.strptime(report_time, '%H:%M').time()
        user_object = WorkSpaceUser.objects.get(UserId=user_id)
        user_object.Address = home_address
        user_object.ReportTime = report_time
        user_object.UserRole.add()
        for item in selected_options:
            user_object.UserRole.add(int(item['value']))
        user_object.save()
        text = ':pray: Thank you'
        updated_block = [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": text,
                    "emoji": True
                }
            }
        ]
        Client.chat_update(channel=channel_id, ts=ts_id, blocks=updated_block)
        attachment = generate_attachment('main_menu')
        if attachment:
            Client.chat_postMessage(channel=channel_id,
                                    attachments=json.dumps(attachment), as_user=True)
    elif data['actions'][0]['value'] == 'submit report':
        user_obj = WorkSpaceUser.objects.get(UserId=user_id)
        yesterday_text = temp[0]['plain_text_yesterday_report']['value']
        today_text = temp[1]['plain_text_today_report']['value']
        blocker_text = temp[2]['plain_text_blocker']['value']
        target_channel_id = data['actions'][0]['action_id']
        request_data = {
            'yesterday_text': yesterday_text,
            'today_text': today_text,
            'blocker_text': blocker_text,
            'user_id': user_id,
            'image_url': user_obj.ImageURL,
            'user_name': user_obj.FullName,
            'channel_id': target_channel_id
        }
        add_report(request_data)

        # res = create_user_report(request_data)
        # Client.chat_postMessage(channel=target_channel_id, attachments=json.dumps(res))
        res = create_user_report_header(request_data)
        Client.chat_postMessage(channel=target_channel_id, attachments=json.dumps(res))
        res = create_user_report_yesterday(request_data)
        Client.chat_postMessage(channel=target_channel_id, attachments=json.dumps(res))
        res = create_user_report_today(request_data)
        Client.chat_postMessage(channel=target_channel_id, attachments=json.dumps(res))
        res = create_user_report_blocker(request_data)
        if res:
            Client.chat_postMessage(channel=target_channel_id, attachments=json.dumps(res))
        Client.chat_update(channel=channel_id, ts=ts_id, blocks=[
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "Well done! This is all, you can continue with your work",
                    "emoji": True
                }
            }
        ])
