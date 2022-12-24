REGISTER_FORM = [
    {
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": "Please enter additional information",
            "emoji": True
        }
    },
    {
        "type": "input",
        "element": {
            "type": "multi_static_select",
            "placeholder": {
                "type": "plain_text",
                "text": "Select options",
                "emoji": True
            },
            "options": [
                {
                    "text": {
                        "type": "plain_text",
                        "text": " ",  # role
                        "emoji": True
                    },
                    "value": "value-0"  # rol_id
                }
            ],
            "action_id": "multi_static_select_role"
        },
        "label": {
            "type": "plain_text",
            "text": "Please select your current position",
            "emoji": True
        }
    },
    {
        "type": "input",
        "element": {
            "type": "plain_text_input",
            "action_id": "plain_text_input_home_address"
        },
        "label": {
            "type": "plain_text",
            "text": "Please enter your home address",
            "emoji": True
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Please specify the reporting time"
        },
        "accessory": {
            "type": "timepicker",
            "initial_time": "13:37",
            "placeholder": {
                "type": "plain_text",
                "text": "Select time",
                "emoji": True
            },
            "action_id": "timepicker-action-report-time"
        }
    },
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Submit",
                    "emoji": True
                },
                "value": "click_me_123",
                "style": "primary",
                "action_id": "actionId-register-submit"
            }
        ]
    }
]


def plain_text(message):
    plain = [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": message,
                "emoji": True
            }
        },
        {
            "type": "divider"
        }
    ]
    return plain


def report(data):
    report_dict = [
        {
            "type": "divider"
        },
        {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "multiline": True,
                "action_id": "plain_text_yesterday_report"
            },
            "label": {
                "type": "plain_text",
                "text": data['yesterday'],
                "emoji": True
            }
        },
        {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "multiline": True,
                "action_id": "plain_text_today_report"
            },
            "label": {
                "type": "plain_text",
                "text": data['today'],
                "emoji": True
            }
        },
        {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "multiline": True,
                "action_id": "plain_text_blocker"
            },
            "label": {
                "type": "plain_text",
                "text": data['blocker'],
                "emoji": True
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Submit",
                        "emoji": True
                    },
                    "value": "submit report",
                    "style": "primary",
                    "action_id": data['button_id']
                }
            ]
        }
    ]
    return report_dict
