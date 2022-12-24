from celery import shared_task
from .slack_interfaces.interfaces import get_client
from .model_interactions.methds import get_users_not_reported


@shared_task(bind=True)
def add(self):
    get_users_not_reported()
    # print('hi there')


@shared_task(bind=True)
def alarm_to_all_users(self):
    msg = 'Hey! Are you ready to have our DataCo-Lab daily meeting now?(y/n)'
    print(msg)
    get_client().chat_postMessage(channel='D04DGRSQWD7', user='U012L1M3RUP', text=msg)


@shared_task(bind=True)
def print_temp(self):
    print('*********###### hi there #####***********')
