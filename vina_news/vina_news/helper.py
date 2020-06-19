# -*- coding: utf-8 -*-
import re
from lxml.html.clean import clean_html
from w3lib.html import remove_tags


def bodyCleaner(htmlArr):
    body = [clean_html(x) for x in htmlArr]
    body = [re.sub('<table.+?</table>', '', x, flags=re.DOTALL)
            for x in body]
    body = [re.sub('<div class="pswp-content__caption".+?</div>',
                   '', x, flags=re.DOTALL) for x in body]
    body = [re.sub('<div class="imgcaption".+?</div>',
                   '', x, flags=re.DOTALL) for x in body]
    body = [remove_tags(x).strip() for x in body]
    body = ''.join(body)
    body = body.replace(
        'To view this video please enable JavaScript, and consider upgrading to a web browser that\n          supports HTML5 video', '')
    body = body.replace('Xem thêm video:', '')
    body = body.replace('Xem chi tiết tại đây', '')

    return body
