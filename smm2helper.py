#!/usr/bin/env python

from SMM2.encryption import Save as EncryptedSave
from SMM2.save import Save as DecryptedSave
from SMM2.save import SLOT_STATUS
from SMM2.encryption import Course as EncryptedCourse
from SMM2.course import Course as DecryptedCourse
from SMM2.data import GAME_STYLE_NAMES

from pathlib import Path
import webbrowser
import sys

import pyclip
import webview

import widgets
import tgrcode_api
from tgrcode_api import Course as OnlineCourse
from tgrcode_api import Maker as OnlineMaker
import config

save_dir: Path = Path(config.SAVE_DIR)
online_course_list_cache: list[OnlineCourse] = []


def display_an_empty_slot(window: webview.Window, idx: int):
    if config.SHOW_EMPTY_SLOT:
        widgets.insert_my_course(window, '(Empty Slot)', f'#{idx}', idx)


def decrypt_and_display_a_course(window: webview.Window, course: list[int, SLOT_STATUS]):
    global save_dir
    course_file_path: Path = Path(save_dir / Path(f'course_data_{str(course[0]).rjust(3, "0")}.bcd'))
    if course_file_path.exists():
        encrypted_course = EncryptedCourse()
        encrypted_course.load(course_file_path.open('rb').read())
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
    if not Path(save_dir).exists():
        widgets.insert_my_course(window, 'SMM2 save data directory not found',
                                 'Please set "save_dir" in config.yml first.', 0)
        return
    if not Path(save_dir / 'save.dat').exists():
        widgets.insert_my_course(window, 'SMM2 save data not found',
                                 'Please check if "save_dir" in config.yml is a valid SMM2 save data.', 0)
        return
    encrypted_save.load(Path(save_dir / 'save.dat').open('rb').read())
    encrypted_save.decrypt()
    decrypted_save = DecryptedSave()
    decrypted_save.load(encrypted_save.data)
    for course in decrypted_save.own_courses:
        decrypt_and_display_a_course(window, course)
    for course in decrypted_save.downloaded_courses:
        decrypt_and_display_a_course(window, course)


def load_online_random(window: webview.Window,
                       count: int = config.TGRCODE_API_COURSE_COUNT,
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
    except tgrcode_api.TGRCodeAPIBaseException as ex:
        widgets.show_error_message(window, str(ex))


def load_online_popular(window: webview.Window,
                        count: int = config.TGRCODE_API_COURSE_COUNT,
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
    except tgrcode_api.TGRCodeAPIBaseException as ex:
        widgets.show_error_message(window, str(ex))


class Api:
    def __init__(self):
        self.is_random: bool = True  # True: random / False: popular
        self.downloading: bool = False
        self.is_maker_search: bool = False  # True: back to list / False: back to course details
        self.cached_course_name: str | None = None  # Cached course's name
        self.cached_maker: OnlineMaker | None = None  # Cached maker
        self.cached_record_holder: OnlineMaker | None = None  # Cached record holder
        self.is_maker_courses: bool = False  # True: Super Maker World / Maker's courses / False: normal list
        self.cached_window_title: str | None = None

    def handle_tab_active(self, tab_id: str):
        global window
        if tab_id in ['e', 'n', 'ex', 'sex']:
            if self.is_random:
                load_online_random(window, config.TGRCODE_API_COURSE_COUNT, tab_id)
            else:
                load_online_popular(window, config.TGRCODE_API_COURSE_COUNT, tab_id)
        else:
            widgets.show_error_message(window, 'Unknown difficulty ID')

    def handle_switch_random(self) -> bool:
        self.is_maker_courses = False
        self.is_random = not self.is_random
        return self.is_random

    def handle_entry_click(self, parent_id: str, entry_idx):
        global window
        entry_idx = int(entry_idx)
        if parent_id == 'online-courses':
            course: OnlineCourse = online_course_list_cache[entry_idx]
            self.cached_course_name = course.name
            self.cached_maker = course.maker
            self.cached_record_holder = course.record_holder
            widgets.show_online_course_details(window=window, idx=entry_idx, course=course)

    def handle_copy_text(self, text_to_copy: str):
        pyclip.copy(text_to_copy)

    def handle_open_link(self, link: str):
        webbrowser.open(link)

    def handle_download_course_to_slot(self, course_data_id: str, slot_idx: str):
        global window
        self.downloading = True
        print(f'Download {course_data_id} to slot #{slot_idx} ...')
        widgets.show_info_message(window, f'Downloading course {course_data_id} to slot #{slot_idx}, please wait ...')
        output_file = Path(save_dir / Path(f'course_data_{slot_idx.rjust(3, "0")}.bcd'))
        backup_file = Path(save_dir / Path(f'course_data_{slot_idx.rjust(3, "0")}.bcd.bak'))
        if backup_file.exists():
            backup_file.unlink()
        output_file.rename(backup_file)
        with output_file.open('wb') as file_handle:
            try:
                file_handle.write(tgrcode_api.level_data_dataid(int(course_data_id)))
            except Exception as ex:
                widgets.show_error_message(window, str(ex))
                if output_file.exists():
                    output_file.unlink()
                backup_file.rename(output_file)
                self.downloading = False
                return
        widgets.show_success_message(window, 'Download completed')
        widgets.clear_local_course(window)
        load_local_courses(window)
        self.downloading = False

    def handle_search_course(self, course_id: str):
        global window
        print(f'Search course {course_id}')
        try:
            course: OnlineCourse = tgrcode_api.level_info(course_id)
        except (Exception, tgrcode_api.TGRCodeAPIBaseException) as ex:
            widgets.clear_tabs_state(window)
            widgets.show_error_message(window, str(ex))
            return
        self.cached_course_name = course.name
        self.cached_maker = course.maker
        self.cached_record_holder = course.record_holder
        widgets.show_online_course_details(window=window, idx=-1, course=course)

    def handle_set_subtitle(self, subtitle: str | None = None):
        global window
        widgets.set_subtitle(window, subtitle)

    def handle_course_maker_details(self):
        global window
        widgets.show_online_maker_details(window, self.cached_maker)

    def handle_course_record_holder_details(self):
        global window
        widgets.show_online_maker_details(window, self.cached_record_holder)

    def handle_search_maker(self, maker_id: str):
        global window
        print(f'Search maker {maker_id}')
        try:
            maker: OnlineMaker = tgrcode_api.user_info(maker_id)
        except (Exception, tgrcode_api.TGRCodeAPIBaseException) as ex:
            widgets.clear_tabs_state(window)
            widgets.show_error_message(window, str(ex))
            return
        self.cached_maker = maker
        self.is_maker_search = True
        widgets.show_online_maker_details(window=window, maker=maker)

    def handle_load_super_world(self, super_world_id: str):
        global window
        global online_course_list_cache
        self.is_maker_search = False
        self.is_maker_courses = True
        self.cached_window_title = f'Super {self.cached_maker.name} World'
        print(f'Loading Super World {super_world_id} by {self.cached_maker.name}...')
        widgets.clear_online_course(window)
        widgets.insert_online_course(window, 'Loading ...', 'Please wait.', 0)
        try:
            courses: list[OnlineCourse] = tgrcode_api.super_world(super_world_id)
            widgets.clear_online_course(window)
            online_course_list_cache = courses
            for idx in range(0, len(courses)):
                course = courses[idx]
                widgets.insert_online_course(window, course.name,
                                             f'{course.game_style} | '
                                             f'{course.maker.name} | '
                                             f'{tgrcode_api.prettify_course_id(course.course_id)}',
                                             idx)
        except tgrcode_api.TGRCodeAPIBaseException as ex:
            widgets.show_error_message(window, str(ex))

    def handle_load_maker_courses(self, maker_id: str):
        global window
        global online_course_list_cache
        self.is_maker_search = False
        self.is_maker_courses = True
        self.cached_window_title = f'{self.cached_maker.name}\'s courses'
        print(f'Loading {self.cached_window_title} ({maker_id})')
        widgets.clear_online_course(window)
        widgets.insert_online_course(window, 'Loading ...', 'Please wait.', 0)
        try:
            courses: list[OnlineCourse] = tgrcode_api.get_posted(maker_id)
            widgets.clear_online_course(window)
            online_course_list_cache = courses
            for idx in range(0, len(courses)):
                course = courses[idx]
                widgets.insert_online_course(window, course.name,
                                             f'{course.game_style} | '
                                             f'{course.maker.name} | '
                                             f'{tgrcode_api.prettify_course_id(course.course_id)}',
                                             idx)
        except tgrcode_api.TGRCodeAPIBaseException as ex:
            widgets.show_error_message(window, str(ex))

    def get_cached_course_name(self) -> str:
        return self.cached_course_name

    def get_cached_window_title(self) -> str:
        return self.cached_window_title

    def set_is_maker_search(self, is_maker_search) -> bool:
        self.is_maker_search = is_maker_search
        return is_maker_search

    def get_is_maker_search(self) -> bool:
        return self.is_maker_search

    def get_is_maker_courses(self) -> bool:
        return self.is_maker_courses

    def get_tgrcode_api(self) -> str:
        return config.TGRCODE_API

    def get_downloading(self) -> bool:
        return self.downloading


def webview_init(window: webview.Window):
    load_local_courses(window)
    if config.LOAD_ONLINE_ON_START:
        load_online_random(window)
    else:
        widgets.insert_online_course(window, 'Click a tab to load online courses.', '', 0)
    widgets.clear_tabs_state(window)


if __name__ == '__main__':
    api: Api = Api()
    window = webview.create_window(f'SMM2Helper {config.VERSION}', url='web/index.html', js_api=api)
    webview.start(webview_init, window, gui='edgechromium' if sys.platform == 'win32' else 'gtk',
                  debug=config.DEBUG, http_server=True)
