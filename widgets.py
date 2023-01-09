from webview import Window
from urllib.parse import quote
import json

from tgrcode_api import Course as OnlineCourse
from tgrcode_api import Maker as OnlineMaker
from tgrcode_api import prettify_course_id
from config import TGRCODE_API, SHOW_THUMBNAILS, VERSION, DEBUG


def readable_number(number: int) -> str:
    if number < 1000:
        return str(number)
    else:
        return f'{number // 1000}k'


def evaluate_js(window: Window, function_name: str, args: list | None = None):
    args_str: str = ''
    if args:
        for arg in args:
            match arg:
                case int():
                    args_str += str(arg)
                case str():
                    args_str += f"decodeURIComponent('{quote(arg)}')"
                case bool():
                    args_str += 'true' if arg else 'false'
                case _:
                    args_str += str(arg)
            args_str += ', '
    evaluate_str = f'{function_name}({args_str.strip(", ")});'
    if DEBUG:
        print(evaluate_str)
    window.evaluate_js(evaluate_str)


# ----

def insert_my_course(window: Window, course_title: str, course_desc: str, idx: int):
    evaluate_js(window, 'insertMyCourse', [course_title, course_desc, idx])


def insert_online_course(window: Window, course_title: str, course_desc: str, idx: int):
    evaluate_js(window, 'insertOnlineCourse', [course_title, course_desc, idx])


def clear_local_course(window: Window):
    evaluate_js(window, 'clearLocalCourse')


def clear_online_course(window: Window):
    evaluate_js(window, 'clearOnlineCourse')


def clear_tabs_state(window: Window):
    window.evaluate_js("document.getElementById('tabs').removeAttribute('state');")


def show_error_message(window: Window, message: str):
    evaluate_js(window, 'showErrorMessage', [message])


def show_success_message(window: Window, message: str):
    evaluate_js(window, 'showSuccessMessage', [message])


def show_info_message(window: Window, message: str):
    evaluate_js(window, 'showInfoMessage', [message])


def show_dialog(window: Window,
                title: str, content: str, yes_visible: bool = True,
                yes_text: str = "Yes", no_visible: bool = True, no_text: str = "No",
                dialog_callback_id: str = 'default', dialog_callback_object: dict | None = None):
    evaluate_js(window, 'showDialog', [
        title, content, str(yes_visible).lower(), yes_text, str(no_visible).lower(),
        no_text, dialog_callback_id, json.dumps(dialog_callback_object)
    ])


def show_online_course_details(window: Window, idx: int, course: OnlineCourse):
    api_root: str = TGRCODE_API if SHOW_THUMBNAILS else ''
    evaluate_js(window, 'showOnlineCourseDetails', [
        idx, course.name, course.description, course.uploaded_date, prettify_course_id(course.course_id),
        course.data_id, course.game_style, course.theme.split(' ')[0], course.difficulty, course.tag_1, course.tag_2,
        course.world_record, course.upload_time, readable_number(course.clears), readable_number(course.attempts),
        course.clear_rate, readable_number(course.likes), readable_number(course.boos),
        course.maker.name, prettify_course_id(course.maker.maker_id),
        course.record_holder.name, prettify_course_id(course.record_holder.maker_id),
        f'{api_root}/level_thumbnail/{course.course_id}',
        f'{api_root}/level_entire_thumbnail/{course.course_id}'
    ])


def show_online_maker_details(window: Window, maker: OnlineMaker):
    evaluate_js(window, 'showOnlineMakerDetails', [
        maker.name, maker.region, prettify_course_id(maker.maker_id), maker.country, maker.last_active,
        maker.mii_image_url, maker.pose_name, maker.hat_name, maker.shirt_name, maker.pants_name,
        maker.courses_played, maker.courses_attempted, maker.courses_cleared, maker.courses_deaths, maker.likes,
        maker.maker_points, maker.easy_highscore, maker.normal_highscore, maker.expert_highscore,
        maker.super_expert_highscore, maker.versus_rating, maker.versus_rank, maker.versus_plays,
        maker.versus_won, maker.versus_lost, maker.versus_disconnected, maker.coop_clears, maker.coop_plays,
        maker.versus_kills, maker.versus_killed_by_others, maker.uploaded_levels, maker.first_clears,
        maker.world_records, maker.super_world_clears, maker.super_world_id
    ])


def set_subtitle(window: Window, title: str | None = None):
    window.set_title(f'{title} - SMM2Helper {VERSION}' if title else f'SMM2Helper {VERSION}')
