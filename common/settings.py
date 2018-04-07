# -*- coding: utf-8 -*-

from __future__ import unicode_literals


# common Slack settings
EVENTS = {
    'TYPES': {
        'verification': 'url_verification',
        'callback': 'event_callback'
    },
    'SUBSCRIBED': {
        'user_change': lambda self: self.handle_user_change
    }
}
