from ..models import MenuActions, Role, Menu
from .block_forms import REGISTER_FORM


def generate_attachment(menu_name):
    actions = list()
    menu_action_obj = MenuActions.objects.select_related('menu').filter(menu__MenuTitle=menu_name)
    menu_obj = Menu.objects.get(MenuTitle=menu_name)
    text = None
    color = None
    # callback_id = None
    for item in menu_action_obj:
        text = item.menu.TextMessage
        color = item.menu.SideColor
        # callback_id = menu_obj.id
        data = {
            'name': item.Name,
            'text': item.Text,
            'value': item.id,
            'type': 'button'
        }
        actions.append(data)
    return [{
        "text": text,
        "fallback": "You are unable to choose an option",
        "callback_id": menu_name,
        "color": color,
        "attachment_type": "default",
        "actions": actions
    }]


def create_user_register_form():
    mydata = Role.objects.all().values()
    options = list()
    for item in mydata:
        data = {
            "text": {
                "type": "plain_text",
                "text": item["Role"],  # role
                "emoji": True
            },
            "value": str(item["id"])  # rol_id
        }
        options.append(data)
    if len(options) > 0:
        REGISTER_FORM[1]['element']['options'] = options
    return REGISTER_FORM


def create_user_report_header(data):
    res = [
        {
            "color": "#a3a6a8",
            "pretext": "Daily report by <@%s>" % data['user_id'],
            "author_name": data['user_name'],
            "author_icon": data['image_url'],
        }]
    return res


def create_user_report_yesterday(data):
    res = [
        {
            "color": "#0461cc",
            "fields": [
                {
                    "title": "Yesterdays Progress",
                    "value": "• " + data['yesterday_text'].replace("\n", "\n• "),
                    "short": False
                }
            ]
        }
    ]
    return res


def create_user_report_today(data):
    res = [
        {
            "color": "#1c8203",
            "fields": [
                {
                    "title": "Plans for today",
                    "value": "• " + data['today_text'].replace("\n", "\n• "),
                    "short": False
                }
            ]
        }
    ]
    return res


def create_user_report_blocker(data):
    blocker_none_list = ['no', 'No', 'nothing', 'Nothing']
    if data['blocker_text'] is not None and data['blocker_text'] not in blocker_none_list:
        res = [
            {
                "color": "#e61405",
                "fields": [
                    {
                        "title": "Blockers",
                        "value": "• " + data['blocker_text'].replace("\n", "\n• "),
                        "short": False
                    }
                ]
            }
        ]
        return res
    return False


def create_user_report(data):
    blocker_none_list = ['no', 'No', 'nothing', 'Nothing']
    res = [
        {
            "color": "#a3a6a8",
            "pretext": "Daily report by <@%s>" % data['user_id'],
            "author_name": data['user_name'],
            "author_icon": data['image_url'],
        },
        {
            "color": "#0461cc",
            "fields": [
                {
                    "title": "Yesterdays Progress",
                    "value": "• " + data['yesterday_text'].replace("\n", "\n• "),
                    "short": False
                }
            ]
        },
        {
            "color": "#1c8203",
            "fields": [
                {
                    "title": "Plans for today",
                    "value": "• " + data['today_text'].replace("\n", "\n• "),
                    "short": False
                }
            ]
        }
    ]
    if data['blocker_text'] is not None and data['blocker_text'] not in blocker_none_list:
        res.append({
            "color": "#e61405",
            "fields": [
                {
                    "title": "Blockers",
                    "value": "• " + data['blocker_text'].replace("\n", "\n• "),
                    "short": False
                }
            ]
        })
    return res
