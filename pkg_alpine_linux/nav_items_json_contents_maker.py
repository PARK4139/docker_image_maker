# -*- coding: utf-8 -*-  # python 3.x 하위버전 호환을 위한코드
__author__ = 'PARK4139 : Jung Hoon Park'

from uuid import uuid4

import clipboard

from pkg_park4139_for_linux import BusinessLogicUtil, DebuggingUtil


def _preprocess_description(description):
    description = (description
                   .strip()
                   .replace('\n\n\n', '\n\n')
                   .replace('\n', '\\n')
                   .replace("\"", "\\\"")
                   .replace("\[", "\\\[")
                   # .replace(" ", "🌸")
                   # .replace("\t", "🌸")
                   .replace("    ", "    ")
                   .replace("   ", "   ")
                   .replace("  ", "  ")
                   .replace("\t", "    ")
                   .replace("", r"\\033")
                   .replace("", r"\\a")
                   .replace("", "v")
                   .replace("\S", r"\\S")
                   .replace("\d", r"\\d")
                   .replace("\p", r"\\p")
                   .replace("\s", r"\\s")
                   )
    return description


index: str = uuid4().hex + BusinessLogicUtil.get_time_as_('%Y%m%d%H%M%S%f') + BusinessLogicUtil.get_random_alphabet()
title = 'alpine linux'
href = f'/{title}'
description = '''


'''

nav_item = ""
nav_item = nav_item + "{"
nav_item = nav_item + f'    "index": "{index}",'
# nav_item = nav_item + f'    "title": "{title}",'
nav_item = nav_item + f'    "title": "{title}```",'
# nav_item = nav_item + f'    "href": "{href}",'
nav_item = nav_item + f'    "href": "{href}```",'
nav_item = nav_item + f'    "description": "\\n\\n{_preprocess_description(description)}\\n\\n"'
nav_item = nav_item + "},"

DebuggingUtil.print_ment_success(nav_item)
clipboard.copy(nav_item)
