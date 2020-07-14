# coding: utf-8

import json

import requests
from sentry.plugins.bases.notify import NotificationPlugin

import sentry_dingding
from .forms import DingDingOptionsForm

DingTalk_API = "https://oapi.dingtalk.com/robot/send?access_token={token}"


class DingDingPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to DingDing.
    """
    author = 'dreamerldq'
    author_url = 'https://github.com/dreamerldq/sentry-dingding-format'
    version = '1.0.5'
    description = 'Send project error counts to DingDing .'
    resource_links = [
        ('Source', 'https://github.com/cench/sentry-10-dingding'),
        ('Bug Tracker', 'https://github.com/dreamerldq/sentry-dingding-format/issues'),
        ('README', 'https://github.com/dreamerldq/sentry-dingding-format/blob/master/README.md'),
    ]

    slug = 'WbDingDing'
    title = 'WbDingDing'
    conf_key = slug
    conf_title = title
    project_conf_form = DingDingOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('access_token', project))

    def notify_users(self, group, event, *args, **kwargs):
        self.post_process(group, event, *args, **kwargs)

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        if group.is_ignored():
            return

        access_token = self.get_option('access_token', group.project)
        send_url = DingTalk_API.format(token=access_token)
        title = u'【%s】的项目异常' % event.project.slug

        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": u"#### {title} \n\n > {message} \n\n > {device} \n\n > {uid} \n\n > {path} \n\n [详细信息]({url})".format(
                    title=title,
                    device=event.get_tag('device'),
                    uid=event.get_tag('uid'),
                    path=event.get_tag('url'),
                    message=event.title or event.message,
                    url=u"{}events/{}/".format(group.get_absolute_url(), event.event_id),
                )
            }
        }
        requests.post(
            url=send_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8")
        )
