#!/usr/bin/env python
from SMM2.encryption import Save as EncryptedSave
from SMM2.save import Save as DecryptedSave
from SMM2.save import SLOT_STATUS
from SMM2.encryption import Course as EncryptedCourse
from SMM2.course import Course as DecryptedCourse

from pathlib import Path

import webview
import widgets
import tgrcode_api
from tgrcode_api import Course as OnlineCourse
from tgrcode_api import Maker as OnlineMaker
import config


def game_style_from_bytes(game_style: bytes) -> str:
    match game_style:
        case b'1M':
            return 'SMB1'
        case b'3M':
            return 'SMB3'
        case b'WM':
            return 'SMW'
        case b'UW':
            return 'NSMBU'
        case b'W3':
            return 'SM3DW'


def load_local_courses(window: webview.Window):
    print('Loading local levels ...')
    save_dir: Path = Path(config.SAVE_DIR)
    encrypted_save = EncryptedSave()
    encrypted_save.load(open(Path(save_dir / 'save.dat'), 'rb').read())
    encrypted_save.decrypt()
    decrypted_save = DecryptedSave()
    decrypted_save.load(encrypted_save.data)
    for course in decrypted_save.downloaded_courses:
        encrypted_course = EncryptedCourse()
        encrypted_course.load(open(Path(save_dir / Path(f'course_data_{course[0]}.bcd')), 'rb').read())
        encrypted_course.decrypt()
        decrypted_course = DecryptedCourse()
        decrypted_course.load(encrypted_course.data)
        if course[1] == SLOT_STATUS.OCCUPIED:
            if decrypted_course.HEADER.DESCRIPTION:
                widgets.insert_my_course(window, decrypted_course.HEADER.NAME,
                                         f'#{course[0]} | '
                                         f'{game_style_from_bytes(decrypted_course.HEADER.GAME_STYLE)} | '
                                         f'{decrypted_course.HEADER.DESCRIPTION}')
            else:
                widgets.insert_my_course(window, decrypted_course.HEADER.NAME,
                                         f'#{course[0]} | '
                                         f'{game_style_from_bytes(decrypted_course.HEADER.GAME_STYLE)}')
        else:
            widgets.insert_my_course(window, '(Empty Slot)', f'#{course[0]}')


def load_online_endless(window: webview.Window,
                        count: int = 10,
                        difficulty_id: str = 'e'):
    print('Loading Endless Challenge ...')
    try:
        courses: list[OnlineCourse] = tgrcode_api.search_endless_mode(count, difficulty_id)
        for course in courses:
            widgets.insert_online_course(window, course.name, course.description)
    except tgrcode_api.TGRCodeAPIException as ex:
        window.evaluate_js(f"showErrorMessage('{str(ex)}')")


class Api:
    def handle_tab_active(self, tab_id: str):
        global window
        if tab_id in ['e', 'n', 'ex', 'sex']:
            widgets.clear_online_course(window)
            load_online_endless(window, 10, tab_id)
        else:
            pass


def webview_init(window: webview.Window):
    load_local_courses(window)
    # load_online_endless(window)
    window.evaluate_js("document.getElementById('tabs').removeAttribute('state');")


if __name__ == '__main__':
    api = Api()
    window = webview.create_window('SMM2Helper', html=open(Path('./web/index.html')).read(), js_api=api)
    webview.start(webview_init, window, gui=config.GUI, debug=config.DEBUG)
