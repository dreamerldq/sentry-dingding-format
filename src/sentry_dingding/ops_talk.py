def ops_talk(group, event, *args, **kwargs):
    title = u'【%s】的项目异常' % event.project.slug
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": u"#### {title} \n\n > {message} \n\n > {tags} \n\n > {data} \n\n [详细信息]({url})".format(
                title=title,
                tags=event.as_dict(),
                data=event.data,
                message=event.title or event.message,
                url=u"{}events/{}/".format(group.get_absolute_url(), event.event_id),
            )
        }
    }
    return data
