from webview import Window
from urllib.parse import quote
import json

from tgrcode_api import Course as OnlineCourse
from tgrcode_api import Maker as OnlineMaker
from tgrcode_api import prettify_course_id
from config import TGRCODE_API, SHOW_THUMBNAILS, VERSION


def quote_vars(*args):
    return map(quote, args)


def readable_number(number: int) -> str:
    if number < 1000:
        return str(number)
    else:
        return f'{number // 1000}k'


# ----

def insert_my_course(window: Window, course_title: str, course_desc: str, idx: int):
    course_title, course_desc = quote_vars(course_title, course_desc)
    window.evaluate_js(f"insertMyCourse(decodeURIComponent('{course_title}'),"
                       f"decodeURIComponent('{course_desc}'),"
                       f"{idx});")


def insert_online_course(window: Window, course_title: str, course_desc: str, idx: int):
    course_title, course_desc = quote_vars(course_title, course_desc)
    window.evaluate_js(f"insertOnlineCourse(decodeURIComponent('{course_title}'),"
                       f"decodeURIComponent('{course_desc}'),"
                       f"{idx});")


def clear_local_course(window: Window):
    window.evaluate_js("clearLocalCourse();")


def clear_online_course(window: Window):
    window.evaluate_js("clearOnlineCourse();")


def clear_tabs_state(window: Window):
    window.evaluate_js("document.getElementById('tabs').removeAttribute('state');")


def show_error_message(window: Window, message: str):
    window.evaluate_js(f"showErrorMessage('{message}')")


def show_success_message(window: Window, message: str):
    window.evaluate_js(f"showSuccessMessage('{message}')")


def show_info_message(window: Window, message: str):
    window.evaluate_js(f"showInfoMessage('{message}')")


def show_dialog(window: Window,
                title: str, content: str, yes_visible: bool = True,
                yes_text: str = "Yes", no_visible: bool = True, no_text: str = "No",
                dialog_callback_id: str = 'default', dialog_callback_object: dict = {}):
    title, content, yes_text, no_text = quote_vars(title, content, yes_text, no_text)
    window.evaluate_js(f"showDialog(decodeURIComponent('{title}'),"
                       f"decodeURIComponent('{content}'),"
                       f"'{str(yes_visible).lower()}',"
                       f"decodeURIComponent('{yes_text}'),"
                       f"'{str(no_visible).lower()}',"
                       f"decodeURIComponent('{no_text}'),"
                       f"{dialog_callback_id},"
                       f"{json.dumps(dialog_callback_object)});")


def show_online_course_details(window: Window, idx: int, course: OnlineCourse):
    set_subtitle(window, course.name)
    api_root: str = TGRCODE_API if SHOW_THUMBNAILS else ''
    window.evaluate_js(f"showOnlineCourseDetails({idx},"
                       f"decodeURIComponent('{quote(course.name)}'),"
                       f"decodeURIComponent('{quote(course.description)}'),"
                       f"decodeURIComponent('{quote(course.uploaded_date)}'),"
                       f"'{prettify_course_id(course.course_id)}',"
                       f"{course.data_id},"
                       f"'{course.game_style}',"
                       f"'{course.theme.split(' ')[0]}',"
                       f"'{course.difficulty}',"
                       f"'{course.tag_1}','{course.tag_2}',"
                       f"decodeURIComponent('{quote(course.world_record)}'),"
                       f"'{course.upload_time}',"
                       f"'{readable_number(course.clears)}',"
                       f"'{readable_number(course.attempts)}',"
                       f"'{course.clear_rate}',"
                       f"'{readable_number(course.likes)}',"
                       f"'{readable_number(course.boos)}',"
                       f"decodeURIComponent('{quote(course.maker.name)}'),"
                       f"'{prettify_course_id(course.maker.maker_id)}',"
                       f"decodeURIComponent('{quote(course.record_holder.name)}'),"
                       f"'{prettify_course_id(course.record_holder.maker_id)}',"
                       f"'{api_root}/level_thumbnail/{course.course_id}',"
                       f"'{api_root}/level_entire_thumbnail/{course.course_id}');")


def show_online_maker_details(window: Window, maker: OnlineMaker):
    set_subtitle(window, maker.name)
    window.evaluate_js("showOnlineMakerDetails("
                       f"decodeURIComponent('{quote(maker.name)}'),"
                       f"decodeURIComponent('{quote(maker.region)}'),"
                       f"'{prettify_course_id(maker.maker_id)}',"
                       f"decodeURIComponent('{quote(maker.country)}'),"
                       f"decodeURIComponent('{quote(maker.last_active)}'),"
                       f"decodeURIComponent('{quote(maker.mii_image_url)}'),"
                       f"'{maker.pose_name}','{maker.hat_name}','{maker.shirt_name}','{maker.pants_name}',"
                       f"{maker.courses_played},{maker.courses_attempted},{maker.courses_cleared},"
                       f"{maker.courses_deaths},{maker.likes},{maker.maker_points},"
                       f"{maker.easy_highscore},{maker.normal_highscore},{maker.expert_highscore},"
                       f"{maker.super_expert_highscore},"
                       f"{maker.versus_rating},'{maker.versus_rank}',{maker.versus_plays},"
                       f"{maker.versus_won},{maker.versus_lost},{maker.versus_disconnected},"
                       f"{maker.coop_clears},{maker.coop_plays},{maker.versus_kills},{maker.versus_killed_by_others},"
                       f"{maker.uploaded_levels},{maker.first_clears},{maker.world_records},{maker.super_world_clears},"
                       f"'{maker.super_world_id}');")


def set_subtitle(window: Window, title: str | None = None):
    window.set_title(f'{title} - SMM2Helper {VERSION}' if title else f'SMM2Helper {VERSION}')
