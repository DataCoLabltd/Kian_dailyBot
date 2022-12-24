import json

import slack
from decouple import config
from ..utils.block_forms import report
from ..models import ReportText

SLACK_TOKEN = config("SLACK_OAUTH_TOKEN", cast=str)

Client = slack.WebClient(SLACK_TOKEN)


def process(data):
    action_id = data['actions'][0]['value']
    channel_id = data['channel']['id']
    ts_id = data['message_ts']
    menu_action_obj = ReportText.objects.select_related('ReportButton').filter(ReportButton__id=int(action_id))
    report_obj = ReportText.objects.select_related('Channel').filter(id=menu_action_obj[0].id)
    ch_id = report_obj[0].Channel.ChannelId
    text_data = dict()
    for item in menu_action_obj:
        text_data['yesterday'] = item.YesterdayText
        text_data['today'] = item.TodayText
        text_data['blocker'] = item.BlockerText
        text_data['button_id'] = ch_id
    print(text_data, flush=True)
    Client.chat_update(channel=channel_id, ts=ts_id, attachments=json.dumps([{"type": "divider"}]),
                       blocks=report(text_data))
