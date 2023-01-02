from webview import Window
from urllib.parse import quote


def insert_my_course(window: Window, course_title: str, course_desc: str):
    course_title = quote(course_title)
    course_desc = quote(course_desc)
    window.evaluate_js(f"insertMyCourse(decodeURIComponent('{course_title}'),"
                       f"decodeURIComponent('{course_desc}'));")


def insert_online_course(window: Window, course_title: str, course_desc: str):
    course_title = quote(course_title)
    course_desc = quote(course_desc)
    window.evaluate_js(f"insertOnlineCourse(decodeURIComponent('{course_title}'),"
                       f"decodeURIComponent('{course_desc}'));")


def clear_online_course(window: Window):
    window.evaluate_js("clearOnlineCourse();")


def clear_tabs_state(window: Window):
    window.evaluate_js("document.getElementById('tabs').removeAttribute('state');")


def show_error_message(window: Window, error_message: str):
    window.evaluate_js(f"showErrorMessage('{error_message}')")
