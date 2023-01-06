#!/usr/bin/env python
from SMM2.encryption import Save as EncryptedSave
from SMM2.save import Save as DecryptedSave
from SMM2.save import SLOT_STATUS
from SMM2.encryption import Course as EncryptedCourse
from SMM2.course import Course as DecryptedCourse
from SMM2.data import GAME_STYLE_NAMES

from pathlib import Path
import webbrowser

import pyclip
import webview

import widgets
import tgrcode_api
from tgrcode_api import Course as OnlineCourse
from tgrcode_api import Maker as OnlineMaker
import config

save_dir: Path = Path(config.SAVE_DIR)
online_course_list_cache: list[OnlineCourse] = []
is_random: bool = True  # True: random / False: popular


def display_an_empty_slot(window: webview.Window, idx: int):
    if config.SHOW_EMPTY_SLOT:
        widgets.insert_my_course(window, '(Empty Slot)', f'#{idx}', idx)


def decrypt_and_display_a_course(window: webview.Window, course: list[int, SLOT_STATUS]):
    global save_dir
    course_file_path: Path = Path(save_dir / Path(f'course_data_{str(course[0]).rjust(3, "0")}.bcd'))
    if course_file_path.exists():
        encrypted_course = EncryptedCourse()
        encrypted_course.load(open(course_file_path, 'rb').read())
        encrypted_course.decrypt()
        decrypted_course = DecryptedCourse()
        decrypted_course.load(encrypted_course.data)
        if course[1] == SLOT_STATUS.OCCUPIED:
            if decrypted_course.HEADER.DESCRIPTION.strip():
                widgets.insert_my_course(window, decrypted_course.HEADER.NAME,
                                         f'#{course[0]} | '
                                         f'{GAME_STYLE_NAMES[decrypted_course.HEADER.GAME_STYLE]} | '
                                         f'{decrypted_course.HEADER.DESCRIPTION}',
                                         course[0])
            else:
                widgets.insert_my_course(window, decrypted_course.HEADER.NAME,
                                         f'#{course[0]} | '
                                         f'{GAME_STYLE_NAMES[decrypted_course.HEADER.GAME_STYLE]}',
                                         course[0])
        else:
            display_an_empty_slot(window, course[0])
    else:
        display_an_empty_slot(window, course[0])


def load_local_courses(window: webview.Window):
    global save_dir
    print('Loading local levels ...')
    encrypted_save = EncryptedSave()
    encrypted_save.load(open(Path(save_dir / 'save.dat'), 'rb').read())
    encrypted_save.decrypt()
    decrypted_save = DecryptedSave()
    decrypted_save.load(encrypted_save.data)
    for course in decrypted_save.own_courses:
        decrypt_and_display_a_course(window, course)
    for course in decrypted_save.downloaded_courses:
        decrypt_and_display_a_course(window, course)


def load_online_random(window: webview.Window,
                       count: int = config.TGRCODE_API_COURSE_NUMBER,
                       difficulty_id: str = 'e'):
    global online_course_list_cache
    print('Loading Endless Challenge ...')
    widgets.clear_online_course(window)
    widgets.insert_online_course(window, 'Loading ...', 'Please wait.', 0)
    try:
        courses: list[OnlineCourse] = tgrcode_api.search_endless_mode(count, difficulty_id)
        widgets.clear_online_course(window)
        online_course_list_cache = courses
        for idx in range(0, len(courses)):
            course = courses[idx]
            widgets.insert_online_course(window, course.name,
                                         f'{course.game_style} | '
                                         f'{course.maker.name} | '
                                         f'{tgrcode_api.prettify_course_id(course.course_id)}',
                                         idx)
    except tgrcode_api.TGRCodeAPIException as ex:
        widgets.show_error_message(window, str(ex))


def load_online_popular(window: webview.Window,
                        count: int = config.TGRCODE_API_COURSE_NUMBER,
                        difficulty_id: str = 'e'):
    global online_course_list_cache
    print('Loading popular levels ...')
    widgets.clear_online_course(window)
    widgets.insert_online_course(window, 'Loading ...', 'Please wait.', 0)
    try:
        courses: list[OnlineCourse] = tgrcode_api.search_popular(count, difficulty_id)
        widgets.clear_online_course(window)
        online_course_list_cache = courses
        for idx in range(0, len(courses)):
            course = courses[idx]
            widgets.insert_online_course(window, course.name,
                                         f'{course.game_style} | '
                                         f'{course.maker.name} | '
                                         f'{tgrcode_api.prettify_course_id(course.course_id)}',
                                         idx)
    except tgrcode_api.TGRCodeAPIException as ex:
        widgets.show_error_message(window, str(ex))


class Api:
    def handle_tab_active(self, tab_id: str):
        global window
        if tab_id in ['e', 'n', 'ex', 'sex']:
            if is_random:
                load_online_random(window, config.TGRCODE_API_COURSE_NUMBER, tab_id)
            else:
                load_online_popular(window, config.TGRCODE_API_COURSE_NUMBER, tab_id)
        else:
            widgets.show_error_message(window, 'Unknown difficulty ID')

    def handle_switch_random(self) -> bool:
        global is_random
        is_random = not is_random
        return is_random

    def handle_entry_click(self, parent_id: str, entry_idx):
        global window
        entry_idx = int(entry_idx)
        if parent_id == 'online-courses':
            widgets.show_online_course_details(window=window, idx=entry_idx, course=online_course_list_cache[entry_idx])

    def handle_copy_text(self, text_to_copy: str):
        pyclip.copy(text_to_copy)

    def handle_open_link(self, link: str):
        webbrowser.open(link)

    def handle_download_course_to_slot(self, course_data_id: str, slot_idx: str):
        pass


def webview_init(window: webview.Window):
    load_local_courses(window)
    if config.LOAD_ONLINE_ON_START:
        load_online_random(window)
    else:
        widgets.insert_online_course(window, 'Click a tab to load online courses.', '', 0)
    widgets.clear_tabs_state(window)


if __name__ == '__main__':
    api: Api = Api()
    window = webview.create_window('SMM2Helper', url='web/index.html', js_api=api)
    webview.start(webview_init, window, gui='gtk', debug=config.DEBUG, http_server=True)
