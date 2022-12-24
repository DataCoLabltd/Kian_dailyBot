from ..models import Reports, WorkSpaceUser, Channel
from datetime import datetime
import slack
from decouple import config

SLACK_TOKEN = config("SLACK_OAUTH_TOKEN", cast=str)
Client = slack.WebClient(SLACK_TOKEN)


def add_report(data):
    user_obj = WorkSpaceUser.objects.get(UserId=data['user_id'])
    channel_obj = Channel.objects.get(ChannelId=data['channel_id'])
    report_obj = Reports.objects.create(UserId=user_obj,
                                        ChannelId=channel_obj,
                                        TodayReport=data['today_text'],
                                        YesterdayReport=data['yesterday_text'],
                                        BlockerReport=data['blocker_text'])
    report_obj.save()


def get_users_not_reported():
    query_set = Channel.objects.all().filter(UserAlarm=True)
    for channel in query_set:
        temp = []
        temp1 = ''
        print(channel.Name, flush=True)
        reports_object = Reports.objects.filter(ChannelId=channel.ChannelId,
                                                ReportDate__range=[
                                                    str(datetime.now().replace(hour=00, minute=00, second=00)),
                                                    str(datetime.now().now())])
        for r in reports_object:
            temp.append(r.UserId)
        for user in channel.ChannelUsers.all():
            if user not in temp:
                temp1 = temp1 + '<@%s> , \n' % user.UserId
        Client.chat_postMessage(channel=channel.ChannelId,
                                text='These users dont complete their daily report: \n' + temp1)
